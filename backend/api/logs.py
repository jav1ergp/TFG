from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from config.back_config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
log_collection = db['logs']

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/api/logs", methods=["GET"])
def get_logs():
    page = int(request.args.get("page", 1))  # Página (por defecto 1)
    limit = int(request.args.get("limit", 10))  # Número de registros por página (por defecto 10)
    
    skip = (page - 1) * limit  # Calcular el desplazamiento

    query_filter = {}
    
    total = log_collection.count_documents(query_filter)

    logs = log_collection.find(query_filter).sort("timestamp", -1).skip(skip).limit(limit)
    
    logs_list = []
    for log in logs:
        logs_list.append({
            "id": str(log["_id"]),
            "action": log["action"],
            "description": log["description"],
            "plate": log["plate"],
            "zona": log["zona"],
            "timestamp": log["timestamp"]
        })

    return jsonify({
        "data": logs_list,
        "total": total,
        "page": page,
        "limit": limit
    })
