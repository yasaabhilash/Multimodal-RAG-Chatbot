from fastapi import FastAPI
from fastapi import UploadFile, File
from fastapi import Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.upload_service import UploadService

import shutil
import os

from rag import (
    ask_question,
    rebuild_vector_db
)

from chat_manager import (
    create_chat,
    load_chats,
    rename_chat,
    archive_chat,
    delete_chat,
    save_chat,
    unarchive_chat
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================
# MODELS
# =====================================

class Question(BaseModel):
    question: str
    history: list = []


class RenameRequest(BaseModel):
    title: str


class SaveChatRequest(BaseModel):
    chat_id: str
    messages: list


# =====================================
# BASIC ROUTES
# =====================================

@app.get("/")
def home():

    return {
        "message": "RAG Backend Running"
    }


@app.post("/chat")
def chat(data: Question):

    return ask_question(
        data.question,
        data.history
    )


# =====================================
# CHAT MANAGEMENT
# =====================================

@app.get("/chats")
def get_chats():

    return load_chats()


@app.post("/chat/create")
def create_chat_endpoint():

    return create_chat()


@app.post("/chat/save")
def save_chat_endpoint(
    data: SaveChatRequest
):

    save_chat(
        data.chat_id,
        data.messages
    )

    return {
        "success": True
    }


@app.put("/chat/{chat_id}/rename")
def rename_chat_endpoint(
    chat_id: str,
    data: RenameRequest
):

    rename_chat(
        chat_id,
        data.title
    )

    return {
        "success": True
    }


@app.post("/chat/{chat_id}/archive")
def archive_chat_endpoint(
    chat_id: str
):

    archive_chat(chat_id)

    return {
        "success": True
    }


@app.post("/chat/{chat_id}/unarchive")
def unarchive_chat_endpoint(
    chat_id: str
):

    unarchive_chat(chat_id)

    return {
        "success": True
    }


@app.delete("/chat/{chat_id}")
def delete_chat_endpoint(
    chat_id: str,
    archived: bool = Query(False)
):

    delete_chat(
        chat_id,
        archived
    )

    return {
        "success": True
    }


# =====================================
# FILE UPLOAD
# =====================================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    try:

        uploader = UploadService()

        result = uploader.upload(file)

        print()

        print("Uploaded")

        print(result)

        print()

        print("Rebuilding Vector Database...")

        rebuild_vector_db()

        return {

            "message": "Upload Successful",

            "file": result

        }

    except Exception as e:

        print(e)

        return {

            "message": str(e)

        }