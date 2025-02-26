from ultralytics import YOLO
import cv2
import logging
from . import alpr_service
from . import db_service

logging.getLogger('open_image_models.detection.core.yolo_v9.inference').handlers.clear()
logging.getLogger('open_image_models.detection.pipeline.license_plate').handlers.clear()
logging.getLogger('open_image_models.detection.core.yolo_v9.inference').setLevel(logging.WARNING)
logging.getLogger('open_image_models.detection.pipeline.license_plate').setLevel(logging.WARNING)
logging.getLogger('ultralytics').setLevel(logging.CRITICAL)

def handle_car(frame, source, vehicle):  # logica para detectar matricula y meterla en la bd un coche
    plate = alpr_service.detect_plate(frame, vehicle)
    
    if plate is not None:
        db_service.handle_plate(plate, source)
        
        
    
def generate_frames(url_entrada, url_zona, url_salida):
    model = YOLO('yolov8n.pt')
    cap_entrada = cv2.VideoCapture(url_entrada)
    cap_zona = cv2.VideoCapture(url_zona)
    cap_salida = cv2.VideoCapture(url_salida)
    
    if not cap_entrada.isOpened():
        print("No se pudo acceder a la cámara de la entrada")
        return
    if not cap_zona.isOpened():
        print("No se pudo acceder a la cámara de la zona")
        return
    if not cap_salida.isOpened():
        print("No se pudo acceder a la cámara de la salida")
    else:
        print("Cámaras abierta")
        
        
    
    while True:
        frames = {
            "Entrada": cap_entrada.read(),
            "Zona": cap_zona.read(),
            "Salida": cap_salida.read()
        }
        
        for source, (ret, frame) in frames.items():
            if not ret:
                print(f"Error: No se pudo capturar el frame de la cámara {source}.")
                continue
        
            results = model(frame)
            filtered_results = []
            for result in results[0].boxes:
                if result.cls in [2, 3]:
                    filtered_results.append(result)

            # Procesar cada detección
            for result in filtered_results:
                class_id = int(result.cls)  # ID de la clase detectada
                
                if class_id == 2:
                    vehicle = "coche"
                elif class_id == 3:
                    vehicle = "moto"
                    
                handle_car(frame, source, vehicle) # Ejecutar la acción
                    
                    # comprobar matriculas repetidas y fechas
                    # meter en bd
                    # enviar a frontend


