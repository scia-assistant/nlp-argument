"""Module that contains the evaluation of the perplexity"""

from typing import List, Union

import torch
from datasets import load_dataset
from tqdm import tqdm
from transformers import logging


def _default_text() -> List[str]:
    test = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    return test["text"]


def eval_perplexity(
    tokenizer,
    model,
    max_context_length,
    text_input: Union[str, List],
    device: str = "cpu",
    verbose: bool = True,
) -> float:
    """Given a text and a LLM, compute its perplexity.

    Args:
        tokenizer (_type_): The llm tokenizer
        model (_type_): The llm model
        max_context_length (_type_): The max text length the llm has been trained with.
        text_input (Union[str, List]): The text which will be use to compute the perplexity.
        device (str, optional): Which device is used. Defaults to "cpu".
        verbose (bool, optional): Display advancement of the pipeline if sets to True.
        Defaults to True.

    Returns:
        float: The perplexity
    """

    text_str: str = (
        text_input if isinstance(text_input, str) else "\n\n".join(text_input)
    )

    if verbose:
        print("Encoding input...")

    logging.set_verbosity_error()
    encodings = tokenizer(text_str, return_tensors="pt")
    logging.set_verbosity_warning()

    stride = max_context_length
    seq_len = encodings.input_ids.size(1)

    if verbose:
        print("Model max context size :", max_context_length)
        print("Input size (number of token) :", seq_len)

    nlls = []
    prev_end_loc = 0
    for begin_loc in tqdm(range(0, seq_len, stride), desc="Compute perplexity"):
        end_loc = min(begin_loc + max_context_length, seq_len)
        trg_len = end_loc - prev_end_loc  # may be different from stride on last loop
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)

            # loss is calculated using CrossEntropyLoss which averages over valid labels
            # N.B. the model only calculates loss over trg_len - 1 labels, because it internally shifts the labels
            # to the left by 1.
            neg_log_likelihood = outputs.loss

        nlls.append(neg_log_likelihood)

        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    ppl = torch.exp(torch.stack(nlls).mean())
    return ppl.item()


def _main():
    from load_llm.load_llm import LLMPretrained, LLMWrapper

    model = LLMWrapper(llm_pretrained=LLMPretrained.GPT2_SMALL)

    ppl = eval_perplexity(
        tokenizer=model.tokenizer,
        model=model.model,
        max_context_length=model.get_max_context_length(),
        text_input="Once upon a time",
    )
    print("Perplexity :", ppl)


if __name__ == "__main__":
    _main()
