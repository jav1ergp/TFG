import bcrypt
import re

class User:
    def __init__(self, email, password_hash, admin=False):
        self.email = email
        self.admin = admin
        self.password = password_hash

    @classmethod
    def create(cls, email, plain_password, admin=False):
        """Crea un nuevo usuario con contraseña hasheada"""
        password_hash = bcrypt.hashpw(
            plain_password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')  # Convertir a string para almacenar
        return cls(email, password_hash, admin)
    
    def check_password(self, plain_password):
        """Verifica la contraseña contra el hash almacenado"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            self.password.encode('utf-8')  # Convertir string guardado a bytes
        )

    @staticmethod
    def is_valid_email(email):
        email_valid = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(email_valid, email)

        if match is not None: # Si coincide es valido
            return True
        else:
            return False