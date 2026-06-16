import cv2
import mediapipe as mp
import serial
import time

# =====================
# SERIAL
# =====================
ser = serial.Serial('COM15', 115200, timeout=1)
time.sleep(2)

# =====================
# MEDIAPIPE
# =====================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    data = [0,0,0,0,0,0]

    # koordinat default
    finger_xyz = {
        "thumb": (0,0,0),
        "index": (0,0,0),
        "middle": (0,0,0),
        "ring": (0,0,0),
        "pinky": (0,0,0)
    }

    jumlah_keypoint = 0

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]

        # gambar skeleton
        mp_drawing.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        lm = hand.landmark
        jumlah_keypoint = len(lm)  # harusnya 21

        # =====================
        # DETEKSI JARI
        # =====================
        data[0] = 1 if lm[4].x < lm[3].x else 0
        data[1] = 1 if abs(lm[4].x - lm[8].x) < 0.05 else 0
        data[2] = 1 if lm[8].y < lm[6].y else 0
        data[3] = 1 if lm[12].y < lm[10].y else 0
        data[4] = 1 if lm[16].y < lm[14].y else 0
        data[5] = 1 if lm[20].y < lm[18].y else 0

        # =====================
        # KOORDINAT TIAP JARI (UJUNG)
        # =====================
        finger_xyz["thumb"]  = (lm[4].x,  lm[4].y,  lm[4].z)
        finger_xyz["index"]  = (lm[8].x,  lm[8].y,  lm[8].z)
        finger_xyz["middle"] = (lm[12].x, lm[12].y, lm[12].z)
        finger_xyz["ring"]   = (lm[16].x, lm[16].y, lm[16].z)
        finger_xyz["pinky"]  = (lm[20].x, lm[20].y, lm[20].z)

        # =====================
        # GAMBAR TITIK + INDEX
        # =====================
        h, w, _ = frame.shape

        for i, point in enumerate(lm):
            cx, cy = int(point.x * w), int(point.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, str(i), (cx+5, cy-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

    # =====================
    # KIRIM KE ARDUINO
    # =====================
    kirim = "{},{},{},{},{},{}\n".format(*data)

    try:
        ser.write(kirim.encode())
    except:
        print("Serial error!")

    # =====================
    # PRINT DATA
    # =====================
    print("Jari:", data)
    print("Jumlah keypoint:", jumlah_keypoint)

    for jari, (x,y,z) in finger_xyz.items():
        print(f"{jari}: X={x:.2f}, Y={y:.2f}, Z={z:.2f}")

    print("---------------------------")

    # =====================
    # TAMPILKAN DI LAYAR
    # =====================
    cv2.putText(frame, f"Keypoint: {jumlah_keypoint}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    y_offset = 60
    for jari, (x,y,z) in finger_xyz.items():
        text = f"{jari}: {x:.2f},{y:.2f},{z:.2f}"
        cv2.putText(frame, text, (10,y_offset),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        y_offset += 20

    cv2.imshow("Hand Tracking + XYZ Lengkap", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.05)

cap.release()
ser.close()
cv2.destroyAllWindows()