from langchain_community.document_loaders import UnstructuredHTMLLoader

class RAG():
    def __init__(self, data_path: str) -> None:
        self.documents = []
        self.html_loader = UnstructuredHTMLLoader()
        

    def load_vector_store(self):
        documents = self.loader.load()
        return documents
