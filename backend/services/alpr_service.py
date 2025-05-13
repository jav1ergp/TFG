from fast_alpr import ALPR
from datetime import datetime
from backend.models.plate import Plate

def init_alpr():
    return ALPR(
        detector_model="yolo-v9-t-384-license-plate-end2end",
        ocr_model="global-plates-mobile-vit-v2-model",
        ocr_providers=['CPUExecutionProvider'],
        detector_providers=['CPUExecutionProvider']
    )

def detect_plate(frame, vehicle):
    alpr = init_alpr()
    results = alpr.predict(frame)

    if results and results[0].ocr.text != "":
        ocr_result = results[0].ocr
        license_plate_text = ocr_result.text
        confidence = round(ocr_result.confidence, 2)
        date_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        zona = "entrada"
        print("AAAAAAAAA", license_plate_text, confidence)
        
        if Plate.is_valid_plate(license_plate_text) and confidence > 0.9:
            return Plate(license_plate_text, confidence, vehicle, date_in, zona)

    return None
