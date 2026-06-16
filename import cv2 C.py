import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt

mqttbroker = "mqtt-dashboard.com"

client = mqtt.Client()
client.connect(mqttbroker)

kirim = "tangan_kanan"

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()

while True:
    success, img = cap.read()

    if not success:
        print("kamera tidak terbaca")
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        client.publish(kirim, payload="ada tangan")
        print("ada tangan")
    else:
        client.publish(kirim, payload="tidak ada tangan")
        print("tidak ada tangan")

    cv2.imshow("camera", img)

    if cv2.waitKey(1) & 0xFF == 27:   # tekan ESC untuk keluar
        break

cap.release()
cv2.destroyAllWindows()