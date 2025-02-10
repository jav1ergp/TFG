from flask import Blueprint, Response
from services.car_detection import generate_frames

bp = Blueprint('plate_detection', __name__)


@bp.route('/car_detection', methods=['GET'])
def detect_plate_route():
    """
    Endpoint para iniciar la detección de coches y devolver el frame y datos relevantes.
    """
    url_pc = 0
    #url_portatil = "http://192.168.1.107:5010/video_feed"
    url_portatil = "http://192.168.1.40:8080/video"
    
    return Response(generate_frames(url_pc, url_portatil), mimetype='multipart/x-mixed-replace; boundary=frame')
