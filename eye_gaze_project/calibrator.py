import cv2

def run_calibration():
    print("Starting calibration...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not detected.")
        return

    print("Look at the CENTER of the screen and press SPACE when ready.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, "Look at the CENTER and press SPACE", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow("Calibration", frame)

        key = cv2.waitKey(1)
        if key == 32:  # Spacebar
            print("Calibration point captured!")
            break
        elif key == 27:  # ESC
            print("Calibration canceled.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Calibration completed!")

if __name__ == "__main__":
    run_calibration()
