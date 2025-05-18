from ultralytics import YOLO
import cv2
import sys

# Clases del dataset COCO que son vehículos
CLASES_VEHICULOS = ["car", "truck", "bus", "motorbike", "bicycle"]

# Cargar modelo YOLOv8n
modelo = YOLO("yolov8n.pt")

def detectar_vehiculos(ruta_imagen, mostrar=True, guardar=False, ruta_salida="vehiculos_detectados.jpg"):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"No se pudo cargar la imagen: {ruta_imagen}")
        return

    # Realizar la predicción
    resultados = modelo.predict(source=imagen, save=False, verbose=False)[0]

    for caja, clase_id, conf in zip(resultados.boxes.xyxy, resultados.boxes.cls, resultados.boxes.conf):
        nombre_clase = modelo.names[int(clase_id)]
        if nombre_clase in CLASES_VEHICULOS:
            x1, y1, x2, y2 = map(int, caja)
            etiqueta = f"{nombre_clase} ({conf:.2f})"

            cv2.rectangle(imagen, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.rectangle(imagen, (x1, y1 - 25), (x1 + 150, y1), (255, 0, 0), -1)
            cv2.putText(imagen, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    if mostrar:
        cv2.imshow("Vehículos detectados", imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if guardar:
        cv2.imwrite(ruta_salida, imagen)
        print(f"Imagen guardada en {ruta_salida}")

# Uso por consola
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        detectar_vehiculos(ruta, mostrar=True, guardar=True)
    else:
        print("Uso: python detectar_vehiculos.py <ruta_imagen>")
