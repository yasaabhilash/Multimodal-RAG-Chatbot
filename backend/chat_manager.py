import os
import json
import shutil
import time

ACTIVE_DIR = "chat_sessions/active"
ARCHIVED_DIR = "chat_sessions/archived"

os.makedirs(ACTIVE_DIR, exist_ok=True)
os.makedirs(ARCHIVED_DIR, exist_ok=True)


def create_chat():

    chat_id = str(time.time_ns())

    data = {
        "id": chat_id,
        "title": "New Chat",
        "messages": []
    }

    with open(
        f"{ACTIVE_DIR}/{chat_id}.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )

    return data


def load_chats():

    active = []
    archived = []

    for file in os.listdir(ACTIVE_DIR):

        try:

            with open(
                os.path.join(
                    ACTIVE_DIR,
                    file
                ),
                "r",
                encoding="utf-8"
            ) as f:

                active.append(
                    json.load(f)
                )

        except:
            pass

    for file in os.listdir(ARCHIVED_DIR):

        try:

            with open(
                os.path.join(
                    ARCHIVED_DIR,
                    file
                ),
                "r",
                encoding="utf-8"
            ) as f:

                archived.append(
                    json.load(f)
                )

        except:
            pass

    return {
        "active": active,
        "archived": archived
    }


def save_chat(
    chat_id,
    messages
):

    path = f"{ACTIVE_DIR}/{chat_id}.json"

    if not os.path.exists(path):
        return

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    data["messages"] = messages

    if (
        data["title"] == "New Chat"
        and len(messages) > 0
    ):

        data["title"] = messages[0]["text"][:40]

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def rename_chat(
    chat_id,
    title
):

    path = f"{ACTIVE_DIR}/{chat_id}.json"

    if not os.path.exists(path):
        return

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    data["title"] = title

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2
        )


def archive_chat(chat_id):

    source = f"{ACTIVE_DIR}/{chat_id}.json"

    target = f"{ARCHIVED_DIR}/{chat_id}.json"

    if os.path.exists(source):

        shutil.move(
            source,
            target
        )


def unarchive_chat(chat_id):

    source = f"{ARCHIVED_DIR}/{chat_id}.json"

    target = f"{ACTIVE_DIR}/{chat_id}.json"

    if os.path.exists(source):

        shutil.move(
            source,
            target
        )


def delete_chat(
    chat_id,
    archived=False
):

    folder = (
        ARCHIVED_DIR
        if archived
        else ACTIVE_DIR
    )

    path = f"{folder}/{chat_id}.json"

    if os.path.exists(path):

        os.remove(path)