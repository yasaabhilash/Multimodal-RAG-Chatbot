import os
import shutil
import uuid

from models.document_store import DocumentStore
from models.image_store import ImageStore

from services.image_service import ImageService


class UploadService:

    IMAGE_EXTENSIONS = (
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".webp",
        ".heic"
    )

    DOCUMENT_FOLDERS = {
        ".pdf": "documents/pdf",
        ".docx": "documents/docx",
        ".txt": "documents/txt",
        ".csv": "documents/csv",
        ".xlsx": "documents/xlsx"
    }

    IMAGE_FOLDER = "images/uploaded"

    def __init__(self):

        os.makedirs(self.IMAGE_FOLDER, exist_ok=True)

        for folder in self.DOCUMENT_FOLDERS.values():
            os.makedirs(folder, exist_ok=True)

        self.image_service = ImageService()
        self.image_store = ImageStore()
        self.document_store = DocumentStore()

    def upload(self, upload_file):

        original_filename = upload_file.filename

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        # ==========================================
        # IMAGE
        # ==========================================

        if extension in self.IMAGE_EXTENSIONS:

            unique_filename = f"{uuid.uuid4().hex}{extension}"

            save_path = os.path.join(
                self.IMAGE_FOLDER,
                unique_filename
            )

            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(
                    upload_file.file,
                    buffer
                )

            print("\n===================================")
            print("IMAGE SAVED")
            print("Original :", original_filename)
            print("Saved As :", unique_filename)
            print("Path     :", os.path.abspath(save_path))
            print("===================================\n")

            image_info = self.image_service.process_image(
                save_path
            )

            

            self.image_store.add_image(
                filename=unique_filename,
                path=save_path,
                
            )

            return {
                "type": "image",
                "filename": unique_filename,
                "path": save_path,
                "metadata": image_info
            }

        # ==========================================
        # DOCUMENT
        # ==========================================

        if extension in self.DOCUMENT_FOLDERS:

            folder = self.DOCUMENT_FOLDERS[
                extension
            ]

            unique_filename = f"{uuid.uuid4().hex}{extension}"

            save_path = os.path.join(
                folder,
                unique_filename
            )

            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(
                    upload_file.file,
                    buffer
                )

            self.document_store.add_document(
                filename=unique_filename,
                path=save_path,
                filetype=extension
            )

            return {
                "type": "document",
                "filename": unique_filename,
                "path": save_path
            }

        raise Exception(
            f"Unsupported file type: {extension}"
        )