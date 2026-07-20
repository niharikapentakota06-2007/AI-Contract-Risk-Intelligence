import logging
import uuid
import time
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- LOGGING SETUP (Day 6-7 Requirement) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)
logger = logging.getLogger("ProductionAPI")

# --- FASTAPI APP WITH SWAGGER METADATA (Day 4-5 Requirement) ---
app = FastAPI(
    title="Legal Contract Analytics Engine",
    description=(
        "Production-grade API for contract metadata extraction, clause tagging, "
        "and semantic vector database indexing."
    ),
    version="1.0.0",
    docs_url="/docs",      # Interactive Swagger UI
    redoc_url="/redoc"     # Alternative documentation view
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks_db = {}

class TaskResponse(BaseModel):
    task_id: str
    status: str
    filename: str
    extracted_metadata: dict | None = None

def run_async_inference(task_id: str, filename: str):
    """Simulates background ML pipeline with structured logging."""
    logger.info(f"Started asynchronous inference task: {task_id} for file: {filename}")
    try:
        tasks_db[task_id]["status"] = "processing"
        time.sleep(2)  # Simulate processing pipeline
        
        tasks_db[task_id]["extracted_metadata"] = {
            "file_name": filename,
            "highlighted_clauses": [
                {"type": "Confidentiality", "risk": "Low", "text": "Parties agree to non-disclosure."},
                {"type": "Indemnification", "risk": "Medium", "text": "Contractor shall indemnify liabilities."}
            ],
            "processing_time_sec": 2.0
        }
        tasks_db[task_id]["status"] = "completed"
        logger.info(f"Task {task_id} completed successfully.")
    except Exception as e:
        tasks_db[task_id]["status"] = "failed"
        logger.error(f"Task {task_id} failed with error: {str(e)}")

@app.get("/health", tags=["System"])
async def health_check():
    """Health status check for load balancers and Docker container monitoring."""
    return {"status": "healthy", "service": "Contract API", "timestamp": time.time()}

@app.post("/upload", response_model=dict, tags=["Inference"])
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Upload legal contract documents for asynchronous ML analysis."""
    if not file.filename.endswith(('.pdf', '.txt', '.docx')):
        logger.warning(f"Rejected upload for unsupported file: {file.filename}")
        raise HTTPException(status_code=400, detail="Unsupported file format.")

    task_id = str(uuid.uuid4())
    tasks_db[task_id] = {
        "filename": file.filename,
        "status": "queued",
        "extracted_metadata": None
    }
    
    logger.info(f"Received document: {file.filename}. Assigned Task ID: {task_id}")
    background_tasks.add_task(run_async_inference, task_id, file.filename)
    
    return {"task_id": task_id, "status": "queued", "message": "Inference task scheduled successfully."}

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Inference"])
async def get_task_results(task_id: str):
    """Fetch status and extracted contract highlights for a given task ID."""
    if task_id not in tasks_db:
        logger.warning(f"Metadata requested for non-existent task ID: {task_id}")
        raise HTTPException(status_code=404, detail="Task not found.")
    
    return TaskResponse(
        task_id=task_id,
        status=tasks_db[task_id]["status"],
        filename=tasks_db[task_id]["filename"],
        extracted_metadata=tasks_db[task_id]["extracted_metadata"]
    )
