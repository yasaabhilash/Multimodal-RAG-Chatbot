from fastapi import FastAPI, UploadFile, File, Form
import os
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chatbot API")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload multiple files for processing"""
    file_paths = [os.path.join("uploads", file.filename) for file in files]
    os.makedirs("uploads", exist_ok=True)
    
    for file, file_path in zip(files, file_paths):
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
    from path.to.backend.services.rag_service import RagService
    rag_service = RagService()
    rag_service.process_documents(file_paths)
    
    return {"message": f"Successfully processed {len(files)} files"}

@app.post("/query")
async def query_rag(query: str = Form(...)):
    """Query the RAG system"""
    from path.to.backend.services.rag_service import RagService
    rag_service = RagService()
    response = rag_service.query(query)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
