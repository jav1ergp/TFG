import cv2
from fast_alpr import ALPR

# Inicializar ALPR
alpr = ALPR(
    detector_model="yolo-v9-t-384-license-plate-end2end",
    ocr_model="global-plates-mobile-vit-v2-model",
    ocr_providers=['CPUExecutionProvider'],
    detector_providers=['CPUExecutionProvider']
)

def procesar_imagen(ruta_imagen, mostrar=True, guardar=False, ruta_salida="salida.jpg"):
    # Leer la imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("No se pudo leer la imagen.")
        return

    # Procesar la imagen con ALPR
    resultados = alpr.predict(imagen)

    # Dibujar las predicciones sobre la imagen
    imagen_anotada = alpr.draw_predictions(imagen)

    # Añadir texto con la matrícula si hay resultado
    if resultados:
        ocr_resultado = resultados[0].ocr
        texto_matricula = ocr_resultado.text
        confianza = round(ocr_resultado.confidence, 2)

        # Coordenadas del recuadro
        x1, y1, x2, y2 = resultados[0].bbox
        etiqueta = f"{texto_matricula} ({confianza})"

        # Dibujar etiqueta
        cv2.rectangle(imagen_anotada, (x1, y1 - 30), (x2, y1), (0, 255, 0), -1)
        cv2.putText(imagen_anotada, etiqueta, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

        print(f"Matrícula detectada: {texto_matricula} (Confianza: {confianza})")
    else:
        print("No se detectó ninguna matrícula.")

    # Mostrar la imagen si se desea
    if mostrar:
        cv2.imshow("Resultado ALPR", imagen_anotada)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Guardar la imagen si se desea
    if guardar:
        cv2.imwrite(ruta_salida, imagen_anotada)
        print(f"Imagen guardada en {ruta_salida}")


# Ejemplo de uso
if __name__ == "__main__":
    procesar_imagen("ejemplo.jpg", mostrar=True, guardar=True)
