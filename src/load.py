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

from data_ingestion.retriever import Retriever
from rag.rag import RAG
EMBEDDING_MODEL_NAME = "thenlper/gte-small"
READER_MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
EMBEDDING_DIR = "embeddings_dir"

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
)

# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.bfloat16,
# )

# model = AutoModelForCausalLM.from_pretrained(READER_MODEL_NAME, quantization_config=bnb_config)
# tokenizer = AutoTokenizer.from_pretrained(READER_MODEL_NAME)

model = LLMWrapper(llm_pretrained=LLMPretrained.TINY_LLAMA)

dataset = load_dataset("antoinejeannot/jurisprudence", "tribunal_judiciaire")

RAW_KNOWLEDGE_BASE = [
    LangchainDocument(page_content=doc["text"], metadata={"source": doc["id"]}) for doc in tqdm(dataset['train'].take(100))
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,  # The maximum number of characters in a chunk: we selected this value arbitrarily
    chunk_overlap=50,  # The number of characters to overlap between chunks (10%)
    add_start_index=True,  # If `True`, includes chunk's start index in metadata
    strip_whitespace=True  # If `True`, strips whitespace from the start and end of every document
)

retriever = Retriever(embedding_model=embedding_model, text_splitter=text_splitter, vector_store_path=f"faiss_index")

rag = RAG(vector_store=retriever.vector_store, model=model)

# rag.generate_answer(k=5, query="Qu'est-ce qu'un litige?", model=model, tokenizer=tokenizer)
rag.generate_answer(k=5, query="Qu'est-ce qu'un litige?")