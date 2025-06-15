# API para eliminar plates, si se manda all se eliminan todas, si se manda una especifica se elimina esa

from flask import Blueprint, jsonify
from pymongo import MongoClient
from config.config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']

delete_plate_bp  = Blueprint("delete_plate", __name__)

@delete_plate_bp.route("/api/delete/<plate>", methods=["DELETE"])  
def delete_plate(plate):
    """Elimina registros de vehículos según el valor de la matrícula."""
    if plate == "all":
        collection.delete_many({
            "$or": [
                {"date_out": None},
            ]
        })
        return "", 200
    
    result = collection.delete_one({"plate": plate})  
      
    if result:
        return "", 200
    else:  
        return jsonify({"error": "No se encontro la matricula a eliminar."}), 404