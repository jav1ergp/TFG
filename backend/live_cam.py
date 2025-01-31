import cv2
from fast_alpr import ALPR
from pymongo import MongoClient
from datetime import datetime
import time
from flask import Flask, Response, jsonify

# Configuración de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client['alpr']  # Nombre de la base de datos
collection = db['plates']  # Nombre de la colección

# Inicializar ALPR
alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
    ocr_providers=['CPUExecutionProvider'],
    detector_providers=['CPUExecutionProvider']
)

# Inicializar la cámara
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

print("Presiona 'q' para salir.")

try:
    while True:
        # Capturar un frame de la cámara
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo capturar el frame.")
            break

        # Procesar el frame con ALPR
        alpr_results = alpr.predict(frame)

        # Extraer texto de la matrícula y confianza
        license_plate_text = ""
        confidence = 0.0
        if alpr_results:  # Verificar si hay resultados
            ocr_result = alpr_results[0].ocr
            license_plate_text = ocr_result.text
            confidence = round(ocr_result.confidence, 2)

        # Dibujar predicciones en el frame
        annotated_frame = alpr.draw_predictions(frame)

        # Mostrar el frame con las predicciones
        cv2.imshow("ALPR Result", annotated_frame)

        # Guardar los datos en MongoDB si se detectó una matrícula
        if license_plate_text and confidence > 0.9:
            current_time = datetime.now()
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

            plate_data = {
                "plate": license_plate_text,
                "confidence": confidence,
                "date_in": current_time_str,
                "date_out": None
            }
            collection.insert_one(plate_data)
            print(f"Matrícula detectada: {license_plate_text} (Confianza: {confidence})")
          
        # Esperar 2 segundos antes de capturar el siguiente frame
        if  0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nInterrupción por teclado detectada. Saliendo...")

finally:
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
