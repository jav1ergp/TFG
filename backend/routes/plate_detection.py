from flask import Blueprint, Response
from services.car_detection import generate_frames

bp = Blueprint('plate_detection', __name__)


@bp.route('/car_detection', methods=['GET'])
def detect_plate_route():
    """
    Endpoint para iniciar la detección de coches y devolver el frame y datos relevantes.
    """

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
