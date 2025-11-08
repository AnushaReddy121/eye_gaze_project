import cv2

print("Testing camera...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Could not open webcam.")
else:
    ret, frame = cap.read()
    print("✅ Camera opened successfully.")
    print("Frame captured:", ret)
    if ret:
        cv2.imshow("Test Camera", frame)
        cv2.waitKey(3000)  # show 3 seconds
    cap.release()
    cv2.destroyAllWindows()
