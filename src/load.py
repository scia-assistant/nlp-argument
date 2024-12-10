# pip install datasets
import datasets
from tqdm.notebook import tqdm
from datasets import load_dataset
from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import pandas as pd
import matplotlib.pyplot as plt
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from load_llm.load_llm import LLMPretrained, LLMWrapper
from sentence_transformers import SentenceTransformer
from transformers import CamembertModel, CamembertTokenizer
import sentencepiece
from data_ingestion.retriever import Retriever
from rag.rag import RAG
EMBEDDING_MODEL_NAME = "thenlper/gte-small"
READER_MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
EMBEDDING_DIR = "embeddings_dir"

import os
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

retriever = Retriever(embedding_model=embedding_model, text_splitter=text_splitter, vector_store_path="faiss_index")#, documents=RAW_KNOWLEDGE_BASE)

rag = RAG(vector_store=retriever.vector_store, model=model)

# query = "Quelles sont les principales erreurs de droit que la Cour de cassation identifie dans ses décisions ?"
query = "Quels sont les critères pris en compte par la Cour de cassation pour reconnaître une faute inexcusable de l'employeur en matière de droit du travail ?"
res_similarity, answer = rag.generate_answer(k=5, query=query)
print("================QUESTION====================")
print(query)
print("================RETRIEVED TEXTS====================")
for doc, score in res_similarity:
    print(doc)
    print(f"Score {score}")
print("================ANSWER====================")
print(answer)
