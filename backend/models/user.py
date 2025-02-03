import bcrypt
import re

class User:
    def __init__(self, email, password, admin=False):
        self.email = email
        self.admin = admin
        self.password = password

    def check_password(self, password):
        """Verifica si la contraseña ingresada es correcta."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    @staticmethod
    def is_valid_email(email):
        """Verifica si el correo tiene un formato válido."""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None