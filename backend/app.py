import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from flask import Flask
from backend.api import plazas, datos, logs
from backend.services.car_detection import start_detection
from config.back_config import URL_ENTRADA, URL_ZONA, URL_SALIDA


app = Flask(__name__)

# Registrar rutas
app.register_blueprint(plazas.parking_bp)
app.register_blueprint(datos.data_bp)
app.register_blueprint(logs.logs_bp)

start_detection(URL_ENTRADA, URL_ZONA, URL_SALIDA)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
