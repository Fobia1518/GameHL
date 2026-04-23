from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.job import Clip
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    label: str  # "highlight" o "no_highlight"

@router.post("/{clip_id}")
def submit_feedback(
    clip_id: str,
    feedback: FeedbackRequest,
    db: Session = Depends(get_db)
):
    if feedback.label not in ["highlight", "no_highlight"]:
        raise HTTPException(
            status_code=400,
            detail="Label debe ser 'highlight' o 'no_highlight'"
        )

    clip = db.get(Clip, clip_id)
    if not clip:
        raise HTTPException(status_code=404, detail="Clip no encontrado")

    clip.label = feedback.label
    db.commit()

    # Contar clips etiquetados
    labeled_count = db.query(Clip).filter(Clip.label != None).count()

    return {
        "clip_id": clip_id,
        "label": feedback.label,
        "total_labeled": labeled_count,
        "message": "Feedback guardado correctamente"
    }

@router.get("/clips/{job_id}")
def get_clips(job_id: str, db: Session = Depends(get_db)):
    clips = db.query(Clip).filter(Clip.job_id == job_id).all()
    if not clips:
        raise HTTPException(status_code=404, detail="No se encontraron clips")

    return [
        {
            "clip_id": c.id,
            "timestamp": c.timestamp,
            "path": c.path,
            "label": c.label
        }
        for c in clips
    ]