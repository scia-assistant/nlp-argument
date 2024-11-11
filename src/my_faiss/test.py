import hashlib
import os

import faiss
import numpy as np
import pdfplumber
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer


def get_pdf_text_hash(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "".join(
            page.extract_text() for page in pdf.pages if page.extract_text()
        )
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, text_hash


def chunk_text(text, chunk_size):
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
    return chunks


def add_document_to_index(data_folder, db, index):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunk_size = 200
    chunks_collection = db["chunks"]

    # go through data_folder to index files that are not indexed
    for file_name in os.listdir(data_folder):
        file_path = os.path.join(data_folder, file_name)

        if file_name.endswith(".pdf"):
            text, text_hash = get_pdf_text_hash(file_path)
        else:
            continue

        if not chunks_collection.find_one({"file_hash": text_hash}):
            chunks = chunk_text(text, chunk_size)

            # Process each chunk
            for chunk_num, chunk in enumerate(chunks):
                # Generate embedding for each chunk
                embedding = model.encode([chunk]).astype(np.float32)

                faiss_id = index.ntotal
                # Add to the index
                index.add(embedding)
                chunks_collection.insert_one(
                    {
                        "file_name": file_name,
                        "file_hash": text_hash,
                        "faiss_id": faiss_id,
                        "text": chunk,
                    }
                )

    return index


username = "admin"
password = "admin123"

uri = f"mongodb://{username}:{password}@localhost:27017/faiss_db?authSource=admin"
client = MongoClient(uri)

db = client["faiss_db"]

data_folder = "datas/"
index_path = "index.faiss"

if os.path.exists(index_path):
    index = faiss.read_index(index_path)
else:
    dimension = 384
    index = faiss.IndexFlatL2(dimension)
    faiss.write_index(index, index_path)

index = add_document_to_index(data_folder, db, index)

faiss.write_index(index, "index.faiss")
