from threading import Thread
import cv2
from ultralytics import YOLO
import logging
from backend.services import alpr_service
from backend.services import db_service

# Configuración de logging para evitar mensajes excesivos
logging.getLogger('open_image_models.detection.core.yolo_v9.inference').handlers.clear()
logging.getLogger('open_image_models.detection.pipeline.license_plate').handlers.clear()
logging.getLogger('open_image_models.detection.core.yolo_v9.inference').setLevel(logging.WARNING)
logging.getLogger('open_image_models.detection.pipeline.license_plate').setLevel(logging.WARNING)
logging.getLogger('ultralytics').setLevel(logging.CRITICAL)

def start_detection(url_entrada, url_zona, url_salida):
    cameras = {
        "Entrada": url_entrada,
        "Zona": url_zona,
        "Salida": url_salida
    }

    for source, url in cameras.items():
        thread = Thread(target=process_camera, args=(source, url))
        thread.daemon = True
        thread.start()


def process_camera(source, url):
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(url)
    
    if not cap.isOpened():
        print(f"No se pudo acceder a la cámara ({url}).")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Error al capturar frame de la cámara {source}.")
            break

        results = model(frame)
        
        # Procesar cada detección
        for result in results[0].boxes:
            if result.cls in [2, 3]:
                class_id = int(result.cls)
                
                if class_id == 2:
                    vehicle = "coche"
                elif class_id == 3:
                    vehicle = "moto"

                plate = alpr_service.detect_plate(frame, vehicle)
                
                if plate is not None:
                    db_service.handle_plate(plate, source)
                    
    cap.release()
    
        
        