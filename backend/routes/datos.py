from flask import Blueprint, jsonify
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["parking"]
collection = db["vehicles"]

data_bp = Blueprint("data", __name__)

@data_bp.route("/api/data", methods=["GET"])
def get_data():
    logs = collection.find().sort("date_in", -1)

    logs_list = []
    for log in logs:
        logs_list.append({
            "id": str(log["_id"]),
            "plate": log.get("plate"),
            "confidence": log.get("confidence"),
            "vehicle": log.get("vehicle"),
            "zona": log.get("zona"),
            "date_in": log.get("date_in"),
            "date_out": log.get("date_out", "Pendiente")
        })

    return jsonify(logs_list)
