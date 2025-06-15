# API para registrar plates

from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from backend.models.plate import Plate
from datetime import datetime
from config.config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

register_plate_bp  = Blueprint("register_plate", __name__)

@register_plate_bp.route("/api/register", methods=["POST"])
def register_plate():
    """Registra una nueva entrada de vehículo en el parking si no está ya dentro"""
    data = request.json
    plate_text = data.get("plate")
    zona = data.get("zona")
    vehicle = data.get("vehicle")

    last_entry = collection.find_one(
        {"plate": plate_text},
        sort=[("date_in", -1)]
    )

    if last_entry and last_entry.get("zona") != "fuera":
        return jsonify({"error": "La matrícula ya está registrada y no ha salido del parking."}), 404
    
    plate = Plate(
        license_plate_text=plate_text,
        confidence=1.0,
        vehicle=vehicle,
        date_in=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        zona=zona
    )

    Plate.save_plate(plate)

    return "", 200