from pymongo import MongoClient  
from datetime import datetime  
import sys  
import os  
  
# Añadir el directorio padre al path para poder importar los módulos  
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
  
from backend.models.plate import Plate
from backend.models.log import Log  
from backend.services.db_service import handle_plate, find_similar_plate, get_latest_plate_record, update_plate_zona
from config.config import MONGO_URI, MONGO_PARKING
  
# Conexión a la base de datos  
client = MongoClient(MONGO_URI)  
db = client['parking']  
collection = db['vehicles']  
  
from pymongo import MongoClient    
from datetime import datetime    
import sys    
import os    
    
# Añadir el directorio padre al path para poder importar los módulos    
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))    
    
from backend.models.plate import Plate  
from backend.models.log import Log    
# Importar tu nueva implementación en lugar de la del db_service actual  
from config.config import MONGO_URI, MONGO_PARKING  
    
    
from pymongo import MongoClient
from datetime import datetime
from backend.models.plate import Plate
from backend.models.log import Log
from config.config import MONGO_URI, MONGO_PARKING

client = MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['vehicles']


def clear_test_data():    
    """Limpia los datos de prueba de la base de datos"""    
    print("Limpiando datos de prueba...")    
    collection.delete_many({"plate": {"$in": ["1111AAA", "1112AAA", "1122AAA", "1122BBB", "2222BBB", "2223BBB", "3333CCC"]}})    
    print("Datos de prueba eliminados.")    
    
def setup_test_data():    
    """Configura datos de prueba en la base de datos"""    
    print("Configurando datos de prueba...")    
    # Crear placas de prueba en Zona 1 (actualizado)  
    plates_data = [    
        {    
            "plate": "1112AAA",    
            "confidence": 0.95,    
            "vehicle": "coche",    
            "date_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),    
            "date_out": None,    
            "zona": "Zona 1"  # Actualizado  
        },    
        {    
            "plate": "1122AAA",    
            "confidence": 0.90,    
            "vehicle": "coche",    
            "date_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),    
            "date_out": None,    
            "zona": "Zona 1"  # Actualizado  
        },    
        {    
            "plate": "1122BBB",    
            "confidence": 0.85,    
            "vehicle": "coche",    
            "date_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),    
            "date_out": None,    
            "zona": "Zona 1"  # Actualizado  
        },    
        {    
            "plate": "2223BBB",    
            "confidence": 0.92,    
            "vehicle": "moto",    
            "date_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),    
            "date_out": None,    
            "zona": "Zona 1"  # Actualizado  
        }    
    ]    
        
    collection.insert_many(plates_data)    
    print("Datos de prueba insertados correctamente.")    
    
def test_find_similar_plate():    
    """Prueba la función find_similar_plate"""    
    print("\n=== Prueba de find_similar_plate ===")    
        
    # Caso 1: Buscar matrícula similar a 1111AAA (debe encontrar 1112AAA - 6 caracteres iguales)    
    similar = find_similar_plate("1111AAA", "Zona 2", "coche")  # Actualizado zona  
    if similar:    
        print(f"✅ Encontrada matrícula similar a 1111AAA: {similar['plate']} (Esperado: 1112AAA)")    
        print(f"   Coincidencia: 6 de 7 caracteres iguales")    
    else:    
        print("❌ No se encontró matrícula similar a 1111AAA")    
        
    # Caso 2: Buscar matrícula similar a 2222BBB (debe encontrar 2223BBB - 6 caracteres iguales)    
    similar = find_similar_plate("2222BBB", "Zona 2", "moto")  # Actualizado zona  
    if similar:    
        print(f"✅ Encontrada matrícula similar a 2222BBB: {similar['plate']} (Esperado: 2223BBB)")    
        print(f"   Coincidencia: 6 de 7 caracteres iguales")    
    else:    
        print("❌ No se encontró matrícula similar a 2222BBB")    
        
    # Caso 3: Buscar matrícula similar a 3333CCC (no debería encontrar ninguna)    
    similar = find_similar_plate("3333CCC", "Zona 2", "coche")  # Actualizado zona  
    if not similar:    
        print("✅ Correctamente no se encontró matrícula similar a 3333CCC")    
    else:    
        print(f"❌ Se encontró matrícula similar a 3333CCC cuando no debería: {similar['plate']}")    
        
    # Caso 4: Buscar matrícula con solo 5 caracteres iguales (1112AAA vs 1122AAA)    
    similar = find_similar_plate("8812AAA", "Zona 2", "coche")  # Actualizado zona  
    if similar:    
        print(f"✅ Encontrada matrícula con 5 caracteres iguales: {similar['plate']}")    
        print(f"   Coincidencia: 5 de 7 caracteres iguales")    
    else:    
        print("❌ No se encontró matrícula con 5 caracteres iguales cuando debería")    
        
    # Caso 5: Buscar matrícula con diferente tipo de vehículo    
    similar = find_similar_plate("1112AAA", "Zona 2", "moto")  # Actualizado zona  
    if not similar:    
        print("✅ Correctamente no se encontró matrícula de diferente tipo de vehículo")    
    else:    
        print(f"❌ Se encontró matrícula de diferente tipo de vehículo cuando no debería: {similar['plate']}")    
        
    # Caso 6: Probar búsqueda para salida (fuera)  
    similar = find_similar_plate("1112AAA", "fuera", "coche")    
    if similar:    
        print(f"✅ Encontrada matrícula para salida: {similar['plate']}")    
    else:    
        print("❌ No se encontró matrícula para salida")  
    
