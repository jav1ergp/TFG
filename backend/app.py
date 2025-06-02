import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from flask import Flask
from backend.api import plazas, datos, logs, register_plate, delete_plate
from backend.services.car_detection import start_detection
from config.config import URL_ENTRADA, URL_ZONA, URL_SALIDA


app = Flask(__name__)

# Registrar rutas
app.register_blueprint(plazas.parking_bp)
app.register_blueprint(datos.data_bp)
app.register_blueprint(logs.logs_bp)
app.register_blueprint(register_plate.register_plate_bp)
app.register_blueprint(delete_plate.delete_plate_bp)

start_detection(URL_ENTRADA, URL_ZONA, URL_SALIDA)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
