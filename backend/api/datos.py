from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from config.back_config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["parking"]
collection = db["vehicles"]

data_bp = Blueprint("data", __name__)

@data_bp.route("/api/data", methods=["GET"])
def get_data():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    sort_field = request.args.get("sort", "date_in")
    sort_order = int(request.args.get("order", -1))
    search = request.args.get("search", None)

    skip = (page - 1) * limit

    # Construir filtro de búsqueda
    query_filter = {}
    if search:
        query_filter["plate"] = search
        
    # Ordenación con filtro
    if sort_field != "date_in":
        logs = collection.find(query_filter).sort([
            (sort_field, sort_order),
            ("date_in", -1)
        ])
    else:
        logs = collection.find(query_filter).sort("date_in", sort_order)

    logs = logs.skip(skip).limit(limit)
    
    # Contar total de documentos CON filtro
    total = collection.count_documents(query_filter)
    
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

    return jsonify({
        "data": logs_list,
        "total": total,
        "page": page,
        "limit": limit
    })