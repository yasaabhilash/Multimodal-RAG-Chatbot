import os
from ollama import Client


class VisionService:

    def __init__(self):

        self.client = Client(
            host="http://localhost:11434"
        )

        self.model = "qwen2.5vl:7b"

    def describe_image(self, image_path: str) -> str:

        image_path = os.path.abspath(image_path)

        if not os.path.exists(image_path):
            raise FileNotFoundError(image_path)

        print("\n==============================")
        print("VISION MODEL")
        print("==============================")
        print("Image :", image_path)
        print()

        prompt = """
You are an expert computer vision model.

Describe EVERYTHING visible in this image.

Your answer must include:

- overall scene
- people
- objects
- vehicles
- animals
- buildings
- road
- sky
- weather
- colors
- actions
- positions
- clothing
- accessories
- facial expressions
- text
- foreground
- background
- small details

Be extremely detailed.

Never guess things that cannot actually be seen.
"""

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_path]
                }
            ]
        )

        print("Vision Complete\n")

        return response["message"]["content"].strip()

    def answer_question(
        self,
        image_path: str,
        question: str
    ) -> str:

        image_path = os.path.abspath(image_path)

        if not os.path.exists(image_path):
            raise FileNotFoundError(image_path)

        prompt = f"""
You are an expert image assistant.

Answer ONLY using the uploaded image.

If the answer cannot be determined from the image, reply exactly:

I cannot determine that from the image.

Question:

{question}
"""

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_path]
                }
            ]
        )

        return response["message"]["content"].strip()