import os

# ===========================
# Paths
# ===========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOCUMENT_FOLDER = os.path.join(
    BASE_DIR,
    "documents"
)

VECTOR_DB_FOLDER = os.path.join(
    BASE_DIR,
    "vector_db"
)

CHAT_FOLDER = os.path.join(
    BASE_DIR,
    "chat_sessions"
)

# ===========================
# Models
# ===========================

EMBEDDING_MODEL = "nomic-embed-text"

LLM_MODEL = "qwen2.5:7b"

# ===========================
# Chunking
# ===========================

CHUNK_SIZE = 700

CHUNK_OVERLAP = 150

# ===========================
# Retrieval
# ===========================

TOP_K = 5

# ===========================
# OCR
# ===========================

TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = (
    r"C:\poppler\Library\bin"
)

# ===========================
# Image Extensions
# ===========================

IMAGE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp",
    ".heic"
)

# ===========================
# Document Extensions
# ===========================

SUPPORTED_DOCUMENTS = (

    ".pdf",

    ".txt",

    ".docx",

    ".csv",

    ".xlsx"

)