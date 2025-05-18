import cv2
from fast_alpr import ALPR
import sys

# Inicializar ALPR
alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
    ocr_providers=["CPUExecutionProvider"],
    detector_providers=["CPUExecutionProvider"]
)

def procesar_imagen(ruta_imagen, mostrar=True, guardar=False, ruta_salida="salida.jpg"):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"No se pudo leer la imagen: {ruta_imagen}")
        return

    # Ejecutar ALPR
    resultados = alpr.predict(imagen)

    if not resultados:
        print("No se detectó ninguna matrícula.")
        return

    for resultado in resultados:
        texto = resultado.ocr.text
        confianza = round(resultado.ocr.confidence, 2)
        bbox = resultado.detection.bounding_box
        x1, y1, x2, y2 = bbox.x1, bbox.y1, bbox.x2, bbox.y2

        # Dibujar rectángulo y texto
        cv2.rectangle(imagen, (x1, y1), (x2, y2), (0, 255, 0), 2)
        etiqueta = f"{texto} ({confianza}%)"
        cv2.rectangle(imagen, (x1, y1 - 25), (x1 + 200, y1), (0, 255, 0), -1)
        cv2.putText(imagen, etiqueta, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        print(f"Matrícula detectada: {texto} (Confianza: {confianza})")

    if mostrar:
        cv2.imshow("Resultado ALPR", imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if guardar:
        cv2.imwrite(ruta_salida, imagen)
        print(f"Imagen guardada como {ruta_salida}")

# Ejecutar desde consola
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        procesar_imagen(ruta, mostrar=True, guardar=True)
    else:
        print("Uso: python coche.py <ruta_imagen>")
