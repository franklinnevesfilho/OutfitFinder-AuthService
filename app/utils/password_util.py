import bcrypt

class PasswordUtil:
    """
    Password utility class

    Methods:
    --------
    hash_password(password: str) -> str
        Hash a password using bcrypt

    check_password(password: str, hashed: str) -> bool
        Check if a password matches a hashed password
    """

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def check_password(password: str, hashed: str):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
