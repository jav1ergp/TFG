import random
import string
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
from backend.models.plate import Plate
from backend.services.db_service import handle_plate
from config.back_config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

def generar_matricula():
    numeros = ''.join(random.choices(string.digits, k=4))
    letras = ''.join(random.choices('BCDFGHJKLMNPRSTVWXYZ', k=3))  # Letras válidas en matrículas españolas
    return f"{numeros}{letras}"

def generar_fecha_aleatoria():
    dias_atras = random.randint(0, 13)
    hora_random = random.randint(6, 22)
    minuto_random = random.randint(0, 59)
    
    fecha = datetime.now() - timedelta(days=dias_atras)
    fecha = fecha.replace(hour=hora_random, minute=minuto_random, second=0, microsecond=0)
    
    return fecha.strftime("%Y-%m-%d %H:%M:%S")  # Convertir a string ya aquí


def get_matriculas_por_zona(zona):
    return list(collection.find({"zona": zona, "date_out": None}))

def simular_accion():
    opciones = ["entrada", "zona", "salida"]
    accion = random.choice(opciones)

    if accion == "entrada2":
        plate = Plate(
            license_plate_text=generar_matricula(),
            confidence="0.95",
            vehicle=random.choice(["coche", "moto"]),
            date_in=generar_fecha_aleatoria(),
            zona="Zona 1",
        )
        handle_plate(plate, "Entrada")
        
    elif accion == "zona":
        registros = get_matriculas_por_zona("Zona 1")
        if registros:
            elegido = random.choice(registros)
            plate = Plate(
                license_plate_text=elegido["plate"],
                confidence="0.95",
                vehicle=elegido["vehicle"],
                date_in=elegido["date_in"],
                zona="Zona 1"
            )
            handle_plate(plate, "Zona")

    elif accion == "salida2":
        registros = get_matriculas_por_zona("Zona 2")
        if registros:
            elegido = random.choice(registros)
            plate = Plate(
                license_plate_text=elegido["plate"],
                confidence="0.95",
                vehicle=elegido["vehicle"],
                date_in=elegido["date_in"],
                zona="Zona 2"
            )
            handle_plate(plate, "Salida")



def iniciar_simulacion():
    for _ in range(200):
        simular_accion()
        time.sleep(2)

if __name__ == "__main__":
    iniciar_simulacion()
