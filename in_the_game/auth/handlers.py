import os
import time
from typing import Dict
import jwt
from jwt.exceptions import DecodeError


JWT_SECRET = os.getenv("JWT_SECRET", default="secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITH", default="HS256")


def sign_with_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Dict:
    try:
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_payload["expires"] >= time.time():
            return decoded_payload
    except (DecodeError, KeyError):
        pass    
    return {}
