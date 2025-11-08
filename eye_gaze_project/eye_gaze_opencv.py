import cv2
import numpy as np
import pyautogui

# Start webcam using DirectShow backend
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
screen_w, screen_h = pyautogui.size()

if not cap.isOpened():
    print("❌ Could not open camera.")
    exit()

print("✅ Eye gaze tracker started (with preview). Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Warning: Unable to read frame from camera.")
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes
    eyes = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
    detected_eyes = eyes.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in detected_eyes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        eye_center_x = x + w // 2
        eye_center_y = y + h // 2

        # Rough mapping from eye center to screen coordinates
        screen_x = np.interp(eye_center_x, [0, frame.shape[1]], [0, screen_w])
        screen_y = np.interp(eye_center_y, [0, frame.shape[0]], [0, screen_h])

        pyautogui.moveTo(screen_x, screen_y, duration=0.1)

    cv2.imshow("Eye Gaze Tracking (Press Q to Quit)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Stopped by user.")
        break

cap.release()
cv2.destroyAllWindows()
