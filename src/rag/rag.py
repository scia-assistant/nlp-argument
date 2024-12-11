import torch
from langchain_community.document_loaders import UnstructuredHTMLLoader
from load_llm.load_llm import LLMPretrained, LLMWrapper
from langchain.docstore.document import Document
from transformers import pipeline

class RAG:
    def __init__(self, vector_store, model, tokenizer=None) -> None:
        self.vector_store = vector_store
        self.model = model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.model.to(self.device)
        if tokenizer is None:
            self.tokenizer = self.model.tokenizer
        else:
            self.tokenizer = tokenizer
        print("creating pipeline")
        # self.READER_LLM = pipeline(
        #     model=self.model.model,
        #     tokenizer=self.tokenizer,
        #     task="text-generation",
        #     # do_sample=True,
        #     # temperature=0.3,
        #     repetition_penalty=1.2,
        #     return_full_text=False,
        #     max_new_tokens=500,
        #     device=self.device
        # )
        print("done creating pipeline")


    def retrieve_k_top(self, k: int, query: str):
        return self.vector_store.similarity_search_with_score(query=query, k=k)

    def get_formatted_prompt(self, query: str, retrieved_texts: list[str]):
        PROMPT_TEMPLATE = """
Vous êtes un chatbot. En utilisant uniquement les textes fournis dans la partie contexte, donnez une réponse complète à la question, en citant les passages des textes qui vous ont permis de répondre.\n
Contexte:\n
{context}\n
Question: {question}\n
Réponse:"""
        context = ""
        context += "".join(
            [
                f"Document {str(i)}:\n" + doc + "\n"
                for i, doc in enumerate(retrieved_texts)
            ]
        )

        return PROMPT_TEMPLATE.format(question=query, context=context)

    def generate_answer(self, k: int, query: str):
        print("retriving documents...")
        inputs = self.tokenizer(query, return_tensors="pt").to(self.device)
        output = self.model.model.generate(
            inputs["input_ids"],
            max_new_tokens=500,             # Maximum number of tokens to generate
            do_sample=True,                 # Enable sampling for more diverse output
            temperature=0.7,                # Sampling temperature (lower for more focused, higher for more random)
            repetition_penalty=1.2,         # Penalize repetitive sequences
            pad_token_id=self.tokenizer.eos_token_id  # Set pad token to avoid warnings for some models
        )
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return generated_text
        #res_similarity = self.retrieve_k_top(k, query)

        #retrieved_docs_text = [doc.page_content for doc, _  in res_similarity]

        # print("documents retrived generating response")
        # # RAG_PROMPT_TEMPLATE = self.get_formatted_prompt(query, retrieved_docs_text)
        # prompt = "Quels sont les critères pris en compte par la Cour de cassation pour reconnaître une faute inexcusable de l'employeur en matière de droit du travail ?\nAnswer:"


        # #answer = self.READER_LLM(RAG_PROMPT_TEMPLATE)[0]["generated_text"]
        # answer = self.READER_LLM(prompt)[0]["generated_text"]

        #return answer
        #return res_similarity, answer