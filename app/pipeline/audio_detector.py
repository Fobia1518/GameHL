import librosa
import numpy as np

def detect_audio_peaks(video_path: str, threshold_db: float = -20.0) -> list[float]:
    """Retorna timestamps en segundos donde el audio supera el umbral."""
    y, sr = librosa.load(video_path, sr=None, mono=True)
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
    rms_db = librosa.amplitude_to_db(rms)
    times = librosa.frames_to_time(
        np.arange(len(rms_db)), sr=sr, hop_length=512
    )

    peaks = []
    for t, db in zip(times, rms_db):
        if db >= threshold_db:
            if not peaks or t - peaks[-1] > 1.0:
                peaks.append(float(t))

    return peaks