def test_handle_plate_with_similar():    
    """Prueba la función handle_plate con matrículas similares"""    
    print("\n=== Prueba de handle_plate con matrículas similares ===")    
        
    # Caso 1: Detectar matrícula 1111AAA en zona (debería encontrar 1112AAA y actualizarla)    
    plate1 = Plate("1111AAA", 0.95, "coche", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Zona 1")  # Actualizado  
    print("\nPrueba 1: Detectando 1111AAA en zona (similar a 1112AAA)")    
    handle_plate(plate1, "Zona")    
        
    # Verificar que 1112AAA se actualizó a zona "Zona 2"    
    updated_record = get_latest_plate_record("1112AAA")    
    if updated_record and updated_record["zona"] == "Zona 2":  # Actualizado  
        print(f"✅ La matrícula 1112AAA se actualizó correctamente a zona 'Zona 2'")    
    else:    
        print("❌ La matrícula 1112AAA no se actualizó correctamente")    
        
    # Primero mover 2223BBB a Zona 2 para poder probar la salida  
    moto_record = get_latest_plate_record("2223BBB")  
    if moto_record:  
        update_plate_zona(moto_record["_id"], "Zona 2")  
        print("Moviendo 2223BBB a Zona 2 para prueba de salida")  
      
    # Caso 2: Detectar matrícula 2222BBB en salida (debería encontrar 2223BBB y marcarla como salida)    
    plate2 = Plate("2222BBB", 0.92, "moto", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Zona 1")  # Actualizado  
    print("\nPrueba 2: Detectando 2222BBB en salida (similar a 2223BBB)")    
    handle_plate(plate2, "Salida")    
        
    # Verificar que 2223BBB se marcó como salida    
    updated_record = get_latest_plate_record("2223BBB")    
    if updated_record and updated_record["date_out"] is not None:    
        print(f"✅ La matrícula 2223BBB se marcó correctamente como salida")    
    else:    
        print("❌ La matrícula 2223BBB no se marcó correctamente como salida")    
        
    # Caso 3: Probar con una matrícula que no tiene similares suficientes    
    plate3 = Plate("3333CCC", 0.95, "coche", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Zona 1")  # Actualizado  
    print("\nPrueba 3: Detectando 3333CCC en zona (no debería encontrar similares)")    
    handle_plate(plate3, "Zona")    
        
    # Verificar que se registra el error    
    print("✅ Prueba completada - verificar mensaje de error en la consola")    
    
def test_vehicle_type_check():    
    """Prueba la verificación del tipo de vehículo"""    
    print("\n=== Prueba de verificación del tipo de vehículo ===")    
        
    # Añadir una matrícula similar pero de diferente tipo    
    collection.insert_one({    
        "plate": "1112BBB",  # Similar a 1112AAA pero con diferente final    
        "confidence": 0.95,    
        "vehicle": "moto",  # Diferente tipo de vehículo    
        "date_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),    
        "date_out": None,    
        "zona": "Zona 1"  # Actualizado  
    })    
        
    # Caso 1: Buscar matrícula similar pero con diferente tipo de vehículo    
    similar = find_similar_plate("1112AAA", "Zona 2", "coche")  # Actualizado zona  
    if similar and similar["vehicle"] == "coche":    
        print(f"✅ Correctamente encontró solo matrículas del mismo tipo de vehículo: {similar['plate']}")    
    else:    
        print("❌ No se filtró correctamente por tipo de vehículo")    
        
    # Limpiar la matrícula adicional    
    collection.delete_one({"plate": "1112BBB"})    
  
def test_new_features():  
    """Prueba las nuevas características de tu implementación"""  
    print("\n=== Prueba de nuevas características ===")  
      
    # Probar entrada duplicada con logging  
    plate_dup = Plate("1112AAA", 0.95, "coche", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Zona 1")  
    print("Probando entrada duplicada...")  
    handle_plate(plate_dup, "Entrada")  
      
    # Probar salida sin estar en Zona 2  
    plate_wrong_zone = Plate("1122AAA", 0.90, "coche", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Zona 1")  
    print("Probando salida desde zona incorrecta...")  
    handle_plate(plate_wrong_zone, "Salida")  
      
    print("✅ Pruebas de nuevas características completadas")  
    
def main():    
    """Función principal para ejecutar todas las pruebas"""    
    print("=== INICIANDO PRUEBAS DEL SISTEMA DE DETECCIÓN DE MATRÍCULAS SIMILARES (VERSIÓN ACTUALIZADA) ===\n")    
        
    # Limpiar datos de pruebas anteriores    
    clear_test_data()    
        
    # Configurar datos de prueba    
    setup_test_data()    
        
    # Ejecutar pruebas    
    test_find_similar_plate()    
    test_handle_plate_with_similar()    
    test_vehicle_type_check()  
    test_new_features()  # Nueva función de prueba  
        
    # Limpiar al finalizar    
    clear_test_data()    
        
    print("\n=== PRUEBAS COMPLETADAS ===")    
    
if __name__ == "__main__":    
    main()