from langchain_community.vectorstores import FAISS
from typing import Optional
from langchain.docstore.document import Document


class Retriever:
    def __init__(
        self,
        embedding_model,
        text_splitter,
        vector_store_path: str,
        documents: Optional[list[Document]] = None,
    ):
        self.embedding_model = embedding_model
        self.text_splitter = text_splitter
        self.vector_store_path = vector_store_path
        if documents is None:
            self.vector_store = self.load()
        else:
            self.vector_store = self.save(documents=documents)

    def load(self):
        print("Loading local FAISS VectorStore...")
        try:
            vector_store = FAISS.load_local(
                self.vector_store_path,
                embeddings=self.embedding_model,
                allow_dangerous_deserialization=True,
            )
            print("Loading successful !")
            return vector_store
        except RuntimeError:
            print("Could not load local FAISS VectorStore")

    def save(self, documents):
        splitted_docs = []
        print("Splitting into documents into chunks...")
        for doc in documents:
            splitted_docs += self.text_splitter.split_documents([doc])
        print("Creating FAISS VectorStore")
        vector_store = FAISS.from_documents(documents=splitted_docs, embedding=self.embedding_model)
        print("Saving local FAISS VectorStore...")
        vector_store.save_local(self.vector_store_path)
        print("Saving successful !")
        return vector_store
