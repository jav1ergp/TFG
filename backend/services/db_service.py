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
        "date_out": None
    }
    collection.insert_one(plate_data)
        
def handle_plate(plate):
    # Buscar el registro más reciente de la matrícula
    print(f"Matrícula detectada: {plate.license_plate_text}")
    latest_record = get_latest_plate_record(plate.license_plate_text)

    if latest_record:
        if latest_record["date_out"] is None:
            # Calcular el tiempo transcurrido desde date_in
            time_elapsed = time_check(latest_record["date_in"])
            print(f"Tiempo transcurrido desde la última entrada: {time_elapsed} minutos")

            if time_elapsed >= 3:
                # Actualizar date_out y cerrar el registro
                update_plate_date_out(latest_record["_id"], plate.date_in)
                print(f"Date_out actualizado para la matrícula: {plate.license_plate_text}")
            else:
                print(f"No se ha alcanzado el tiempo mínimo para actualizar el registro de: {plate.license_plate_text}")
        else:
            # Calcular el tiempo transcurrido desde el último date_out
            time_elapsed = time_check(latest_record["date_out"])
            print(f"Tiempo transcurrido desde el último date_out: {time_elapsed} minutos")

            if time_elapsed >= 3:
                # Crear un nuevo registro si ha pasado suficiente tiempo desde el último date_out
                save_plate_to_db(plate)
                print(f"Nuevo registro creado para la matrícula: {plate.license_plate_text}")
            else:
                print(f"No se ha alcanzado el tiempo mínimo para crear un nuevo registro de: {plate.license_plate_text}")
    else:
        # Si no hay registros previos, crear un nuevo registro
        save_plate_to_db(plate)
        print(f"Nuevo registro creado para una matrícula no registrada: {plate.license_plate_text}")


def time_check(date_in):
    current_time = datetime.now()
    # Convertir date_in a datetime si es una cadena
    if isinstance(date_in, str):
        date_in = datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S")
    
    time_difference = (current_time - date_in).total_seconds() / 60
    return time_difference

 
def repeited_plate(license_plate_text):
    existing_plate = collection.find_one({"plate": license_plate_text})
    
    if existing_plate:
        return True
    else:
        return False

def check_date_in_db(license_plate_text):
    plate_record = collection.find_one({"plate": license_plate_text})
    
    if plate_record and plate_record.get("date_out") is not None:
        return True
    
    return False

def get_latest_plate_record(license_plate_text):
    return collection.find_one(
        {"plate": license_plate_text},
        sort=[("date_in", -1)]  # Ordenar por date_in en orden descendente
    )

def update_plate_date_out(record_id, date_out):
    collection.update_one(
        {"_id": record_id},
        {"$set": {"date_out": date_out}}
    )
