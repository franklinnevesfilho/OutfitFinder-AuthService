from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt

class JwtUtil:
    _KEYS: dict[str] = {
        "private": None,
        "public": None
    }


    @classmethod
    def generate_keys(cls, key_size=2048):
        if cls._KEYS["private"] is not None or cls._KEYS["public"] is not None:
            raise ValueError("Keys already generated. Call 'generate_keys()' only once.")

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        cls._KEYS["private"] = private_key
        cls._KEYS["public"] = public_key

    @classmethod
    def get_private_key_pem(cls) -> bytes:
        if cls._KEYS["private"] is None:
            raise ValueError("Private key not generated. Call 'generate_keys()' first.")

        pem = cls._KEYS["private"].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem

    @classmethod
    def get_public_key_pem(cls) -> bytes:
        if cls._KEYS["public"] is None:
            raise ValueError("Public key not generated. Call 'generate_keys()' first.")

        pem = cls._KEYS["public"].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    @classmethod
    def encode_jwt(cls, payload: dict, algorithm='RS256') -> str:
        if cls._KEYS["private"] is None:
            raise ValueError("Private key not generated. Call 'generate_keys()' first.")

        payload.update(cls.get_default_payload())
        token = jwt.encode(payload, cls.get_private_key_pem(), algorithm=algorithm)
        return token

    @classmethod
    def decode_jwt(cls, token: str, algorithms=None) -> dict:
        if algorithms is None:
            algorithms = ['RS256']
        if cls._KEYS["public"] is None:
            raise ValueError("Public key not generated. Call 'generate_keys()' first.")

        payload = jwt.decode(token, cls.get_public_key_pem(), algorithms=algorithms)
        return payload

    @classmethod
    def get_default_exp(cls) -> int:
        return 3600

    @classmethod
    def get_default_algorithm(cls) -> str:
        return 'RS256'

    @classmethod
    def get_default_payload(cls) -> dict:
        return {
            "iss": "OF-AuthService",
            "aud": "fastapi",
            "exp": cls.get_default_exp(),
            "alg": cls.get_default_algorithm()
        }


JwtUtil.generate_keys()