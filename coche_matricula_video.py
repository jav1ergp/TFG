import cv2
from ultralytics import YOLO
from fast_alpr import ALPR
import sys
import os

# Clases de interés
CLASES_VEHICULOS = ["car", "truck", "bus", "motorbike", "bicycle"]

# Cargar modelos
modelo_vehiculos = YOLO("yolov8n.pt")
alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
    ocr_providers=["CPUExecutionProvider"],
    detector_providers=["CPUExecutionProvider"]
)

def procesar_video(ruta_video, ruta_salida="salida_detectada.mp4", mostrar=False):
    cap = cv2.VideoCapture(ruta_video)
    if not cap.isOpened():
        print(f"No se pudo abrir el video: {ruta_video}")
        return

    # Configurar salida
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    nombre_codec = cv2.VideoWriter_fourcc(*"mp4v")
    salida = cv2.VideoWriter(ruta_salida, nombre_codec, fps, (ancho, alto))

    frame_actual = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detectar vehículos
        resultados_vehiculos = modelo_vehiculos.predict(source=frame, save=False, verbose=False)[0]
        for caja, clase_id, conf in zip(resultados_vehiculos.boxes.xyxy, resultados_vehiculos.boxes.cls, resultados_vehiculos.boxes.conf):
            nombre_clase = modelo_vehiculos.names[int(clase_id)]
            if nombre_clase in CLASES_VEHICULOS:
                x1, y1, x2, y2 = map(int, caja)
                etiqueta = f"{nombre_clase} ({conf:.2f})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.rectangle(frame, (x1, y1 - 25), (x1 + 150, y1), (255, 0, 0), -1)
                cv2.putText(frame, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Detectar matrículas
        resultados_matriculas = alpr.predict(frame)
        for resultado in resultados_matriculas:
            texto = resultado.ocr.text
            confianza = round(resultado.ocr.confidence, 2)
            bbox = resultado.detection.bounding_box
            x1, y1, x2, y2 = bbox.x1, bbox.y1, bbox.x2, bbox.y2
            etiqueta = f"{texto} ({confianza}%)"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1 - 25), (x1 + 200, y1), (0, 255, 0), -1)
            cv2.putText(frame, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        # Mostrar si se desea
        if mostrar:
            cv2.imshow("Detecciones", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        salida.write(frame)
        frame_actual += 1
        print(f"Procesando frame {frame_actual}/{total_frames}", end='\r')

    cap.release()
    salida.release()
    cv2.destroyAllWindows()
    print(f"\nVideo procesado y guardado en: {ruta_salida}")

# Uso desde consola
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        entrada = sys.argv[1]
        salida = sys.argv[2] if len(sys.argv) >= 3 else "salida_detectada.mp4"
        procesar_video(entrada, ruta_salida=salida, mostrar=True)
    else:
        print("Uso: python detectar_video.py <ruta_video> [salida]")
