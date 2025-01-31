from flask import Flask
from routes import video_feed, plate_detection

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(video_feed.bp)
app.register_blueprint(plate_detection.bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
