from pymongo import MongoClient
from datetime import datetime
from models.plate import Plate

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
collection = db['vehicles']

def save_plate_to_db(plate):
    plate_data = {
        "plate": plate.license_plate_text,
        "confidence": plate.confidence,
        "date_in": plate.date_in,
        "date_out": plate.date_out,
        "zona": plate.zona
    }
    collection.insert_one(plate_data)
        
def handle_plate(plate, source):    # Manejar las zonas de las matriculas
    # Buscar el registro más reciente de la matrícula
    print(f"Matrícula detectada: {plate.license_plate_text}")
    latest_record = get_latest_plate_record(plate.license_plate_text)

    if source == "PC":
        # Por el PC, es una entrada
        if latest_record:
            # Si la matrícula ya está registrada y no ha salido
            if latest_record["date_out"] is None:
                print(f"La matrícula {plate.license_plate_text} ya está dentro.")
            else:
                print(f"La matrícula {plate.license_plate_text} ya salió, se está registrando de nuevo.")
                save_plate_to_db(plate)  # Guardar como nueva entrada
        else:
            # Si no hay registros previos, se registra la entrada
            save_plate_to_db(plate)
            print(f"Nuevo registro de entrada para la matrícula: {plate.license_plate_text}")
        
    elif source == "Portátil":
         # Por el portátil, es una salida
        if latest_record:
            # Si la matrícula está registrada y no ha salido aún
            if latest_record["date_out"] is None:
                time_elapsed = time_check(latest_record["date_in"])
                print(f"Tiempo transcurrido desde la última entrada: {time_elapsed} minutos")
                if time_elapsed >= 1:
                    # Actualizar date_out y cambiar la zona a "fuera"
                    update_plate_date_out(latest_record["_id"], plate.date_in)
                    print(f"Date_out actualizado para la matrícula {plate.license_plate_text}")
                else:
                    print(f"No se ha alcanzado el tiempo mínimo para actualizar la salida de: {plate.license_plate_text}")
            else:
                print(f"La matrícula {plate.license_plate_text} ya ha salido.")
        else:
            # Si no hay registro previo en la base de datos (no está registrada), es un error
            print(f"Error: La matrícula {plate.license_plate_text} no está registrada, no puede salir.")
            

def time_check(date_in):
    current_time = datetime.now()
    # Convertir date_in a datetime si es una cadena
    if isinstance(date_in, str):
        date_in = datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S")
    
    time_difference = (current_time - date_in).total_seconds() / 60
    return time_difference

def get_latest_plate_record(license_plate_text):
    return collection.find_one(
        {"plate": license_plate_text},
        sort=[("date_in", -1)]  # Ordenar por date_in en orden descendente
    )

def update_plate_date_out(record_id, date_out):
    collection.update_one(
        {"_id": record_id},
        {"$set": {"zona": "fuera", "date_out": date_out}}
    )

