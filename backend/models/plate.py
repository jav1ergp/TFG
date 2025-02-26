from pymongo import MongoClient
from models.log import Log

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
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
    def save_plate_to_db(cls, plate):
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
            zone=plate.zona,
            date_in=plate.date_in
        )
        
        Log.save_log(log)
        
        return plate
    
    @staticmethod
    def is_valid_plate(matricula):
        matricula = matricula.replace(" ", "").replace("-", "")
        
        # Matrícula moderna: 4 dígitos + 3 letras (ejemplo: 1234XYZ)
        if len(matricula) == 7 and matricula[:4].isdigit() and matricula[4:].isalpha() and matricula[4:].isupper():
            return True
        
        # Matrícula antigua: 1-2 letras + 4 dígitos + 1-2 letras (ejemplo: M1234AB, MA1234A)
        if 6 <= len(matricula) <= 8:
            for i in range(len(matricula)):
                if matricula[i].isdigit():
                    letras_iniciales = matricula[:i]
                    numeros = matricula[i:i+4]
                    letras_finales = matricula[i+4:]

                    if (1 <= len(letras_iniciales) <= 2 and len(numeros) == 4 and numeros.isdigit() and
                        1 <= len(letras_finales) <= 2 and letras_finales.isalpha() and
                        letras_iniciales.isupper() and letras_finales.isupper()):
                        return True
        return False
