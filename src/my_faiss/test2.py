import faiss
import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

username = "admin"
password = "admin123"

uri = f"mongodb://{username}:{password}@localhost:27017/faiss_db?authSource=admin"
client = MongoClient(uri)

db = client["faiss_db"]

# Load the Faiss index
index = faiss.read_index("index.faiss")

# Define your query text
query_text = "what is printf?"

# Generate the embedding for the query text
query_embedding = model.encode([query_text]).astype(np.float32)

# Number of nearest neighbors to retrieve
k = 5  # Adjust as needed

# Perform the search
distances, indices = index.search(query_embedding, k)

# Retrieve and print the results with metadata from MongoDB
chunks_collection = db["chunks"]
print("Top {} nearest neighbors:".format(k))
for i in range(k):
    faiss_id = indices[0][i]

    # Retrieve metadata for the result chunk using faiss_id
    result = chunks_collection.find_one({"faiss_id": int(faiss_id)})  # Ensure faiss_id is an integer
    if result:
        print(f"Result {i+1}:")
        print(f"File: {result['file_name']}, Chunk: {result['file_hash']}")
        print(f"Text: {result['text']}")
        print(f"Distance: {distances[0][i]}\n")
