from flask import Blueprint, jsonify
from services.car_detection import start_detection
from config import URL_ENTRADA, URL_ZONA, URL_SALIDA

bp = Blueprint('plate_detection', __name__)


@bp.route('/car_detection', methods=['GET'])
def detect_plate_route():
    start_detection(URL_ENTRADA, URL_ZONA, URL_SALIDA)
    return jsonify({'status': 'start_detection'})
