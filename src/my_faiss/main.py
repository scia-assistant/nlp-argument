import os

import faiss
from dotenv import load_dotenv
from pymongo import MongoClient

from faiss_utils import add_documents, search_neighbors

# Load environment variables from .env file
load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

data_path = "datas/"
index_path = "index.faiss"

uri = f"mongodb://{username}:{password}@localhost:27017/{db_name}?authSource=admin"

client = MongoClient(uri)

db = client[db_name]

# add all documents in folder data_path in the db and in the index
# you have to do this step only once, unless you have added documents to the foleder
add_documents(data_path, db, index_path, 30)

# search for result
results = search_neighbors(db, "what is printf", index_path, 5)

for result in results:
    print("-----")
    print(f"File: {result['file_name']}, Chunk: {result['file_hash']}")
    print(f"Text: {result['text']}")
    print("-----\n")
