from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from concurrent.futures import ProcessPoolExecutor
import asyncio
import uuid
import time
import os
from typing import Dict, List, Any, Optional

app = FastAPI(title="Parallel Processing Backend")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict later)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CPU_WORKERS = max(1, (os.cpu_count() or 1) - 1)
process_pool: Optional[ProcessPoolExecutor] = None
jobs: Dict[str, Dict[str, Any]] = {}
jobs_lock = asyncio.Lock()

class SubmitPayload(BaseModel):
    numbers: List[int]

def cpu_heavy_task(n: int) -> int:
    if n < 2:
        return n
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def simulated_large_computation(numbers: List[int]) -> Dict[int, int]:
    results = {}
    for num in numbers:
        results[num] = cpu_heavy_task(num % 35)
    return results

@app.on_event("startup")
async def on_startup():
    global process_pool
    process_pool = ProcessPoolExecutor(max_workers=CPU_WORKERS)

@app.on_event("shutdown")
async def on_shutdown():
    global process_pool
    if process_pool:
        process_pool.shutdown(wait=False)
        process_pool = None

@app.post("/submit")
async def submit_job(payload: SubmitPayload):
    if not payload.numbers:
        raise HTTPException(status_code=400, detail="numbers must be a non-empty list")
    if process_pool is None:
        raise HTTPException(status_code=503, detail="Server not ready")

    job_id = str(uuid.uuid4())
    async with jobs_lock:
        jobs[job_id] = {"status": "queued", "submitted_at": time.time()}

    def on_done(fut):
        try:
            result = fut.result()
            jobs[job_id]["status"] = "finished"
            jobs[job_id]["result"] = result
            jobs[job_id]["finished_at"] = time.time()
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)

    future = process_pool.submit(simulated_large_computation, payload.numbers)
    future.add_done_callback(on_done)
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.get("status") != "finished":
        return {"status": job.get("status")}
    return {"result": job.get("result")}

@app.get("/health")
async def health_check():
    return {"status": "ok", "cpu_workers": CPU_WORKERS}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_parallel_backend:app", host="127.0.0.1", port=8000, reload=True)
