import subprocess
import os

def extract_clip(input_path: str, timestamp: float, output_path: str,
                 before: float = 3.0, after: float = 5.0):
    """Extrae un clip alrededor del timestamp dado."""
    start    = max(0, timestamp - before)
    duration = (timestamp + after) - start  # ajusta duración si start fue recortado

    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(start),
        "-i", input_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "fast",
        "-avoid_negative_ts", "make_zero",  # evita timestamps negativos
        "-fflags", "+genpts",               # regenera timestamps limpios
        output_path
    ], check=True, capture_output=True)