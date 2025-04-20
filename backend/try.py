import pymongo
from config import MONGO_URI  # Asegúrate de que el archivo config.py contiene MONGO_URI correctamente

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["parking"]
    print("✅ Conexión exitosa a MongoDB")

    # Listar las colecciones como prueba
    print("📂 Colecciones en la BD:", db.list_collection_names())

    # Probar lectura de usuarios
    users_collection = db["users"]
    user = users_collection.find_one()
    print("👤 Usuario encontrado:", user if user else "No hay usuarios en la base de datos.")

except Exception as e:
    print("❌ Error al conectar a MongoDB:", e)
