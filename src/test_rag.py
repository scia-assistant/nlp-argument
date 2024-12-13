import joblib
import os
import torch

from tqdm.notebook import tqdm
from datasets import load_dataset
from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from load_llm.load_llm import LLMPretrained, LLMWrapper
from data_ingestion.retriever import Retriever
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel, LlamaForCausalLM
from langchain_community.vectorstores import FAISS

from rag.rag import RAG
EMBEDDING_MODEL_NAME = "thenlper/gte-small"
READER_MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
EMBEDDING_DIR = "embeddings_dir"

os.environ["TOKENIZERS_PARALLELISM"] = "false"

embedding_model = HuggingFaceEmbeddings(
    model_name="Lajavaness/sentence-camembert-large",
    encode_kwargs={"normalize_embeddings": True}
)

model = LLMWrapper(llm_pretrained=LLMPretrained.TINY_LLAMA)

dataset = load_dataset("antoinejeannot/jurisprudence", "cour_de_cassation")

RAW_KNOWLEDGE_BASE = [
    LangchainDocument(page_content=doc["text"], metadata={"source": doc["id"]}) for doc in tqdm(dataset['train'].take(1000))
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    add_start_index=True,
    strip_whitespace=True
)

def main(create_faiss : bool = False):
    if not create_faiss:
        retriever = Retriever(embedding_model=embedding_model, text_splitter=text_splitter, vector_store_path="src/faiss_index")
    else:
        retriever = Retriever(embedding_model=embedding_model, text_splitter=text_splitter, vector_store_path="src/faiss_index", documents=RAW_KNOWLEDGE_BASE)
    rag = RAG(vector_store=retriever.vector_store, model=model)
    rag.model.model.to("cpu")
    query = "Quels sont les critères pris en compte par la Cour de cassation pour reconnaître une faute inexcusable de l'employeur en matière de droit du travail ?"
    answer = rag.generate_answer(k=5, query=query)
    print("================QUESTION====================")
    print(query)
    print("================ANSWER====================")
    print(answer)

if __name__ == "__main__":
    main()