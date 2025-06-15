import pymongo
from backend.models.user import User
from config.config import MONGO_URI, MONGO_PARKING

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_PARKING]
collection = db['users']

def register_user(email, plain_password):
    """Registra un nuevo usuario si el email es valido y no existe en la base de datos"""
    if not User.is_valid_email(email):
        return "invalid_email"

    if collection.find_one({"email": email}):
        return "email_exists"

    user = User.create(email, plain_password)

    save_user_to_db(user)

    return "success"

def verify_login(email, plain_password):
    """Verifica las credenciales del usuario comparando la contraseña con la almacenada"""
    user_data = collection.find_one({"email": email})
    
    if user_data:
        user = User(user_data["email"], user_data["password"], user_data["admin"])
        return user.check_password(plain_password)
    
    return False

def is_admin(email):
    """Devuelve True si el usuario con ese email es administrador"""
    user_data = collection.find_one({"email": email})
    
    is_user_admin = user_data["admin"]
    
    return is_user_admin

def save_user_to_db(user):
    """Guarda User en la base de datos"""
    user_data = {
        "email": user.email,
        "password": user.password,
        "admin": user.admin
    }
    
    collection.insert_one(user_data)