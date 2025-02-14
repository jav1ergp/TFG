from flask import Blueprint, jsonify
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["parking"]
collection = db["vehicles"]

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/api/logs", methods=["GET"])
def get_logs():
    logs = collection.find().sort("fecha_entrada", -1)

    logs_list = []
    for log in logs:
        logs_list.append({
            "id": str(log["_id"]),
            "plate": log.get("plate", "N/A"),
            "confidence": log.get("confidence", "Desconocido"),
            "zona": log.get("zona", "N/A"),
            "date_in": log.get("date_in", "N/A"),
            "date_out": log.get("date_out", "Pendiente")
        })

    return jsonify(logs_list)
