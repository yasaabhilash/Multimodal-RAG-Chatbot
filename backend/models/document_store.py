import json
import os
import uuid
from datetime import datetime


STORE_PATH = "metadata/document_store.json"


class DocumentStore:

    def __init__(self):

        os.makedirs(
            "metadata",
            exist_ok=True
        )

        if not os.path.exists(STORE_PATH):

            with open(
                STORE_PATH,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    [],
                    f,
                    indent=4
                )

    def load(self):

        with open(
            STORE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def save(
        self,
        data
    ):

        with open(
            STORE_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def add_document(

        self,

        filename,

        path,

        filetype

    ):

        data = self.load()

        document = {

            "id": str(uuid.uuid4()),

            "filename": filename,

            "path": path,

            "type": filetype,

            "uploaded_at": str(
                datetime.now()
            )

        }

        data.append(document)

        self.save(data)

        return document

    def latest(self):

        data = self.load()

        if len(data) == 0:

            return None

        return data[-1]