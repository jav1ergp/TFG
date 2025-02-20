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

def handle_car(frame, source):  # logica para detectar matricula y meterla en la bd un coche
    plate = alpr_service.detect_plate(frame)
    
    if plate is not None:
        db_service.handle_plate(plate, source)

def handle_motorcycle(frame, source):  # logica para detectar matricula y meter en la bd moto
    return True
    
def generate_frames(url_pc, url_laptop, url_movil):
    model = YOLO('yolov8n.pt')
    cap_pc = cv2.VideoCapture(url_pc, cv2.CAP_DSHOW)
    cap_laptop = cv2.VideoCapture(url_laptop)
    cap_movil = cv2.VideoCapture(url_movil)
    
    if not cap_pc.isOpened():
        print("❌ No se pudo acceder a la cámara pc. Verifica que no esté en uso.")
        return
    if not cap_laptop.isOpened():
        print("❌ No se pudo acceder a la cámara portatil. Verifica que no esté en uso.")
        return
    if not cap_movil.isOpened():
        print("❌ No se pudo acceder a la cámara movil. Verifica que no esté en uso.")
    else:
        print("✅ Cámara abierta correctamente en Flask.")

    
    actions = {
        2: handle_car,
        3: handle_motorcycle
    }
    
    while True:
        frames = {
            "PC": cap_pc.read(),
            "Laptop": cap_laptop.read(),
            "Movil": cap_movil.read()
        }
        
        for source, (ret, frame) in frames.items():
            if not ret:
                print(f"Error: No se pudo capturar el frame de la cámara {source}.")
                continue
        
            results = model(frame)
            filtered_results = []
            for result in results[0].boxes:
                if result.cls in [2, 3]: # coche(2) o moto(3)
                    filtered_results.append(result)

            # Procesar cada detección
            for result in filtered_results:
                class_id = int(result.cls)  # ID de la clase detectada
                confidence = result.conf  # Confianza de la detección (valor entre 0 y 1)

                if confidence >= 0.8:  # Verificar si la confianza es del 80% o más
                    action = actions.get(class_id)  # Obtener la acción según la clase
                    if action:
                        action(frame, source)  # Ejecutar la acción
                    
                    # comprobar matriculas repetidas y fechas
                    # meter en bd
                    # enviar a frontend

            if source == "PC":
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()

                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


