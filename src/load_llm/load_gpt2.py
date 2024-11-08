"""Module that loads different size of GPT2 LLM"""

from enum import Enum

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer  # type: ignore


class GPT2_size(Enum):  # pylint: disable=invalid-name
    """The different size of GPT2 model that are available.

    Args:
        Enum (str): Id of the model when loading it
    """

    SMALL = "distilgpt2"
    BASE = "gpt2"
    MEDIUM = "gpt2-medium"
    LARGE = "gpt2-large"
    XL = "gpt2-xl"  # using this one can crash your PC, it did with mine


class GPT2_model:  # pylint: disable=invalid-name, too-few-public-methods
    """Wrapper class of the LLM GPT2 and its tokenizer"""

    def __init__(self, gpt2_size: GPT2_size = GPT2_size.BASE, verbose: bool = True):
        if verbose:
            print("Loading tokenizer...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(gpt2_size.value)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        if verbose:
            print("Loading model...")
        self.model = GPT2LMHeadModel.from_pretrained(gpt2_size.value)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate_text(
        self, prompt: str, max_length: int = 100, verbose: bool = True, **kwargs
    ) -> str:
        """Given a prompt, generate text that may follow it

        Args:
            prompt (str): The beginning of the generated text.
            max_length (int, optional): ax number of generated token. Defaults to 100.
            verbose (bool, optional): Display advancement of the pipeline if sets to True.
            Defaults to True.

        Returns:
            str: The genereated text beginning by the given prompt
        """
        if verbose:
            print("Tokenize...")
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        kwargs.setdefault("temperature", 0.7)
        kwargs.setdefault("top_k", 50)
        kwargs.setdefault("top_p", 0.95)
        kwargs.setdefault("num_return_sequences", 1)
        kwargs.setdefault("do_sample", True)

        if verbose:
            print("Generate...")
        outputs = self.model.generate(
            inputs=inputs["input_ids"],
            max_length=max_length,
            attention_mask=inputs["attention_mask"],
            pad_token_id=self.tokenizer.eos_token_id,
            **kwargs,
        )

        if verbose:
            print("Detokenize...")
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


if __name__ == "__main__":
    text = GPT2_model(gpt2_size=GPT2_size.SMALL).generate_text("Once upon a time")
    print(len(text.split(" ")))
    print("Generated text :\n", text)
