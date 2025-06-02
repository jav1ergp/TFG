from pymongo import MongoClient  
from datetime import datetime  
import sys  
import os  
  
# Añadir el directorio padre al path para poder importar los módulos  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
  
from backend.models.plate import Plate
from backend.models.log import Log  
from backend.services.db_service import handle_plate, find_similar_plate, get_latest_plate_record, update_plate_zona, send_telegram_notis
from config.config import MONGO_URI, MONGO_PARKING
  
# Conexión a la base de datos  
client = MongoClient(MONGO_URI)  
db = client['parking']  
collection = db['vehicles']  
  
from pymongo import MongoClient    
from datetime import datetime    
import sys    
import os    
    
# Añadir el directorio padre al path para poder importar los módulos    
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    
    
from backend.models.plate import Plate  
from backend.models.log import Log    
# Importar tu nueva implementación en lugar de la del db_service actual  
from config.config import MONGO_URI, MONGO_PARKING  
    
    
from pymongo import MongoClient
from datetime import datetime
from backend.models.plate import Plate
from backend.models.log import Log
from config.config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

def handle_plate(plate, source):
    print(f"Matricula detectada: {plate.license_plate_text}")
    latest_record = get_latest_plate_record(plate.license_plate_text)

    if source == "Entrada":
        
        # Si la matrícula está registrada
        if latest_record:
            
            # Si no ha salido
            if latest_record["date_out"] is None:
                # Log error
            
            # Si ha salido, nueva entrada
            else:
                Plate.save_plate(plate)
                # Log error
        
        # No hay registros, nueva entrada   
        else:
            Plate.save_plate(plate)
            # Log exito
                
    elif source == "Salida":
        
        # Si la matrícula está registrada
        if latest_record:
            
            # Si no ha salido y su ultimo registro es en la zona 2
            if latest_record["date_out"] is None and latest_record["zona"] == "Zona 2":
                update_plate_date_out(latest_record["_id"], "fuera")
                # Log exito
                
            # Si ha salido 
            else:
                # Log error
        
        # Si la matrícula NO está registrada 
        else:
            
            # Si existe matricula casi igual
            similar_plate = find_similar_plate(plate.license_plate_text, "fuera", plate.vehicle)
            if similar_plate:
                update_plate_date_out(similar_plate["_id"], "fuera")
                # Log exito
                
            # Si no existe
            else:
                send_telegram_notis(plate.license_plate_text, plate.vehicle, source)
                # Log error
            
            
    elif source == "Zona":
        
        # Si la matrícula está registrada
        if latest_record:
            
            # Si no ha salido y su ultimo registro es en la zona 1
            if latest_record["date_out"] is None and latest_record["zona"] == "Zona 1":
                update_plate_zona(latest_record["_id"], "Zona 2")
            else:
                
        # Si la matrícula NO está registrada 
        else:
            
            # Si existe matricula casi igual
            similar_plate = find_similar_plate(plate.license_plate_text, "Zona 2", plate.vehicle)  
            if similar_plate:
                update_plate_date_out(similar_plate["_id"], "Zona 2")
                # Log exito
                
            else:
                send_telegram_notis
                # Log error
                
            

             

def get_latest_plate_record(license_plate_text):
    return collection.find_one(
        {"plate": license_plate_text},
        sort=[("date_in", -1)]  # Ordenar por date_in en orden descendente
    )


def update_plate_date_out(record_id, new_zona):
    db_plate = collection.find_one({"_id": record_id})
    date_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    collection.update_one({"_id": db_plate["_id"]}, {"$set": {"zona": new_zona, "date_out": date_out}})
    
    if db_plate["vehicle"] == "coche":
        vehicle = "El coche"
    elif db_plate["vehicle"] == "moto":
        vehicle = "La moto"
            
    log = Log(
        action="Salida",
        description=f"{vehicle} con matricula {db_plate['plate']} salió del estacionamiento a las {date_out}",
        plate=db_plate["plate"],
        zona=new_zona,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    Log.save_log(log)


def update_plate_zona(record_id, new_zona):
    db_plate = collection.find_one({"_id": record_id})
    
    collection.update_one({"_id": db_plate["_id"]}, {"$set": {"zona": new_zona}})

    if db_plate["vehicle"] == "coche":
        vehicle = "El coche"
    elif db_plate["vehicle"] == "moto":
        vehicle = "La moto"
        
    log = Log(
        action="Cambio de zona",
        description=f"{vehicle} con matricula {db_plate['plate']} cambió de zona de {db_plate['zona']} a {new_zona}",
        plate=db_plate['plate'],
        zona=f"{db_plate['zona']} -> {new_zona}",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    Log.save_log(log)
    
def find_similar_plate(plate_text, zona, vehicle):
    if zona == "Zona 2":
        previous_zone = "Zona 1"
    elif zona == "fuera":
        previous_zone = "Zona 2"
    else:
        return None
    
    plates_in_previous_zone = list(collection.find(
        {"zona": previous_zone, "date_out": None, "vehicle": vehicle}
    ))
      
    if not plates_in_previous_zone:
        return None
    
    best_match = None
    best_score = 5
      
    for plate in plates_in_previous_zone:
        score = similar_score(plate_text, plate["plate"])
        
        if score > best_score:
            best_score = score
            best_match = plate
            break
            
    return best_match

def similar_score(plate1, plate2):
    same_chars = 0
    not_same = 0

    for i in range(len(plate1)):
        if plate1[i] == plate2[i]:
            same_chars += 1
        else:
            not_same += 1
            if not_same == 2:
                break        
    
    return same_chars    