from flask import Blueprint, Response
from services.car_detection import generate_frames
from config import URL_ENTRADA, URL_ZONA, URL_SALIDA

bp = Blueprint('plate_detection', __name__)


@bp.route('/car_detection', methods=['GET'])
def detect_plate_route():
    return Response(generate_frames(URL_ENTRADA, URL_ZONA, URL_SALIDA))
