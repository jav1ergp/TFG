from flask import Flask
from routes import plate_detection, plazas, datos


app = Flask(__name__)

# Registrar rutas
app.register_blueprint(plate_detection.bp)
app.register_blueprint(plazas.parking_bp)
app.register_blueprint(datos.logs_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
