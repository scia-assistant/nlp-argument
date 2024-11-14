# pip install datasets
import datasets
from tqdm.notebook import tqdm
from datasets import load_dataset
from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
import pandas as pd
import matplotlib.pyplot as plt
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

from retriever import Retriever

EMBEDDING_MODEL_NAME = "thenlper/gte-small"
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

embedding_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    encode_kwargs={"normalize_embeddings": True},  # Set `True` for cosine similarity
)



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

retriever = Retriever(embedding_model=embedding_model, text_splitter=text_splitter, vector_store_path="faiss_index")

# docs = []
# for doc in RAW_KNOWLEDGE_BASE:
#     docs += text_splitter.split_documents([doc])


tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-small")


user_query = "Aux termes de leurs dernières conclusions notifiées le 23 décembre 2022 par voie électronique, et au visa des articles 1792 et suivants"
retrieved_docs = retriever.vector_store.similarity_search(query=user_query, k=5)
for doc in retrieved_docs:
    print(doc)
    print("-----------------------------------------")