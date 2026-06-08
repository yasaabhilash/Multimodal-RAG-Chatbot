from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
from pathlib import Path
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chatbot API")

# Import the RagService
from path.to.backend.services.rag_service import RagService

# Initialize the RAG service
rag_service = RagService()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload multiple files for processing"""
    try:
        file_paths = []
        for file in files:
            # Create uploads directory if it doesn't exist
            os.makedirs("uploads", exist_ok=True)
            
            # Save file
            file_path = f"uploads/{file.filename}"
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            file_paths.append(file_path)
        
        # Process files with RAG service
        rag_service.process_documents(file_paths)
        
        return JSONResponse(
            status_code=200,
            content={"message": f"Successfully processed {len(files)} files"}
        )
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/query")
async def query_rag(query: str = Form(...)):
    """Query the RAG system"""
    try:
        response = rag_service.query(query)
        return JSONResponse(
            status_code=200,
            content={"response": response}
        )
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
