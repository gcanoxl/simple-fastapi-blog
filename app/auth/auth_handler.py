import time

import jwt

from app.configs import config
from app.schemas import UserSchema

secrets = config.configs.jwt.secret
algorithms = config.configs.jwt.algorithm


def signJWT(user: UserSchema):
    payload = {
        "id": user.id,
        "username": user.username,
        "expires": time.time() + 3600 * 24 * 7,
    }
    token = jwt.encode(payload, secrets, algorithm=algorithms)
    return token


def decodeJWT(token) -> UserSchema | None:
    try:
        payload = jwt.decode(token, secrets, algorithms=algorithms)
        return UserSchema(**payload) if payload["expires"] >= time.time() else None
    except:
        return None
