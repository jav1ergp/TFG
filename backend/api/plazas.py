from flask import Blueprint, jsonify
from pymongo import MongoClient
from config.back_config import TOTAL_ENTRY_SPOTS_CAR, TOTAL_EXIT_SPOTS_CAR, TOTAL_ENTRY_SPOTS_MOTO, TOTAL_EXIT_SPOTS_MOTO, MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

parking_bp = Blueprint("parking", __name__)

@parking_bp.route("/api/spots", methods=["GET"])
def parking_status():
    occupied_entry_car = collection.count_documents({"zona": "Zona 1", "vehicle": "coche"})
    occupied_exit_car = collection.count_documents({"zona": "Zona 2", "vehicle": "coche"})
    
    occupied_entry_moto = collection.count_documents({"zona": "Zona 1", "vehicle": "moto"})
    occupied_exit_moto = collection.count_documents({"zona": "Zona 2", "vehicle": "moto"})

    available_entry_spots_car = TOTAL_ENTRY_SPOTS_CAR - occupied_entry_car
    available_exit_spots_car = TOTAL_EXIT_SPOTS_CAR - occupied_exit_car
    
    available_entry_spots_moto = TOTAL_ENTRY_SPOTS_MOTO - occupied_entry_moto
    available_exit_spots_moto = TOTAL_EXIT_SPOTS_MOTO - occupied_exit_moto

    return jsonify({
        "entrada_coche": available_entry_spots_car, 
        "salida_coche": available_exit_spots_car,
        "entrada_moto": available_entry_spots_moto, 
        "salida_moto": available_exit_spots_moto
    })
