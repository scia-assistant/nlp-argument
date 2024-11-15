"""Module that loads different pre-trained LLM"""

from enum import Enum
from typing import Any, Callable, Tuple

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    GPT2LMHeadModel,
    GPT2Tokenizer,
    GPTNeoXForCausalLM,
    PreTrainedModel,
)


class LLMPretrained(Enum):
    """Different pre-trained LLM model.

    Args:
        Enum (str): Id of the model when loading it
    """

    # GPT2
    GPT2_SMALL = "distilgpt2"
    GPT2_BASE = "gpt2"
    GPT2_MEDIUM = "gpt2-medium"
    GPT2_LARGE = "gpt2-large"
    GPT2_XL = "gpt2-xl"  # using this one can crash your PC, it did with mine
    # GPT NEO
    GPT_NEO_SMALL = "EleutherAI/gpt-neo-125M"
    GPT_NEO_LARGE = "EleutherAI/gpt-neo-1.3B"
    # pythia
    PYTHIA_14M = "EleutherAI/pythia-14m"
    PYTHIA_410M = "EleutherAI/pythia-410m"
    PYTHIA_1B = "EleutherAI/pythia-1b"
    PYTHIA_1_4B = "EleutherAI/pythia-1.4b"  # may take time
    PYTHIA_2_8B = "EleutherAI/pythia-2.8b"  # dangerous
    PYTHIA_6_9B = "EleutherAI/pythia-6.9b"  # suicidal
    PYTHIA_12B = "EleutherAI/pythia-12b"  # we are not in a fairy tail ok !
    # flan
    FLAN_SMALL = "google/flan-t5-small"
    FLAN_BASE = "google/flan-t5-base"
    # olmo
    OLMO = "allenai/OLMo-1B-0724-hf"
    # TinyLlama
    TINY_LLAMA = "TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T"


class LLMWrapper:  # pylint: disable=too-few-public-methods
    """Wrapper class of pre-trained LLM and their tokenizer"""

    def __init__(self, llm_pretrained: LLMPretrained, verbose: bool = True):

        self.version = llm_pretrained
        tokenizer_loader, model_loader = self._get_loaders(llm_pretrained)

        if verbose:
            print("Loading tokenizer...")
        self.tokenizer = tokenizer_loader(llm_pretrained.value)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        if verbose:
            print("Loading model...")
        self.model = model_loader(llm_pretrained.value)

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.nb_parameters = sum(p.numel() for p in self.model.parameters())

    @staticmethod
    def _get_loaders(
        llm_pretrained: LLMPretrained,
    ) -> Tuple[Callable[[str], Any], Callable[[str], PreTrainedModel]]:
        if llm_pretrained.name.startswith("GPT2"):
            return (GPT2Tokenizer.from_pretrained, GPT2LMHeadModel.from_pretrained)

        if llm_pretrained.name.startswith("GPT_NEO"):
            return (AutoTokenizer.from_pretrained, AutoModelForCausalLM.from_pretrained)

        if llm_pretrained.name.startswith("FLAN"):
            return (
                AutoTokenizer.from_pretrained,
                AutoModelForSeq2SeqLM.from_pretrained,
            )

        if llm_pretrained.name.startswith("OLMO"):
            return (AutoTokenizer.from_pretrained, AutoModelForCausalLM.from_pretrained)

        if llm_pretrained.name.startswith("PYTHIA"):
            return (AutoTokenizer.from_pretrained, GPTNeoXForCausalLM.from_pretrained)

        if llm_pretrained.name.startswith("TINY_LLAMA"):
            return (AutoTokenizer.from_pretrained, AutoModelForCausalLM.from_pretrained)

        raise ValueError(f"LLMLoader '{llm_pretrained.name}' has not loaders")

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

    def get_max_context_length(self):
        """Gets the max text length the LLM has been trained with."""
        if self.version.name.startswith("GPT2") or self.version.name.startswith("FLAN"):
            return self.model.config.n_positions
        if self.version.name.startswith("GPT_NEO"):
            return self.model.config.max_position_embeddings
        raise ValueError(
            f"LLMLoader '{self.version.name}' has not a max context length"
        )


if __name__ == "__main__":
    text = LLMWrapper(llm_pretrained=LLMPretrained.TINY_LLAMA).generate_text(
        "Once upon a time"
    )
    print("Generated text :\n", text)
