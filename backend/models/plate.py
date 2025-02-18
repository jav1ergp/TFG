from pymongo import MongoClient
from models.log import Log

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
collection = db['vehicles']

class Plate:
    def __init__(self, license_plate_text, confidence, date_in, zona, date_out=None):
        self.license_plate_text = license_plate_text
        self.confidence = confidence
        self.date_in = date_in
        self.date_out = date_out
        self.zona = zona
    
    @classmethod
    def save_plate_to_db(cls, plate):
        # Guardar los datos de la matrícula en la base de datos
        plate_data = {
            "plate": plate.license_plate_text,
            "confidence": plate.confidence,
            "date_in": plate.date_in,
            "date_out": plate.date_out,
            "zona": plate.zona
        }
        collection.insert_one(plate_data)
        
        log = Log(
            action="Entrada",
            description=f"El vehículo con matrícula {plate.license_plate_text} entró a la zona {plate.zona} a las {plate.date_in}",
            plate=plate.license_plate_text,
            zone=plate.zona,
            time_in=plate.date_in
        )
        
        log.save_log(log)
        
        return plate
    
    @staticmethod
    def es_matricula_valida(matricula):
        """Comprueba si el formato de la matrícula es válido (moderno o antiguo)."""
        matricula = matricula.replace(" ", "").replace("-", "")  # Elimina espacios y guiones
        
        # Matrícula moderna: 4 dígitos + 3 letras (ejemplo: 1234XYZ)
        if len(matricula) == 7 and matricula[:4].isdigit() and matricula[4:].isalpha() and matricula[4:].isupper():
            return True
        
        # Matrícula antigua: 1-2 letras + 4 dígitos + 1-2 letras (ejemplo: M1234AB, MA1234A)
        if 6 <= len(matricula) <= 8:
            for i in range(len(matricula)):
                if matricula[i].isdigit():  # Encuentra el primer número
                    letras_iniciales = matricula[:i]
                    numeros = matricula[i:i+4]
                    letras_finales = matricula[i+4:]

                    # Validar formato: letras-números-letras
                    if (1 <= len(letras_iniciales) <= 2 and len(numeros) == 4 and numeros.isdigit() and
                        1 <= len(letras_finales) <= 2 and letras_finales.isalpha() and
                        letras_iniciales.isupper() and letras_finales.isupper()):
                        return True
        return False
