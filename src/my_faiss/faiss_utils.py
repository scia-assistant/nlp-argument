import gc
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from files_utils import chunk_text, get_pdf_text_hash


def add_documents(data_path, db, index_path, chunk_size=200):
    """
    Create embedding and add it in a faiss file.
    Also add informations of each embedding in db:
        file_name: name of file from which embending originates
        file_hash: hash of the file to save that we already indexed it
        faiss_id: id of index in faiss file
        text: text of the chunk

    args:
        data_path: where data to indexed is.
        db: the mongo db where we stock informations
        index_path: where index is save
        chunk_size: number of word per embedding
    """

    model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    chunks_collection = db["chunks"]

    # load or create index
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
    else:
        index = faiss.IndexFlatL2(384)

    # go through data_path to index files that are not indexed
    for file_name in os.listdir(data_path):
        file_path = os.path.join(data_path, file_name)

        if file_name.endswith(".pdf"):
            text, text_hash = get_pdf_text_hash(file_path)
        # add other function for other type of files
        else:
            continue

        if chunks_collection.find_one({"file_hash": text_hash}):
            continue

        print(f"process {file_path}")
        chunks = chunk_text(text, chunk_size)
        documents = []

        # Process each chunk
        for chunk_num, chunk in enumerate(chunks):
            embedding = model.encode([chunk]).astype(np.float32)
            # embedding = np.random.rand(384).reshape(
            #     1, -1
            # )  # for dorian because with model it's not working for me

            faiss_id = index.ntotal
            index.add(embedding)
            documents.append(
                {
                    "file_name": file_name,
                    "file_hash": text_hash,
                    "faiss_id": faiss_id,
                    "text": chunk,
                }
            )
        chunks_collection.insert_many(documents)
        gc.collect()

    faiss.write_index(index, index_path)

    print(f"All data are store in the db and the index is save in {index_path}")


def search_neighbors(db, query_text: str, index_path, nb_neighbors=5):
    """
    search neighbors closest to the query
    args:
        db: db where data is store
        query_text: the query
        index_path: where index is save
        nb_neighbors: number of neighbors we want in the array
    return:
        an array of nb_neighbors elements of the indexes closest to the query
    """

    model = SentenceTransformer("all-MiniLM-L6-v2")

    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
    else:
        raise Exception("the index_path doesn't exist")

    query_embedding = model.encode([query_text]).astype(np.float32)
    # query_embedding = np.random.rand(384).reshape(
    #     1, -1
    # )  # for me because with model it's not working for me

    distances, indices = index.search(query_embedding, nb_neighbors)
    chunks_collection = db["chunks"]

    faiss_ids = np.array(indices).flatten()[:4]

    results = [
        chunks_collection.find_one({"faiss_id": int(faiss_id)})
        for faiss_id in faiss_ids
    ]

    return results
