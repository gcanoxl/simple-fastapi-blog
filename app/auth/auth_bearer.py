from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.auth_handler import decodeJWT
from app.schemas import UserSchema


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> UserSchema:
        credentials: HTTPAuthorizationCredentials | None = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            try:
                user = decodeJWT(credentials.credentials)
                if user:
                    return user
                else:
                    raise HTTPException(
                        status_code=403, detail="Invalid token or expired token."
                    )
            except:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
        else:
            raise HTTPException(status_code=401, detail="Not authenticated")
