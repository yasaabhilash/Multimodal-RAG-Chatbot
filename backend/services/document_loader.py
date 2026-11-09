import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    CSVLoader,
    UnstructuredExcelLoader
)

from langchain_core.documents import Document

from config import (
    DOCUMENT_FOLDER,
    IMAGE_EXTENSIONS
)

from image_processor import (
    extract_text_from_image,
    extract_text_from_pdf_images
)


class DocumentLoader:

    def __init__(self):

        os.makedirs(
            DOCUMENT_FOLDER,
            exist_ok=True
        )

    def load(self):

        documents = []

        # Walk through every subfolder
        for root, dirs, files in os.walk(
            DOCUMENT_FOLDER
        ):

            for file in files:

                path = os.path.join(
                    root,
                    file
                )

                extension = file.lower()

                try:

                    if extension.endswith(".pdf"):

                        documents.extend(

                            self.load_pdf(
                                path,
                                file
                            )

                        )

                    elif extension.endswith(".txt"):

                        documents.extend(

                            TextLoader(
                                path,
                                encoding="utf-8"
                            ).load()

                        )

                    elif extension.endswith(".docx"):

                        documents.extend(

                            Docx2txtLoader(
                                path
                            ).load()

                        )

                    elif extension.endswith(".csv"):

                        documents.extend(

                            CSVLoader(
                                path
                            ).load()

                        )

                    elif extension.endswith(".xlsx"):

                        documents.extend(

                            UnstructuredExcelLoader(
                                path
                            ).load()

                        )

                    elif extension.endswith(
                        IMAGE_EXTENSIONS
                    ):

                        image_doc = self.load_image(
                            path,
                            file
                        )

                        if image_doc:

                            documents.append(
                                image_doc
                            )

                except Exception as e:

                    print(
                        f"Failed loading {path}"
                    )

                    print(e)

        return documents

    def load_pdf(
        self,
        path,
        file
    ):

        documents = []

        loader = PyPDFLoader(path)

        documents.extend(
            loader.load()
        )

        ocr_text = (
            extract_text_from_pdf_images(
                path
            )
        )

        if ocr_text.strip():

            documents.append(

                Document(

                    page_content=ocr_text,

                    metadata={

                        "source": path,

                        "page": 0,

                        "type": "ocr_pdf"

                    }

                )

            )

        return documents

    def load_image(
        self,
        path,
        file
    ):

        text = extract_text_from_image(
            path
        )

        if not text.strip():

            return None

        return Document(

            page_content=text,

            metadata={

                "source": path,

                "page": 0,

                "type": "image"

            }

        )