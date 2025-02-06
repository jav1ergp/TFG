from fast_alpr import ALPR
from datetime import datetime, timedelta
from models.plate import Plate

def init_alpr():
    return ALPR(
        detector_model="yolo-v9-t-384-license-plate-end2end",
        ocr_model="global-plates-mobile-vit-v2-model",
        ocr_providers=['CPUExecutionProvider'],
        detector_providers=['CPUExecutionProvider']
    )

def detect_plate(frame):
    alpr = init_alpr()
    results = alpr.predict(frame)

    if results and results[0].ocr.text != "":
        ocr_result = results[0].ocr
        license_plate_text = ocr_result.text
        confidence = round(ocr_result.confidence, 2)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        zona = "entrada"
        #comprobar zona
        print("AAAAAAAAA", license_plate_text, confidence)

        # Solo crea la instancia si la matrícula es válida y la confianza es alta
        if Plate.es_matricula_valida(license_plate_text) and confidence >= 0.9:
            return Plate(license_plate_text, confidence, current_time, zona)

    return None  # Si no se detecta una matrícula válida
