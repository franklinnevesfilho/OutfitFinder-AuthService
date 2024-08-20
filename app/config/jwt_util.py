from fastapi import HTTPException
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
import jwt
import pytz
from fastapi.security import HTTPAuthorizationCredentials


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
    def encode_jwt(cls, payload: dict, algorithm='RS256', exp: timedelta = timedelta(minutes=15)) -> str:
        if cls._KEYS["private"] is None:
            raise ValueError("Private key not generated. Call 'generate_keys()' first.")

        # Merge the provided payload with the default payload
        default_payload = cls._get_default_payload(exp)
        payload.update(default_payload)

        token = jwt.encode(payload, cls.get_private_key_pem(), algorithm=algorithm)
        return token

    @classmethod
    def decode_jwt(cls, token: HTTPAuthorizationCredentials, algorithms=None) -> dict:
        if algorithms is None:
            algorithms = ['RS256']
        if cls._KEYS["public"] is None:
            raise ValueError("Public key not generated. Call 'generate_keys()' first.")

        try:
            payload = jwt.decode(token.credentials.encode("utf-8"), cls.get_public_key_pem(), algorithms=algorithms)
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token: " + str(e))

    @classmethod
    def _get_default_payload(cls, exp: timedelta) -> dict:
        now = datetime.now(pytz.utc)
        return {
            "iss": "OF-AuthService",
            "exp": now + exp,
        }
