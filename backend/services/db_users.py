import pymongo
from models.user import User

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['parking']
collection = db['users']

def register_user(email, password):
    #if not User.is_valid_email(email):
    #    return "invalid_email"  # El correo tiene un formato inválido

    if collection.find_one({"email": email}):
        return "email_exists"

    user = User(email, password)

    save_user_to_db(user)

    return "success"

def verify_login(email, password):
    """Verifica si el usuario existe y la contraseña es correcta."""
    user_data = collection.find_one({"email": email})
    
    if user_data:
        user = User(user_data["email"], password=user_data["password"], admin=user_data.get("admin", False))
        return user.check_password(password)
    
    return False

def is_admin(email):
    """Verifica si el usuario tiene rol de administrador."""
    user_data = collection.find_one({"email": email})
    
    if user_data is None:
        return False
    
    is_user_admin = user_data.get("admin", False)
    
    return is_user_admin

def save_user_to_db(user):
    user_data = {
        "email": user.email,
        "password": user.password,
        "admin": user.admin
    }
    
    collection.insert_one(user_data)