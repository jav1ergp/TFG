from fast_alpr import ALPR
from datetime import datetime, timedelta

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
    license_plate_text = ""
    confidence = 0.0
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    if results and results[0].ocr.text != "":
        ocr_result = results[0].ocr  #1 matricula y conf
        license_plate_text = ocr_result.text
        confidence = round(ocr_result.confidence, 2)
        print("AAAAAAAAA", license_plate_text, confidence)
        if es_matricula_valida(license_plate_text) and confidence >= 0.9:
            return license_plate_text, round(confidence, 2), current_time_str
    return "", 0.0, current_time_str

def es_matricula_valida(matricula):
    matricula = matricula.replace(" ", "").replace("-", "")  # espacios y guiones
    
    # matrícula moderna 4 dígitos y 3 letras
    if len(matricula) == 7 and matricula[:4].isdigit() and matricula[4:].isalpha() and matricula[4:].isupper():
        return True
    
    # matrícula antigua 1-2 letras y 4 dígitos y 1-2 letras
    if 6 <= len(matricula) <= 8:
        # 
        for i in range(len(matricula)):
            if matricula[i].isdigit():
                letras_iniciales = matricula[:i]
                numeros = matricula[i:i+4]
                letras_finales = matricula[i+4:]
                
                # Validar formato: letras-números-letras
                if (1 <= len(letras_iniciales) <= 2 and len(numeros) == 4 and numeros.isdigit() 
                    and 1 <= len(letras_finales) <= 2 and letras_finales.isalpha() and
                    letras_iniciales.isupper() and letras_finales.isupper()):
                    return True
    return False

