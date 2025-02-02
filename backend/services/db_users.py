import pymongo
import bcrypt
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['parking']
collection = db['users']

def is_valid_email(email):
    # Expresión regular para validar el formato de un correo electrónico
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def register_user(email, password):
    if not is_valid_email(email):
        return "invalid_email"  # El correo tiene un formato inválido

    # Verificar si el correo electrónico ya está registrado
    if collection.find_one({"email": email}):
        return "email_exists"  # El correo ya está registrado

    # Cifrar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insertar el nuevo usuario en la base de datos
    collection.insert_one({
        "email": email,
        "password": hashed_password
    })
    return "success"  # Registro exitoso


def verify_login(email, password):
    # Buscar el usuario en la base de datos usando el correo electrónico
    user = collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return True
    return False
    
def is_admin(email):
    user = collection.find_one({"email": email})
    if user and user.get('admin') == True:
        return True
    return False
    