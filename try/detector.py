import cv2
from fast_alpr import ALPR
from pymongo import MongoClient
from datetime import datetime
#mongod para empezar la base de datos
#mongosh para ver la base de datos
#use alpr show collections db.plates.find()
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client['alpr'] #nombre de la base de datos
collection = db['plates'] #nombre de la coleccion de la base de datos
# Initialize the ALPR
alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
    ocr_providers=['CPUExecutionProvider'],
    detector_providers=['CPUExecutionProvider']
)

# Load the image
image_path = "car2.jpg"
frame = cv2.imread(image_path)

# Get the ALPR results
alpr_results = alpr.predict(frame)

# Extract the license plate text from the results
license_plate_text = ""
confidence = 0.0
if alpr_results:  # Check if there are any results
    ocr_result = alpr_results[0].ocr  #1 matricula y conf
    license_plate_text = ocr_result.text
    confidence = round(ocr_result.confidence, 2)
#for result in alpr_results:  #muchas matriculas
#    ocr_result = result.ocr
#    if ocr_result and ocr_result.text:
#        license_plate_text += ocr_result.text + "\n"

# Draw predictions on the image
annotated_frame = alpr.draw_predictions(frame)
print(confidence)
if license_plate_text:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    plate_data = {
        "plate": license_plate_text,
        "confidence": confidence,
        "date_in": current_time_str,
        "date_out": None
    }
    collection.insert_one(plate_data)
    print(f"Matrícula detectada: {license_plate_text} (Confianza: {confidence})")
    
results = collection.find()
one_result = collection.find_one({"license_plate": "2492JXL"})
for result in results: #los devuelve por la terminal
    print(result) #solo el campo de la matricula
# funcion leer placa
#guardar confidence
# hacer funcion validar placa
cv2.imshow("ALPR Result", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the detected license plate text
print("Detected License Plate Text:\n", license_plate_text)
# db.nombre_de_tu_coleccion.deleteMany({})
