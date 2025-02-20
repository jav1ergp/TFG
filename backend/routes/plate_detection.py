from flask import Blueprint, Response
from services.car_detection import generate_frames

bp = Blueprint('plate_detection', __name__)


@bp.route('/car_detection', methods=['GET'])
def detect_plate_route():
    url_pc = 0
    url_laptop = "http://192.168.68.56:5010/video_feed"
    url_movil = "http://192.168.68.51:8080/video"
    
    return Response(generate_frames(url_pc, url_laptop, url_movil), mimetype='multipart/x-mixed-replace; boundary=frame')
