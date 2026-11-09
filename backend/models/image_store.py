import json
import os


class ImageStore:

    FILE = "metadata/images.json"

    def __init__(self):

        os.makedirs("metadata", exist_ok=True)

        if not os.path.exists(self.FILE):

            with open(self.FILE, "w", encoding="utf-8") as f:

                json.dump([], f, indent=4)

    def load(self):

        with open(self.FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    def save(self, data):

        with open(self.FILE, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_image(self, filename, path):

        data = self.load()

        data.append({

            "filename": filename,

            "path": os.path.abspath(path)

        })

        self.save(data)

    def latest_image(self):

        data = self.load()

        if len(data) == 0:

            return None

        return data[-1]