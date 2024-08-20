import bcrypt

class PasswordUtil:
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password: str, hashed: str):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
