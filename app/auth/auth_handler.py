import time
from datetime import datetime, timedelta

import jwt

from app.configs import config
from app.schemas import UserSchema

secrets = config.configs.jwt.secret
algorithms = config.configs.jwt.algorithm


def signJWT(user: UserSchema):
    payload = {
        "id": user.id,
        "username": user.username,
        "password": user.password,
        "expires": time.time() + 3600 * 24 * 7,
    }
    token = jwt.encode(payload, secrets, algorithm=algorithms)
    return token


print(signJWT(UserSchema(id=1, username="test", password="test123")))
