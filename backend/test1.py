import cv2
import pytesseract as tess
from ultralytics import YOLO
from PIL import Image
import numpy as np

# Configurar la ruta de Tesseract si es necesario
# Cambia esta ruta según tu instalación
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para limpiar la región de la matrícula


def cleanPlate(plate):
    print("CLEANING PLATE...")
    gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        max_cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(max_cnt)

        cleaned_final = thresh[y:y + h, x:x + w]
        return cleaned_final, [x, y, w, h]
    else:
        return plate, None



# Cargar modelos YOLO preentrenados
model_detector = YOLO('yolov8n.pt')  # Modelo general
model_detector_license = YOLO(
    'license_plate_detector.pt')  # Detector de matrículas

# Leer la imagen
img = cv2.imread('car2.jpg')

# Realizar detección de vehículos
results = model_detector(img, verbose=False)[0]
detections = results.boxes.data.tolist()

vehicles = [2]  # ID de clase para 'coche' en el conjunto de datos COCO

for det in detections:
    x1, y1, x2, y2, score, class_id = list(map(int, det[:4])) + det[4:]
    if int(class_id) in vehicles and score > 0.5:
        # Dibujar la detección del vehículo
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"Car: {score:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Recortar la región del vehículo para detectar matrículas
        vehicle_roi = img[y1:y2, x1:x2]

        # Guardar la imagen del vehículo que se envía al detector de matrículas
        cv2.imwrite('vehicle_roi.jpg', vehicle_roi)
        print("Imagen del vehículo guardada como 'vehicle_roi.jpg'")

        # Detectar matrículas en la región del vehículo
        license_results = model_detector_license(vehicle_roi, verbose=False)[0]

        for license_det in license_results.boxes.data.tolist():
            lx1, ly1, lx2, ly2, lscore, _ = list(
                map(int, license_det[:4])) + license_det[4:]
            if lscore > 0.3:  # Baja el umbral de confianza
                plate_roi = vehicle_roi[ly1:ly2, lx1:lx2]

                # Guardar la imagen recortada de la matrícula para inspección
                cv2.imwrite(f'plate_roi_{lx1}_{ly1}.jpg', plate_roi)
                print(f"Recorte de matrícula guardado como 'plate_roi_{
                      lx1}_{ly1}.jpg)'")

                # Limpiar la matrícula
                cleaned_plate, bbox = cleanPlate(plate_roi)
                if bbox is None:
                    print("No se pudo limpiar la matrícula.")
                    continue

                # Realizar OCR
                text = tess.image_to_string(
                    cleaned_plate, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                )
                print(f'Matrícula detectada: {text.strip()}')

                # Guardar la imagen procesada para inspección
                cv2.imwrite(f'cleaned_plate_{lx1}_{ly1}.jpg', cleaned_plate)
                print(f"Imagen procesada guardada como 'cleaned_plate_{
                      lx1}_{ly1}.jpg)'")

# Guardar la imagen anotada con la matrícula detectada
cv2.imwrite('annotated_image.jpg', img)
print("Imagen anotada guardada como 'annotated_image.jpg'")
