from langchain_community.document_loaders import UnstructuredHTMLLoader
from load_llm.load_llm import LLMPretrained, LLMWrapper
from langchain.docstore.document import Document
from transformers import pipeline

class RAG:
    def __init__(self, vector_store, model_name: LLMPretrained) -> None:
        self.vector_store = vector_store
        self.model = LLMWrapper(llm_pretrained=model_name)

    def retrieve_k_top(self, k:int, query: str):
        return self.vector_store.similarity_search(query=query, k=k)
    
    def get_formatted_prompt(self, query: str, retrieved_texts: list[str]):
        PROMPT_TEMPLATE = """
        Using the information contained in the context,
        give a comprehensive answer to the question.\n
        Respond only to the question asked, response should be concise and relevant to the question.
        Provide the number of the source document when relevant.
        If the answer cannot be deduced from the context, do not give an answer.\n
        Context:\n
        {context}\n
        ---\n
        Now here is the question you need to answer.\n

        Question: {question}\n"""
        context = ""
        context += "".join([f"Document {str(i)}:::\n" + doc + "\n" for i, doc in enumerate(retrieved_texts)])

        return PROMPT_TEMPLATE.format(question=query, context=context)   
    
    # def generate_answer(self, k:int, query: str):
    #     retrieved_docs = self.retrieve_k_top(k, query)
    #     retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
    #     prompt = self.get_formatted_prompt(query=query, retrieved_texts=retrieved_docs_text)
    #     print('===========PROMPT=============')
    #     print(prompt)
    #     res = self.model.generate_text(prompt=prompt, max_length=1000)
    #     print('===========RESULT=============')
    #     print(res)

    def generate_answer(self, k:int, query: str, model, tokenizer):

        READER_LLM = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    do_sample=True,
    temperature=0.2,
    repetition_penalty=1.1,
    return_full_text=False,
    max_new_tokens=500,
)
        
        prompt_in_chat_format = [
    {
        "role": "system",
        "content": """Using the information contained in the context,
give a comprehensive answer to the question.
Respond only to the question asked, response should be concise and relevant to the question.
Provide the number of the source document when relevant.
If the answer cannot be deduced from the context, do not give an answer.""",
    },
    {
        "role": "user",
        "content": """Context:
{context}
---
Now here is the question you need to answer.

Question: {question}""",
    },
]
        RAG_PROMPT_TEMPLATE = tokenizer.apply_chat_template(
    prompt_in_chat_format, tokenize=False, add_generation_prompt=True
)
        retrieved_docs = self.retrieve_k_top(k, query)
        retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
        context = "\nExtracted documents:\n"
        context += "".join([f"Document {str(i)}:::\n" + doc for i, doc in enumerate(retrieved_docs_text)])
        final_prompt = RAG_PROMPT_TEMPLATE.format(question=query, context=context)
        print('===========PROMPT=============')
        print(final_prompt)
        answer = READER_LLM(final_prompt)[0]["generated_text"]
        print('===========RESULT=============')
        print(answer)


