import os
import uuid
from app.pipeline.audio_detector import detect_audio_peaks
from app.pipeline.frame_detector import detect_highlight_events
from app.pipeline.clip_extractor import extract_clip
from app.pipeline.renderer import merge_and_normalize
from app.database import SessionLocal
from app.models.job import Job, Clip

BEFORE = 3.0  # segundos antes del evento
AFTER  = 5.0  # segundos despues del evento

def merge_events(events: list[float], min_gap: float) -> list[float]:
    """Fusiona eventos que están muy cerca entre sí."""
    if not events:
        return []
    merged = [events[0]]
    for ts in events[1:]:
        if ts - merged[-1] >= min_gap:
            merged.append(ts)
    return merged

def remove_overlapping_clips(events: list[float], before: float, after: float) -> list[float]:
    """
    Elimina eventos cuyos clips se solapan con el anterior.
    Un clip va desde (ts - before) hasta (ts + after).
    Si el inicio del clip actual es menor que el fin del clip anterior, se solapan.
    """
    if not events:
        return []
    clean = [events[0]]
    for ts in events[1:]:
        prev_end   = clean[-1] + after
        curr_start = ts - before
        if curr_start >= prev_end:
            clean.append(ts)
    return clean

def run_pipeline(job_id: str, input_path: str):
    db = SessionLocal()
    job = db.get(Job, job_id)

    try:
        job.status   = "processing"
        job.progress = 10
        db.commit()

        # Detectar eventos
        audio_events     = detect_audio_peaks(input_path)
        highlight_events = detect_highlight_events(input_path)

        # Unir, ordenar y deduplicar
        all_events = sorted(set(audio_events + highlight_events))
        merged     = merge_events(all_events, min_gap=8.0)

        # Eliminar clips que se solapan en el tiempo
        clean_events = remove_overlapping_clips(merged, before=BEFORE, after=AFTER)

        job.progress = 40
        db.commit()

        # Extraer clips
        clips_dir = f"storage/clips/{job_id}"
        os.makedirs(clips_dir, exist_ok=True)
        clip_paths = []

        for i, ts in enumerate(clean_events[:20]):
            clip_path = f"{clips_dir}/clip_{i:03d}.mp4"
            extract_clip(input_path, ts, clip_path, before=BEFORE, after=AFTER)

            if not os.path.exists(clip_path):
                continue

            clip = Clip(
                id=str(uuid.uuid4()),
                job_id=job_id,
                path=clip_path,
                timestamp=ts,
                score=1.0
            )
            db.add(clip)
            clip_paths.append(clip_path)

        job.progress = 80
        db.commit()

        if not clip_paths:
            job.status = "error"
            job.error  = "No se detectaron highlights en el video"
            db.commit()
            return

        # Renderizar video final 1080p 60fps
        output_path = f"storage/outputs/{job_id}_highlights.mp4"
        merge_and_normalize(clip_paths, output_path)

        job.status      = "done"
        job.output_path = output_path
        job.progress    = 100

    except Exception as e:
        job.status = "error"
        job.error  = str(e)

    finally:
        db.commit()
        db.close()