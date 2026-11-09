import os

from services.vision_service import VisionService

from image_processor import (
    extract_text_from_image
)


class ImageService:

    def __init__(self):

        self.vision = VisionService()

    def process_image(

        self,

        image_path

    ):

        filename = os.path.basename(
            image_path
        )

        print()

        print("Generating image description...")

        description = self.vision.describe_image(
            image_path
        )

        print("Description Generated.")

        ocr = extract_text_from_image(
            image_path
        )

        return {

            "filename": filename,

            "path": image_path,

            "description": description,

            "ocr": ocr

        }