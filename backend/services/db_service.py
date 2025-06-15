from pymongo import MongoClient
from datetime import datetime, timedelta
import requests
from backend.models.plate import Plate
from backend.models.log import Log
from config.config import MONGO_URI, MONGO_PARKING, BOT_TOKEN, CHAT_ID

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

last_detections = {}

def handle_plate(plate, source):
    """Gestiona el registro de una matrícula detectada según la cámara fuente (Entrada, Zona, Salida).
    Actualiza la base de datos y genera logs de las acciones realizadas o errores detectados"""
    
    current_time = datetime.now()
    detection_id  = (plate.license_plate_text, source)
    
    to_delete = [key for key, ts in last_detections.items() 
                if current_time - ts > timedelta(seconds=30)]
    for key in to_delete:
        del last_detections[key]
    
    # Verifica si la deteccion es repetida y reciente de la misma camara
    if detection_id  in last_detections:
        last_time = last_detections[detection_id ]
        if current_time - last_time < timedelta(seconds=10):
            print(f"Detección repetida ignorada: {plate.license_plate_text} en {source}")
            return  # Salir sin procesar la deteccion
    
    # Actualizar nueva deteccion
    last_detections[detection_id ] = current_time
    
    print(f"Matricula detectada: {plate.license_plate_text}")
    latest_record = get_latest_plate_record(plate.license_plate_text)

    if source == "Entrada":
        if latest_record:
            # Si la matrícula ya está registrada y no ha salido
            if latest_record["date_out"] is None:
                print(f"La matricula {plate.license_plate_text} ya está dentro.")
                log = Log(
                    action="Error de detección",
                    description=f"Se registró una matricula que ya esta dentro del parking",
                    plate=plate.license_plate_text,
                    zona="Zona 1",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
            else:
                # Si ha salido se registra de nuevo
                Plate.save_plate(plate)
                print(f"La matricula {plate.license_plate_text} ya salió, registrando nueva entrada.")
                
                
        else:
            # Si no hay registros previos, se registra la entrada
            Plate.save_plate(plate)
            print(f"{plate.vehicle} Nuevo registro de entrada para la matricula: {plate.license_plate_text}")
                
    elif source == "Salida":
        if latest_record:
            # Si la matrícula está registrada y no ha salido aún
            if latest_record["date_out"] is None and latest_record["zona"] == "Zona 2":
                update_plate_date_out(latest_record["_id"], "fuera")
                print(f"Date_out actualizado para la matricula {plate.license_plate_text}")
                
            else:
                print(f"La matricula {plate.license_plate_text} ya ha salido, o no ha entrado.")
                log = Log(
                    action="Error de cambio de zona",
                    description=f"Vehiculo con la matricula {plate.license_plate_text} ya ha salido, o no ha entrado",
                    plate=plate.license_plate_text,
                    zona="Zona 2 -> Fuera",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
        else:
            # Si no hay registro previo en la base de datos (no está registrada), es un error
            similar_plate = find_similar_plate(plate.license_plate_text, "fuera", plate.vehicle) 
            
            if similar_plate:
                update_plate_date_out(similar_plate["_id"], "fuera")
                log = Log(
                    action="Matricula erronea detectada",
                    description=f"Vehiculo con la matricula {similar_plate["plate"]} ha salido del parking, por la matricula erroneamente detectada {plate.license_plate_text}",
                    plate=similar_plate["plate"],
                    zona="Zona 2 -> fuera",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
            
            else:
                send_telegram_notis(plate.license_plate_text, plate.vehicle, source)
                log = Log(
                    action="Error detección matricula",
                    description=f"Se ha detectado una matricula dentro del parking que no se ha detectado en la entrada",
                    plate=plate.license_plate_text,
                    zona="Zona 2 -> fuera",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
            
    elif source == "Zona":
        if latest_record:
            if latest_record["date_out"] is None and latest_record["zona"] == "Zona 1":
                update_plate_zona(latest_record["_id"], "Zona 2")
                
            else:
                log = Log(
                    action="Error de cambio de zona",
                    description=f"Vehiculo con la matricula {plate.license_plate_text} ya está en salida o ha salido",
                    plate=plate.license_plate_text,
                    zona="Zona 1 -> Zona 2",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
                
        else:
            similar_plate = find_similar_plate(plate.license_plate_text, "Zona 2", plate.vehicle)  
            if similar_plate:
                update_plate_date_out(similar_plate["_id"], "Zona 2")
                log = Log(
                    action="Matricula erronea detectada",
                    description=f"Vehiculo con la matricula {similar_plate["plate"]} ha cambiado de zona, por la matricula erroneamente detectada {plate.license_plate_text}",
                    plate=similar_plate["plate"],
                    zona="Zona 1 -> Zona 2",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
            
            else:
                send_telegram_notis(plate.license_plate_text, plate.vehicle, source)
                log = Log(
                    action="Error detección matricula",
                    description=f"Se ha detectado una matricula dentro del parking que no se ha detectado en la entrada",
                    plate=plate.license_plate_text,
                    zona="Zona 1 -> Zona 2",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)

             

def get_latest_plate_record(license_plate_text):
    """Devuelve el registro mas reciente de una matricula en la base de datos"""
    return collection.find_one(
        {"plate": license_plate_text},
        sort=[("date_in", -1)]  # Ordenar por date_in en orden descendente
    )


def update_plate_date_out(record_id, new_zona):
    """Actualiza la fecha de salida y la zona de un registro de matricula"""
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
    """Actualiza la zona de un vehiculo en el registro de matricula"""
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
    """Busca una matricula similar en la zona previa para corregir errores de deteccion"""
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
    """Calcula la similitud de dos matriculas, detiene la comparacion si encuentra 2 diferencias"""
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


def send_telegram_notis(plate_text, vehicle_type, source):
    """Envia una notificacion por Telegram cuando se detecta una matricula erronea y no hay similitudes"""
    bot_token = BOT_TOKEN
    chat_id = CHAT_ID
      
    message = f"""
        Se ha detectado una matricula no registrada en el sistema
    🚗 *Matrícula Detectada*
    📋 Matrícula: `{plate_text}`
    🚙 Vehículo: {vehicle_type}
    📷 Cámara: {source}
    🕐 Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"Telegram enviado para matrícula {plate_text}")
        else:
            print(f"Error enviando Telegram: {response.text}")
    except Exception as e:
        print(f"Error enviando Telegram: {e}")