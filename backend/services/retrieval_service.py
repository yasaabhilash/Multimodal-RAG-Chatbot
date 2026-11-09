import os


class RetrievalService:

    def __init__(self, db):

        self.db = db

    def retrieve(
        self,
        question,
        k=5
    ):

        docs_with_scores = (
            self.db.similarity_search_with_score(
                question,
                k=k
            )
        )

        docs = [

            doc

            for doc, score

            in docs_with_scores

        ]

        return docs, docs_with_scores

    def build_context(
        self,
        docs
    ):

        context = []

        for doc in docs:

            context.append(
                doc.page_content[:1000]
            )

        return "\n\n".join(context)

    def build_sources(
        self,
        docs
    ):

        sources = []

        seen = set()

        for doc in docs:

            source = os.path.basename(

                doc.metadata.get(
                    "source",
                    "Unknown"
                )

            )

            page = doc.metadata.get(
                "page",
                None
            )

            page = (

                page + 1

                if page is not None

                else "Unknown"

            )

            key = (
                source,
                page
            )

            if key in seen:
                continue

            seen.add(key)

            sources.append({

                "file": source,

                "page": page

            })

        return sources