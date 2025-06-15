# Datos, paginación, ordenación, filtros y filtrado por matrícula.

from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from config.config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db["vehicles"]

data_bp = Blueprint("data", __name__)

@data_bp.route("/api/data", methods=["GET"])
def get_data():
    """Devuelve una lista paginada de registros de vehículos desde la base de datos"""
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    sort_field = request.args.get("sort", "date_in")
    sort_order = int(request.args.get("order", -1))
    search = request.args.get("search", None)
    date_out_filter = request.args.get("date_out", None)  

    skip = (page - 1) * limit

    # Construir filtro de búsqueda
    query_filter = {}
    if search:
        query_filter["plate"] = search
        
    if date_out_filter == "null":  
        query_filter["date_out"] = None  
        
    # Ordenación con filtro
    if sort_field != "date_in":
        dates = collection.find(query_filter).sort([
            (sort_field, sort_order),
            ("date_in", -1)
        ])
    else:
        dates = collection.find(query_filter).sort("date_in", sort_order)

    dates = dates.skip(skip).limit(limit)
    
    # Contar total de documentos CON filtro
    total = collection.count_documents(query_filter)
    
    dates_list = []
    for date in dates:
        dates_list.append({
            "id": str(date["_id"]),
            "plate": date.get("plate"),
            "confidence": date.get("confidence"),
            "vehicle": date.get("vehicle"),
            "zona": date.get("zona"),
            "date_in": date.get("date_in"),
            "date_out": date.get("date_out")
        })

    return jsonify({
        "data": dates_list,
        "total": total,
        "page": page,
        "limit": limit
    })