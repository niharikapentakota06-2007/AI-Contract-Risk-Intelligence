import uuid
import asyncio
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Contract Processing API",
    description="API for document upload, async inference, and vector search metadata retrieval",
    version="1.0.0"
)

# In-memory storage for tracking asynchronous task execution status
tasks_db = {}

class MetadataResponse(BaseModel):
    task_id: str
    filename: str
    status: str
    extracted_metadata: dict | None = None


def async_inference_pipeline(task_id: str, filename: str, content: bytes):
    """
    Simulates asynchronous inference task (e.g., CUAD legal clause extraction / embedding generation).
    """
    try:
        tasks_db[task_id]["status"] = "processing"
        
        # Simulate ML model processing delay
        import time
        time.sleep(3)  
        
        # Extracted mock metadata from the model
        extracted_info = {
            "document_name": filename,
            "char_count": len(content),
            "detected_clauses": ["Confidentiality", "Governing Law"],
            "risk_score": "Low"
        }

        tasks_db[task_id]["status"] = "completed"
        tasks_db[task_id]["extracted_metadata"] = extracted_info

    except Exception as e:
        tasks_db[task_id]["status"] = "failed"
        tasks_db[task_id]["error"] = str(e)


@app.post("/upload", response_model=dict)
async def upload_document(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    """
    Endpoint to handle document uploads and trigger asynchronous inference tasks.
    """
    if not file.filename.endswith(('.pdf', '.txt', '.docx')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, TXT, or DOCX allowed.")

    task_id = str(uuid.uuid4())
    content = await file.read()

    tasks_db[task_id] = {
        "filename": file.filename,
        "status": "queued",
        "extracted_metadata": None
    }

    # Trigger async background task for model processing
    background_tasks.add_task(async_inference_pipeline, task_id, file.filename, content)

    return {
        "message": "File uploaded successfully. Inference task initiated.",
        "task_id": task_id,
        "status": "queued"
    }


@app.get("/tasks/{task_id}", response_model=MetadataResponse)
async def get_task_metadata(task_id: str):
    """
    Endpoint to serve extracted metadata and status for a given task ID.
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task ID not found.")

    task_info = tasks_db[task_id]
    return MetadataResponse(
        task_id=task_id,
        filename=task_info["filename"],
        status=task_info["status"],
        extracted_metadata=task_info.get("extracted_metadata")
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
