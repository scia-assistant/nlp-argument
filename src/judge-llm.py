from typing import Tuple
from load_llm.load_llm import LLMPretrained, LLMWrapper
from rag.rag import RAG
from transformers import Pipeline

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage



EVALUATION_PROMPT = """[System]
Please act as an impartial judge and evaluate the quality of the responses provided by two
AI assistants to the user question displayed below. You should choose the assistant that
follows the user’s instructions and answers the user’s question better. Your evaluation
should consider factors such as the helpfulness, relevance, accuracy, depth, creativity,
and level of detail of their responses. Begin your evaluation by comparing the two
responses and provide a short explanation. Avoid any position biases and ensure that the
order in which the responses were presented does not influence your decision. Do not allow
the length of the responses to influence your evaluation. Do not favor certain names of
the assistants. Be as objective as possible. After providing your explanation, output your
final verdict by strictly following this format: "[[A]]" if assistant A is better, "[[B]]"
if assistant B is better, and "[[C]]" for a tie.
[User Question]
{question}
[The Start of Assistant A’s Answer]
{answer_a}
[The End of Assistant A’s Answer]
[The Start of Assistant B’s Answer]
{answer_b}
[The End of Assistant B’s Answer]"""


class LLMJudge:
    """Class to judge the output of two LLMs"""

    def __init__(self, llm: Pipeline, llm_rag: RAG, judge: LLMWrapper):
        self.llm = llm
        self.llm_rag = llm_rag
        self.judge = judge


    def judge_outputs(
        self, query: str, max_length: int = 100, verbose: bool = True, **kwargs
    ) -> Tuple[str, str, str]:
        
        output1 = self.llm1.generate(query)
        output2 = self.llm_rag.generate(k=5, query=query)

        evaluation_prompt = EVALUATION_PROMPT.format(
            question=query, answer_a=output1, answer_b=output2
        )

        # Change to Chatgpt4 need api key
        judgment = self.judge.generate_text(evaluation_prompt, max_length=max_length, verbose=verbose, **kwargs)

        return output1, output2, judgment



def create_pipeline_std_llm() -> Pipeline:
    return None


if __name__ == "__main__":
    llm1 = LLMWrapper(llm_pretrained=LLMPretrained.GPT2_BASE)
    llm2 = LLMWrapper(llm_pretrained=LLMPretrained.FLAN_SMALL)

    judge = LLMJudge(llm1, llm2)

    prompt = "Explain the importance of renewable energy."

    output1, output2, judgment = judge.judge_outputs(prompt)

    print("Model 1 Output:\n", output1)
    print("\nModel 2 Output:\n", output2)
    print("\nJudgment:\n", judgment)
