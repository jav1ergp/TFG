from flask import Blueprint, jsonify, request
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['parking']
collection = db['vehicles']

parking_bp = Blueprint("parking", __name__)

TOTAL_PLAZAS_ENTRADA = 10 # Plazas total 
TOTAL_PLAZAS_SALIDA = 15 # Plazas total

def contar_coches_en_zona(zona):
    """Cuenta cuántos coches están actualmente en la zona (sin date_out)."""
    return collection.count_documents({"zona": zona, "date_out": None})

@parking_bp.route("/api/plazas", methods=["GET"])
def parking_status():
    # Contar cuántos coches hay en cada zona según el campo "zona"
    ocupados_entrada = collection.count_documents({"zona": "entrada"})
    ocupados_salida = collection.count_documents({"zona": "fuera"})

    plazas_libres_entrada = TOTAL_PLAZAS_ENTRADA - ocupados_entrada
    plazas_libres_salida = TOTAL_PLAZAS_SALIDA - ocupados_salida

    return jsonify({
        "entrada": plazas_libres_entrada, 
        "fuera": plazas_libres_salida
    })