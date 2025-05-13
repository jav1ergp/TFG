from pymongo import MongoClient
from datetime import datetime
from backend.models.plate import Plate
from backend.models.log import Log
from config.back_config import MONGO_URI

# Conexión a la base de datos
client = MongoClient(MONGO_URI)
db = client['parking']
collection = db['vehicles']

def handle_plate(plate, source):
    print(f"Matricula detectada: {plate.license_plate_text}")
    latest_record = get_latest_plate_record(plate.license_plate_text)

    if source == "Entrada":
        if latest_record:
            # Si la matrícula ya está registrada y no ha salido
            if latest_record["date_out"] is None:
                print(f"La matricula {plate.license_plate_text} ya está dentro.")
            else:
                print(f"La matricula {plate.license_plate_text} ya salió, registrando nueva entrada.")
                Plate.save_plate_to_db(plate)
        else:
            # Si no hay registros previos, se registra la entrada
            Plate.save_plate_to_db(plate)
            print(f"{plate.vehicle} Nuevo registro de entrada para la matricula: {plate.license_plate_text}")
        
    elif source == "Salida":
        # Por el portátil, es una salida
        if latest_record:
            # Si la matrícula está registrada y no ha salido aún
            if latest_record["date_out"] is None and latest_record["zona"] == "salida":
                # Actualizar date_out y cambiar la zona a "fuera"
                update_plate_date_out(latest_record["_id"], "fuera")
                print(f"Date_out actualizado para la matricula {plate.license_plate_text}")
            else:
                print(f"La matricula {plate.license_plate_text} ya ha salido, o no ha entrado.")
        else:
            # Si no hay registro previo en la base de datos (no está registrada), es un error
            print(f"Error: La matricula {plate.license_plate_text} no está registrada, no puede salir.")
            
    elif source == "Zona":
        # Por el móvil, es un cambio de zona
        if latest_record:
            if latest_record["zona"] == "entrada":
                update_plate_zone(latest_record["_id"], "salida")
                print(f"La matricula {plate.license_plate_text} ha cambiado de entrada a salida.")
            else:
                print(f"La matricula {plate.license_plate_text} ya está en salida o ha salido.")
        else:
            print(f"Error: La matricula {plate.license_plate_text} no está registrada en el sistema.")
            log = Log(
                action="Error de cambio de zona",
                description=f"Intento de cambiar zona para matricula no registrada",
                plate=plate.license_plate_text,
                zone="Entrada -> Salida",
                date_in=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            Log.save_log(log)


def get_latest_plate_record(license_plate_text):
    return collection.find_one(
        {"plate": license_plate_text},
        sort=[("date_in", -1)]  # Ordenar por date_in en orden descendente
    )


def update_plate_date_out(record_id, new_zone):
    db_plate = collection.find_one({"_id": record_id})
    date_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    collection.update_one({"_id": db_plate["_id"]}, {"$set": {"zona": new_zone, "date_out": date_out}})
    
    if db_plate["vehicle"] == "coche":
        vehicle = "El coche"
    elif db_plate["vehicle"] == "moto":
        vehicle = "La moto"
            
    log = Log(
        action="Salida",
        description=f"{vehicle} con matricula {db_plate['plate']} salió del estacionamiento a las {date_out}",
        plate=db_plate["plate"],
        zone=new_zone,
        date_in=db_plate["date_in"],
        date_out=date_out
    )
    
    Log.save_log(log)


def update_plate_zone(record_id, new_zone):
    db_plate = collection.find_one({"_id": record_id})
    
    collection.update_one({"_id": db_plate["_id"]}, {"$set": {"zona": new_zone}})

    if db_plate["vehicle"] == "coche":
        vehicle = "El coche"
    elif db_plate["vehicle"] == "moto":
        vehicle = "La moto"
        
    log = Log(
        action="Cambio de zona",
        description=f"{vehicle} con matricula {db_plate['plate']} cambió de zona de {db_plate['zona']} a {new_zone}",
        plate=db_plate['plate'],
        zone=f"{db_plate['zona']} -> {new_zone}",
        date_in=db_plate['date_in']
    )
    
    Log.save_log(log)