import cv2
import sys
from ultralytics import YOLO
from fast_alpr import ALPR
import math

# Clases del dataset COCO que son vehículos
CLASES_VEHICULOS = ["car", "truck", "bus", "motorbike", "bicycle"]

# Cargar modelos
modelo_vehiculos = YOLO("yolov8n.pt")
alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
    ocr_providers=["CPUExecutionProvider"],
    detector_providers=["CPUExecutionProvider"]
)

def centro(bbox):
    """Devuelve el centro (x, y) del bounding box"""
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) // 2, (y1 + y2) // 2)

def distancia(p1, p2):
    """Calcula la distancia euclidiana entre dos puntos"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def detectar_vehiculos_y_matriculas(ruta_imagen, mostrar=True, guardar=False, ruta_salida="salida_combinada.jpg"):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"No se pudo cargar la imagen: {ruta_imagen}")
        return

    # --- DETECCIÓN DE VEHÍCULOS ---
    resultados_vehiculos = modelo_vehiculos.predict(source=imagen, save=False, verbose=False)[0]
    vehiculos_filtrados = []
    
    for caja, clase_id, conf in zip(resultados_vehiculos.boxes.xyxy, resultados_vehiculos.boxes.cls, resultados_vehiculos.boxes.conf):
        nombre_clase = modelo_vehiculos.names[int(clase_id)]
        if nombre_clase in CLASES_VEHICULOS:
            vehiculos_filtrados.append((conf, caja, nombre_clase))

    if not vehiculos_filtrados:
        print("No se detectaron vehículos relevantes.")
        return

    # Vehículo con mayor confianza
    conf, caja, nombre_clase = max(vehiculos_filtrados, key=lambda x: x[0])
    x1, y1, x2, y2 = map(int, caja)
    centro_vehiculo = centro((x1, y1, x2, y2))
    print(f"Vehículo detectado: {nombre_clase} (Confianza: {conf:.2f})")

    # Dibujar vehículo
    etiqueta = f"{nombre_clase} ({conf:.2f})"
    cv2.rectangle(imagen, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.rectangle(imagen, (x1, y1 - 25), (x1 + 150, y1), (255, 0, 0), -1)
    cv2.putText(imagen, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # --- DETECCIÓN DE MATRÍCULAS ---
    resultados_matriculas = alpr.predict(imagen)
    matricula_mas_cercana = None
    distancia_minima = float('inf')

    for resultado in resultados_matriculas:
        texto = resultado.ocr.text
        confianza_ocr = round(resultado.ocr.confidence, 2)
        bbox = resultado.detection.bounding_box
        x1_lp, y1_lp, x2_lp, y2_lp = bbox.x1, bbox.y1, bbox.x2, bbox.y2
        centro_matricula = centro((x1_lp, y1_lp, x2_lp, y2_lp))
        dist = distancia(centro_vehiculo, centro_matricula)

        if dist < distancia_minima:
            distancia_minima = dist
            matricula_mas_cercana = (texto, confianza_ocr, (x1_lp, y1_lp, x2_lp, y2_lp))

    if matricula_mas_cercana:
        texto, confianza, (x1, y1, x2, y2) = matricula_mas_cercana
        etiqueta = f"{texto} ({confianza}%)"
        cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(imagen, (x1, y1 - 25), (x1 + 200, y1), (0, 255, 0), -1)
        cv2.putText(imagen, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        print(f"Matrícula detectada: {texto} (Confianza: {confianza})")
    else:
        print("No se detectaron matrículas.")

    # Mostrar o guardar imagen
    if mostrar:
        cv2.imshow("Vehículo y Matrícula Detectados", imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if guardar:
        cv2.imwrite(ruta_salida, imagen)
        print(f"Imagen guardada como {ruta_salida}")

# Uso por consola
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        detectar_vehiculos_y_matriculas(ruta, mostrar=True, guardar=True)
    else:
        print("Uso: python detectar_combinado.py <ruta_imagen>")
