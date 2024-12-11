from typing import Tuple
from load_llm.load_llm import LLMPretrained, LLMWrapper
from rag.rag import RAG
from transformers import Pipeline
from data_ingestion.retriever import Retriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline
from openai import OpenAI
import csv



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


    def openai_api(self, prompt):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.4,
        )

        return response.choices[0].message.content


    def judge_outputs(
        self, query: str, max_length: int = 100, verbose: bool = True, **kwargs
    ) -> Tuple[str, str, str]:
        
        RAG_PROMPT_TEMPLATE = f"""
Vous êtes un chatbot. Donnez une réponse complète à la question\n
Question: {query}\n
Réponse:"""


        output1 = self.llm(RAG_PROMPT_TEMPLATE)[0]["generated_text"]
        _, output2 = self.llm_rag.generate_answer(k=5, query=query)

        evaluation_prompt = EVALUATION_PROMPT.format(
            question=query, answer_a=output1, answer_b=output2
        )

        judgment = self.openai_api(evaluation_prompt)


        return output1, output2, judgment
    

    def pair_wise_evaluation(self, nb_sample, file_path):
        questions = []
        counts = {"countA": 0, "countB": 0, "countC": 0, "tot": 0}


        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    questions.append(row[0])
                    
        for i in range(min(nb_sample, len(questions))):
            _, _, judgment = self.judge_outputs(query=questions[i])
            # print(judgment)
            if "[[B]]" in judgment:
                counts["countB"] += 1
            elif "[[A]]" in judgment:
                counts["countA"] += 1
            elif "[[C]]" in judgment:
                counts["countC"] += 1

        return counts




def create_pipeline_std_llm() -> Pipeline:
    model = LLMWrapper(llm_pretrained=LLMPretrained.TINY_LLAMA)
    READER_LLM = pipeline(
        model=model.model,
        tokenizer=model.tokenizer,
        task="text-generation",
        # do_sample=True,
        # temperature=0.3,
        repetition_penalty=1.2,
        return_full_text=False,
        max_new_tokens=500,
        device='cpu'
    )

    return READER_LLM


def create_pipepline_rag_llm() -> RAG:
    embedding_model = HuggingFaceEmbeddings(
        model_name="Lajavaness/sentence-camembert-large",
        encode_kwargs={"normalize_embeddings": True}
    )
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=50,
        add_start_index=True,
        strip_whitespace=True
    )
    model = LLMWrapper(llm_pretrained=LLMPretrained.TINY_LLAMA)
    retriever = Retriever(embedding_model=embedding_model, text_splitter=text_splitter, vector_store_path="faiss_index")

    rag = RAG(vector_store=retriever.vector_store, model=model)
    return rag




if __name__ == "__main__":
    
    llm1 = create_pipeline_std_llm()
    llm2 = create_pipepline_rag_llm()

    judge = LLMJudge(llm1, llm2, None)

    prompt = "Quels sont les critères pris en compte par la Cour de cassation pour reconnaître une faute inexcusable de l'employeur en matière de droit du travail ?"
    print(judge.pair_wise_evaluation(nb_sample=10, file_path="./questions.csv"))

