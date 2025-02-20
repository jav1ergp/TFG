from flask import Blueprint, jsonify
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
collection = db['vehicles']

parking_bp = Blueprint("parking", __name__)

TOTAL_ENTRY_SPOTS = 10
TOTAL_EXIT_SPOTS = 15

@parking_bp.route("/api/spots", methods=["GET"])
def parking_status():
    occupied_entry = collection.count_documents({"zone": "entrada"})
    occupied_exit = collection.count_documents({"zone": "salida"})

    available_entry_spots = TOTAL_ENTRY_SPOTS - occupied_entry
    available_exit_spots = TOTAL_EXIT_SPOTS - occupied_exit

    return jsonify({
        "entrada": available_entry_spots, 
        "salida": available_exit_spots
    })
