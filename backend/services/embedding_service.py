from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


class EmbeddingService:

    def __init__(self):

        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text"
        )

    def build_vector_db(self, documents):

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=150
        )

        chunks = splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks")

        db = FAISS.from_documents(
            chunks,
            self.embeddings
        )

        return db