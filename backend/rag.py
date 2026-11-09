from services.document_loader import DocumentLoader
from services.embedding_service import EmbeddingService
from services.retrieval_service import RetrievalService
from services.answer_service import AnswerService
from services.vision_service import VisionService
from models.image_store import ImageStore


db = None

answer_service = AnswerService()

vision = VisionService()

image_store = ImageStore()


def rebuild_vector_store():

    global db

    print("\nLoading documents...")

    loader = DocumentLoader()

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    if len(documents) == 0:

        db = None

        return

    embedding_service = EmbeddingService()

    db = embedding_service.build_vector_db(
        documents
    )

    print("Vector Database Ready")


def rebuild_vector_db():

    rebuild_vector_store()


rebuild_vector_store()


IMAGE_KEYWORDS = [

    "image",
    "picture",
    "photo",
    "this image",
    "this photo",
    "this picture",
    "bike",
    "car",
    "person",
    "man",
    "woman",
    "girl",
    "boy",
    "dog",
    "cat",
    "vehicle",
    "motorcycle",
    "helmet",
    "tree",
    "road",
    "building",
    "wearing",
    "holding",
    "standing",
    "sitting",
    "left",
    "right",
    "behind",
    "front"

]


def is_image_question(question):

    question = question.lower()

    return any(

        word in question

        for word in IMAGE_KEYWORDS

    )


def ask_question(question, history=None):

    global db

    if history is None:
        history = []

    print("\n==========================")
    print("QUESTION :", question)
    print("==========================")

    latest_image = image_store.latest_image()

    print("Latest Image :", latest_image)

    print("Image Question :", is_image_question(question))

    if latest_image is not None and is_image_question(question):

        print("\n>>>> USING VISION <<<<\n")

        answer = vision.answer_question(
            latest_image["path"],
            question
        )

        return {
            "answer": answer,
            "sources": [
                {
                    "file": latest_image["filename"],
                    "page": "Image"
                }
            ]
        }

    print("\n>>>> USING RAG <<<<\n")

    if db is None:

        return {
            "answer": "No documents available.",
            "sources": []
        }

    retrieval = RetrievalService(db)

    docs, _ = retrieval.retrieve(question, k=5)

    context = retrieval.build_context(docs)

    answer = answer_service.generate_answer(
        question,
        context,
        history
    )

    sources = retrieval.build_sources(docs)

    return {
        "answer": answer,
        "sources": sources
    }