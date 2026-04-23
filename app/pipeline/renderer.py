import subprocess
import os

def merge_and_normalize(clip_paths: list[str], output_path: str):
    """Une todos los clips y normaliza a 1080p 60fps."""
    list_file = output_path + ".txt"

    with open(list_file, "w") as f:
        for p in clip_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-fflags", "+igndts",
        "-i", list_file,
        "-vf", (
            "scale=1920:1080:force_original_aspect_ratio=decrease,"
            "pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
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
    ], check=True, capture_output=True)

    os.remove(list_file)