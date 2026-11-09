from models.image_store import ImageStore


class ImageQueryService:

    def __init__(self):

        self.store = ImageStore()

    def has_image_question(

        self,

        question

    ):

        question = question.lower()

        keywords = [

            "image",

            "picture",

            "photo",

            "describe",

            "person",

            "people",

            "man",

            "woman",

            "child",

            "bike",

            "car",

            "road",

            "tree",

            "sky",

            "animal",

            "dog",

            "cat",

            "color",

            "wearing",

            "doing",

            "holding",

            "standing",

            "sitting",

            "behind",

            "next to",

            "left",

            "right",

            "front",

            "background"

        ]

        return any(

            keyword in question

            for keyword in keywords

        )

    def latest_image(self):

        return self.store.latest_image()