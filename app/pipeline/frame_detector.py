import cv2
import numpy as np

def detect_highlight_events(video_path: str) -> list[float]:
    """
    Detecta momentos de highlight en CS2 usando solo OpenCV:
    - Kill feed: detecta el color naranja-rojizo del nombre propio
    - Flashbang: pantalla con brillo extremo repentino
    - Accion intensa: cambio brusco entre frames
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 60
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    events = []
    prev_gray        = None
    prev_brightness  = None
    frame_idx        = 0
    last_event_frame = -999

    cooldown_frames = int(fps * 8)  # 8 segundos de cooldown entre eventos

    # Zona kill feed: esquina superior derecha
    kf_x = int(width * 0.68)
    kf_y = int(height * 0.02)
    kf_w = width - kf_x
    kf_h = int(height * 0.35)

    def add_event(ts):
        nonlocal last_event_frame
        if frame_idx - last_event_frame >= cooldown_frames:
            events.append(round(ts, 2))
            last_event_frame = frame_idx

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ts = frame_idx / fps

        # Analizar 1 de cada 3 frames para mayor velocidad
        if frame_idx % 3 == 0:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # --- Detector 1: Kill feed ---
            kill_zone = frame[kf_y:kf_y + kf_h, kf_x:kf_x + kf_w]
            hsv = cv2.cvtColor(kill_zone, cv2.COLOR_BGR2HSV)

            # Naranja rojizo exacto del nombre en CS2
            lower = np.array([5,  180, 180])
            upper = np.array([18, 255, 255])
            mask  = cv2.inRange(hsv, lower, upper)
            kill_pixels = cv2.countNonZero(mask)

            if kill_pixels > 40:
                add_event(ts)

            # --- Detector 2: Flashbang ---
            brightness = float(np.mean(gray))
            if prev_brightness is not None:
                jump = brightness - prev_brightness
                if jump > 55 and brightness > 175:
                    add_event(ts)
            prev_brightness = brightness

            # --- Detector 3: Accion intensa ---
            if prev_gray is not None:
                diff  = cv2.absdiff(prev_gray, gray)
                score = float(np.mean(diff))
                if score > 50:
                    add_event(ts)

            prev_gray = gray

        frame_idx += 1

    cap.release()
    return sorted(events)