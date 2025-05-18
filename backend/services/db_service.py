from pymongo import MongoClient
from datetime import datetime
from backend.models.plate import Plate
from backend.models.log import Log
from config.back_config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

def handle_plate(plate, source):
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
                print(f"La matricula {plate.license_plate_text} ya salió, registrando nueva entrada.")
                Plate.save_plate(plate)
                log = Log(
                    action="Registro matricula",
                    description=f"Se registró una matricula que salió previamente",
                    plate=plate.license_plate_text,
                    zona="Zona 1",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
                
        else:
            # Si no hay registros previos, se registra la entrada
            Plate.save_plate(plate)
            print(f"{plate.vehicle} Nuevo registro de entrada para la matricula: {plate.license_plate_text}")
            log = Log(
                    action="Registro nueva matricula",
                    description=f"Se registró una nueva matricula",
                    plate=plate.license_plate_text,
                    zona="Zona 1",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            Log.save_log(log)
                
    elif source == "Salida":
        if latest_record:
            # Si la matrícula está registrada y no ha salido aún
            if latest_record["date_out"] is None and latest_record["zona"] == "Zona 2":
                update_plate_date_out(latest_record["_id"], "fuera")
                print(f"Date_out actualizado para la matricula {plate.license_plate_text}")
                log = Log(
                    action="Vehiculo ha salido del parking",
                    description=f"Vehiculo con la matricula {plate.license_plate_text} ha salido del parking",
                    plate=plate.license_plate_text,
                    zona="Zona 2 -> Fuera",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
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
            print(f"Error: La matricula {plate.license_plate_text} no está registrada, no puede salir.")
            log = Log(
                action="Error de cambio de zona",
                description=f"Intento de cambiar zona para matricula no registrada",
                plate=plate.license_plate_text,
                zona="Zona 2 -> Fuera",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            Log.save_log(log)
            
    elif source == "Zona":
        if latest_record:
            if latest_record["zona"] == "Zona 1":
                update_plate_zona(latest_record["_id"], "Zona 2")
                print(f"La matricula {plate.license_plate_text} ha cambiado de entrada a salida.")
                log = Log(
                    action="Vehiculo ha cambiado de zona",
                    description=f"Vehiculo con la matricula {plate.license_plate_text} ha cambiado de zona",
                    plate=plate.license_plate_text,
                    zona="Zona 1 -> Zona 2",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
            else:
                print(f"La matricula {plate.license_plate_text} ya está en salida o ha salido.")
                log = Log(
                action="Error de cambio de zona",
                description=f"Vehiculo con la matricula {plate.license_plate_text} ya está en salida o ha salido",
                plate=plate.license_plate_text,
                zona="Zona 1 -> Zona 2",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            Log.save_log(log)
        else:
            print(f"Error: La matricula {plate.license_plate_text} no está registrada en el sistema.")
            log = Log(
                action="Error de cambio de zona",
                description=f"Intento de cambiar zona para matricula no registrada",
                plate=plate.license_plate_text,
                zona="Zona 1 -> Zona 2",
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            Log.save_log(log)


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