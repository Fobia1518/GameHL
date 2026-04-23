import cv2
import numpy as np

def detect_highlight_events(video_path: str) -> list[float]:
    """
    Detecta highlights en CS2.
    Detecta la aparicion del kill feed: banda oscura semitransparente
    en la esquina superior derecha con texto blanco.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 60
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    events = []
    frame_idx        = 0
    last_event_frame = -999
    cooldown_frames  = int(fps * 8)

    # Zona kill feed: esquina superior derecha
    # En 1024x768: aprox x=630, y=5, ancho=390, alto=80
    kf_x = int(width * 0.72)
    kf_y = int(height * 0.01)
    kf_w = width - kf_x
    kf_h = int(height * 0.08)

    def add_event(ts, reason):
        nonlocal last_event_frame
        if frame_idx - last_event_frame >= cooldown_frames:
            print(f"[HIGHLIGHT] t={ts:.2f}s reason={reason}")
            events.append(round(ts, 2))
            last_event_frame = frame_idx

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ts = frame_idx / fps

        if frame_idx % 3 == 0:
            kill_zone = frame[kf_y:kf_y + kf_h, kf_x:kf_x + kf_w]
            gray = cv2.cvtColor(kill_zone, cv2.COLOR_BGR2GRAY)

            # El kill feed tiene fondo muy oscuro (casi negro)
            dark_pixels = cv2.countNonZero(cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)[1])
            total_pixels = kill_zone.shape[0] * kill_zone.shape[1]
            dark_ratio = dark_pixels / total_pixels

            # Y texto blanco encima
            white_pixels = cv2.countNonZero(cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1])
            white_ratio = white_pixels / total_pixels

            # Kill feed: mas del 40% oscuro y al menos 5% blanco (texto)
            if dark_ratio > 0.05 and white_ratio > 0.02:
                add_event(ts, "kill_feed")

        frame_idx += 1

    cap.release()
    return sorted(events)