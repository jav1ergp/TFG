from pymongo import MongoClient
from datetime import datetime
from models.plate import Plate
from models.log import Log

# Conexión a la base de datos
client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
collection = db['vehicles']

def handle_plate(plate, source):
    # Manejar las zonas de las matrículas
    print(f"Matrícula detectada: {plate.license_plate_text}")
    latest_record = get_latest_plate_record(plate.license_plate_text)

    if source == "PC":
        # Por el PC, es una entrada
        if latest_record:
            # Si la matrícula ya está registrada y no ha salido
            if latest_record["date_out"] is None:
                print(f"La matrícula {plate.license_plate_text} ya está dentro.")
            else:
                print(f"La matrícula {plate.license_plate_text} ya salió, registrando nueva entrada.")
                Plate.save_plate_to_db(plate)  # Guardar como nueva entrada
        else:
            # Si no hay registros previos, se registra la entrada
            Plate.save_plate_to_db(plate)
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
                    update_plate_date_out(latest_record["_id"], plate.date_in, latest_record["zona"], "fuera")
                    print(f"Date_out actualizado para la matrícula {plate.license_plate_text}")
                else:
                    print(f"No se ha alcanzado el tiempo mínimo para actualizar la salida de: {plate.license_plate_text}")
            else:
                print(f"La matrícula {plate.license_plate_text} ya ha salido.")
        else:
            # Si no hay registro previo en la base de datos (no está registrada), es un error
            print(f"Error: La matrícula {plate.license_plate_text} no está registrada, no puede salir.")
            
    elif source == "Movil":
        # Por el móvil, es un cambio de zona
        if latest_record:
            if latest_record["zona"] == "zona1":
                update_plate_zone(latest_record["_id"], "zona2")
                print(f"La matrícula {plate.license_plate_text} ha cambiado de zona1 a zona2.")
                log = Log(
                    action="Cambio de zona",
                    description=f"Vehículo cambió de zona1 a zona2",
                    plate=plate.license_plate_text,
                    zone="zona1 -> zona2",
                    time_in=latest_record["date_in"]
                )
                log.save_log(log)  # Guardar log cuando cambia de zona
            else:
                print(f"La matrícula {plate.license_plate_text} ya está en zona2 o ha salido.")
        else:
            print(f"Error: La matrícula {plate.license_plate_text} no está registrada en el sistema.")
            log = Log(
                action="Error de cambio de zona",
                description=f"Intento de cambiar zona para matrícula no registrada",
                plate=plate.license_plate_text
            )
            log.save_log(log)  # Guardar log de error

def time_check(date_in):
    # Verifica el tiempo transcurrido desde la última entrada
    current_time = datetime.now()
    if isinstance(date_in, str):
        date_in = datetime.strptime(date_in, "%Y-%m-%d %H:%M:%S")
    
    time_difference = (current_time - date_in).total_seconds() / 60
    return time_difference

def get_latest_plate_record(license_plate_text):
    # Obtener el registro más reciente de la matrícula
    return collection.find_one(
        {"plate": license_plate_text},
        sort=[("date_in", -1)]  # Ordenar por date_in en orden descendente
    )

def update_plate_date_out(record_id, date_out, old_zone, new_zone):
    result = collection.update_one(
        {"_id": record_id},
        {"$set": {"zona": new_zone, "date_out": date_out}}
    )
    
    plate_record = collection.find_one({"_id": record_id})
    
    log = Log(
        action="Salida",
        description=f"El vehículo con matrícula {plate_record['plate']} salió del estacionamiento de la zona {old_zone} a la zona {new_zone} a las {date_out}",
        plate=plate_record["plate"],
        zone=new_zone,
        time_in=plate_record["date_in"],
        time_out=date_out
    )
    
    log.save_log(log)  
    
    return result

def update_plate_zone(record_id, new_zone):
    old_record = collection.find_one({"_id": record_id})
    result = collection.update_one(
        {"_id": record_id},
        {"$set": {"zona": new_zone}}
    )

    log = Log(
        action="Cambio de zona",
        description=f"El vehículo con matrícula {old_record['plate']} cambió de zona de {old_record['zona']} a {new_zone}",
        plate=old_record['plate'],
        zone=f"{old_record['zona']} -> {new_zone}",
        time_in=old_record['date_in']
    )
    
    log.save_log(log) 

    return result