from ultralytics import YOLO
import easyocr
import cv2
import time

model_detector = YOLO('yolov8n.pt')
model_detector_license = YOLO('license_plate_detector.pt')


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vehicles = [2] 

start_time = time.time()
frame_count = 0

# Inicializar EasyOCR
reader = easyocr.Reader(['en'])


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model_detector(frame, verbose=False)[0]
    detections = results.boxes.data.tolist()

    for det in detections:
        x1, y1, x2, y2, score, class_id = list(map(int, det[:4])) + det[4:]
        if int(class_id) in vehicles and score > 0.5:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"Car: {score:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Recortar la región del vehículo para detectar matrículas
            vehicle_roi = frame[y1:y2, x1:x2]
            license_results = model_detector_license(
                vehicle_roi, verbose=False)[0]
            for license_det in license_results.boxes.data.tolist():
                lx1, ly1, lx2, ly2, lscore, _ = list(
                    map(int, license_det[:4])) + license_det[4:]
                if lscore > 0.5:
                    text = reader.readtext(license_det[0])
                    print(f'Matrícula detectada: {text}')
                    cv2.rectangle(vehicle_roi, (lx1, ly1),
                                  (lx2, ly2), (255, 0, 0), 2)
                    cv2.putText(vehicle_roi, f"Plate: {lscore:.2f}", (lx1, ly1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('Vehicle Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
