import cv2
import dlib
import pyautogui
import imutils
from scipy.spatial import distance as dist
import numpy as np

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Eye aspect ratio function
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Constants
EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 3

# Eye landmarks
LEFT_EYE = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

COUNTER = 0

# Start webcam
cap = cv2.VideoCapture(0)
print("✅ Blink Clicker Started. Close both eyes to click. Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        continue  # Skip if frame not captured

    frame = imutils.resize(frame, width=640)
    # Make sure frame is uint8
    if frame.dtype != np.uint8:
        frame = frame.astype(np.uint8)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = gray.astype(np.uint8)  # Ensure 8-bit gray

    rects = detector(gray, 0)

    for rect in rects:
        shape = predictor(gray, rect)
        coords = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

        leftEye = [coords[i] for i in LEFT_EYE]
        rightEye = [coords[i] for i in RIGHT_EYE]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # Draw EAR on frame
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Blink detection
        if ear < EYE_AR_THRESH:
            COUNTER += 1
        else:
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                pyautogui.click()
            COUNTER = 0

    cv2.imshow("Blink Clicker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
