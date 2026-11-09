from langchain_community.vectorstores import FAISS


class VectorDB:

    def __init__(self):

        self.db = None

    def build(self, chunks, embeddings):

        self.db = FAISS.from_documents(
            chunks,
            embeddings
        )

    def similarity_search(
        self,
        question,
        k=5
    ):

        if self.db is None:
            return []

        return self.db.similarity_search_with_score(
            question,
            k=k
        )