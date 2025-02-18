from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
log_collection = db['logs']

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/api/logs", methods=["GET"])
def get_logs():
    page = int(request.args.get("page", 1))  # Página (por defecto 1)
    limit = int(request.args.get("limit", 10))  # Número de registros por página (por defecto 10)
    skip = (page - 1) * limit  # Calcular el desplazamiento

    logs = log_collection.find().sort("date_in", -1).skip(skip).limit(limit)

    logs_list = [
        {
            "id": str(log["_id"]),
            "action": log["action"],
            "description": log["description"],
            "plate": log["plate"],
            "zone": log["zone"],
            "date_in": log["date_in"].isoformat(),
            "date_out": log["date_out"].isoformat(),
            "timestamp": log["timestamp"].isoformat()
        }
        for log in logs
    ]

    return jsonify(logs_list), 200
