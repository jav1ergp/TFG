import bcrypt
import re

class User:
    def __init__(self, email, password, admin=False):
        self.email = email
        self.admin = admin
        self.password = password

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    @staticmethod
    def is_valid_email(email):
        email_valid = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(email_valid, email)

        if match is not None: # Si coincide es valido
            return True
        else:
            return False