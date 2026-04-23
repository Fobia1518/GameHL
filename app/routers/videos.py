import uuid
import shutil
import os
import subprocess
from fastapi import APIRouter, UploadFile, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Job
from app.pipeline.orchestrator import run_pipeline

router = APIRouter()

@router.post("/upload")
async def upload_video(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job_id = str(uuid.uuid4())
    os.makedirs("storage/uploads", exist_ok=True)
    dest = f"storage/uploads/{job_id}_{file.filename}"

    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    job = Job(id=job_id, status="queued", input_path=dest)
    db.add(job)
    db.commit()

    background_tasks.add_task(run_pipeline, job_id, dest)

    return {"job_id": job_id, "status": "queued"}


@router.get("/status/{job_id}")
def get_status(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    return {
        "job_id": job.id,
        "status": job.status,
        "progress": job.progress,
        "output": job.output_path,
        "error": job.error
    }


@router.get("/download/{job_id}")
def download_video(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    if job.status != "done":
        raise HTTPException(status_code=400, detail="El video aún no está listo")
    if not os.path.exists(job.output_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    return FileResponse(
        path=job.output_path,
        media_type="video/mp4",
        filename=f"highlights_{job_id}.mp4"
    )

@router.get("/download/{job_id}/vertical-gameplay")
def download_vertical_gameplay(job_id: str, db: Session = Depends(get_db)):
    """9:16 solo con gameplay, zoom al centro"""
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    if job.status != "done":
        raise HTTPException(status_code=400, detail="El video aún no está listo")

    output_path = job.output_path.replace("_highlights.mp4", "_vertical_gameplay.mp4")

    if not os.path.exists(output_path):
        subprocess.run([
            "ffmpeg", "-y",
            "-i", job.output_path,
            "-vf", (
                "scale=-1:1920,"
                "crop=1080:1920:(iw-1080)/2:(ih-1920)/2,"
                "setsar=1,"
                "fps=60"
            ),
            "-r", "60",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "slow",
            "-c:a", "aac",
            "-b:a", "192k",
            output_path
        ], check=True)

    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=f"highlights_{job_id}_vertical_gameplay.mp4"
    )
 
@router.get("/clip/{clip_id}")
def download_clip(clip_id: str, db: Session = Depends(get_db)):
    from app.models.job import Clip
    clip = db.get(Clip, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip no encontrado")
    if not os.path.exists(clip.path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(
        path=clip.path,
        media_type="video/mp4",
        filename=f"clip_{clip_id}.mp4"
    )