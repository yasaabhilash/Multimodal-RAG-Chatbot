import os

from services.vision_service import VisionService

vision = VisionService()

image = "images/uploaded/download.jpeg"      # <-- use JPG or PNG

print(os.getcwd())

print(os.path.abspath(image))

print(os.path.exists(image))

print()

print("Generating description...\n")

answer = vision.describe_image(image)

print(answer)