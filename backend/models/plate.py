from pymongo import MongoClient
from datetime import datetime
from backend.models.log import Log
from config.back_config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

class Plate:
    def __init__(self, license_plate_text, confidence, vehicle, date_in, zona, date_out=None):
        self.license_plate_text = license_plate_text
        self.confidence = confidence
        self.vehicle = vehicle
        self.date_in = date_in
        self.date_out = date_out
        self.zona = zona
    
    @classmethod
    def save_plate(cls, plate):
        plate_data = {
            "plate": plate.license_plate_text,
            "confidence": plate.confidence,
            "vehicle": plate.vehicle,
            "date_in": plate.date_in,
            "date_out": plate.date_out,
            "zona": plate.zona
        }
        
        collection.insert_one(plate_data)
        
        if plate.vehicle == "coche":
            vehicle = "El coche"
        elif plate.vehicle == "moto":
            vehicle = "La moto"
            
        log = Log(
            action="Entrada",
            description=f"{vehicle} con matrícula {plate.license_plate_text} entró al parking a las {plate.date_in}",
            plate=plate.license_plate_text,
            zona=plate.zona,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        Log.save_log(log)
        
        return plate
    
    @staticmethod
    def is_valid_plate(license_plate_text):
        license_plate_text = license_plate_text.replace(" ", "").replace("-", "")
        
        # Matrícula moderna: 4 dígitos + 3 letras (ejemplo: 1234XYZ)
        if len(license_plate_text) == 7 and license_plate_text[:4].isdigit() and license_plate_text[4:].isalpha() and license_plate_text[4:].isupper():
            return True
        
        # Matrícula antigua: 1-2 letras + 4 dígitos + 1-2 letras (ejemplo: M1234AB, MA1234A)
        if 6 <= len(license_plate_text) <= 8:
            for i in range(len(license_plate_text)):
                if license_plate_text[i].isdigit():
                    letras_iniciales = license_plate_text[:i]
                    numeros = license_plate_text[i:i+4]
                    letras_finales = license_plate_text[i+4:]

                    if (1 <= len(letras_iniciales) <= 2 and len(numeros) == 4 and numeros.isdigit() and
                        1 <= len(letras_finales) <= 2 and letras_finales.isalpha() and
                        letras_iniciales.isupper() and letras_finales.isupper()):
                        return True
        return False
