from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uuid
from typing import Dict, Optional
from datetime import datetime
from graph.graph_builder import app as graph_app

app = FastAPI(title="Startup Idea Evaluator")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- MODELS --------------------
class IdeaRequest(BaseModel):
    raw_idea: str

class IdeaResponse(BaseModel):
    final_score: float
    metric_scores: dict
    swot_analysis: dict

class JobStatus(BaseModel):
    job_id: str
    status: str  # "pending", "processing", "completed", "failed"
    result: Optional[IdeaResponse] = None
    error: Optional[str] = None
    created_at: str

# -------------------- GLOBAL STATE --------------------
# Store job results in memory (consider Redis for production)
jobs: Dict[str, JobStatus] = {}

# Limit concurrent evaluations
evaluation_semaphore = asyncio.Semaphore(2)  # Allow 2 concurrent evaluations

# -------------------- WARMUP --------------------
@app.on_event("startup")
async def startup_event():
    """Warm up the graph to avoid cold start on first request"""
    try:
        print("🔥 Warming up LLM graph...")
        await asyncio.to_thread(
            graph_app.invoke,
            {"raw_idea": "test startup idea"}
        )
        print("✅ Warmup complete")
    except Exception as e:
        print(f"⚠️ Warmup failed (non-critical): {e}")

# -------------------- BACKGROUND PROCESSOR --------------------
async def process_evaluation(job_id: str, raw_idea: str):
    """Background task to process evaluation"""
    jobs[job_id].status = "processing"
    
    async with evaluation_semaphore:
        try:
            final_state = await asyncio.to_thread(
                graph_app.invoke,
                {"raw_idea": raw_idea}
            )
            
            jobs[job_id].result = IdeaResponse(
                final_score=float(final_state.get("final_score", 0)),
                metric_scores=final_state.get("metric_scores", {}),
                swot_analysis=final_state.get("swot_analysis", {})
            )
            jobs[job_id].status = "completed"
            
        except Exception as e:
            print(f"❌ Evaluation error for {job_id}:", e)
            jobs[job_id].status = "failed"
            jobs[job_id].error = str(e)

# -------------------- ENDPOINTS --------------------

@app.post("/evaluate/async")
async def evaluate_async(request: IdeaRequest, background_tasks: BackgroundTasks):
    """Submit evaluation job (returns immediately)"""
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = JobStatus(
        job_id=job_id,
        status="pending",
        created_at=datetime.utcnow().isoformat()
    )
    
    background_tasks.add_task(process_evaluation, job_id, request.raw_idea)
    
    return {"job_id": job_id, "status": "pending"}

@app.get("/evaluate/status/{job_id}")
async def get_status(job_id: str):
    """Check status of evaluation job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]

@app.post("/evaluate", response_model=IdeaResponse)
async def evaluate_sync(request: IdeaRequest):
    """Synchronous evaluation (blocks until complete)"""
    async with evaluation_semaphore:
        try:
            final_state = await asyncio.to_thread(
                graph_app.invoke,
                {"raw_idea": request.raw_idea}
            )
            
            return IdeaResponse(
                final_score=float(final_state.get("final_score", 0)),
                metric_scores=final_state.get("metric_scores", {}),
                swot_analysis=final_state.get("swot_analysis", {})
            )
        except Exception as e:
            print("❌ Evaluation error:", e)
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "active_jobs": len([j for j in jobs.values() if j.status == "processing"]),
        "pending_jobs": len([j for j in jobs.values() if j.status == "pending"])
    }

@app.delete("/jobs/{job_id}")
async def cleanup_job(job_id: str):
    """Clean up completed job"""
    if job_id in jobs:
        del jobs[job_id]
        return {"message": "Job deleted"}
    raise HTTPException(status_code=404, detail="Job not found")