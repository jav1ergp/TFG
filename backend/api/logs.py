# Logs, paginación
from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from config.config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
log_collection = db['logs']

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/api/logs", methods=["GET"])
def get_logs():
    """Devuelve una lista paginada de logs ordenados por fecha (timestamp) descendente"""
    page = int(request.args.get("page"))  # Página
    limit = int(request.args.get("limit"))  # Numero de registros por pagina
    
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
