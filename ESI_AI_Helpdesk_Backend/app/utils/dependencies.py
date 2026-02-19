# dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError
from requests import Session
from app.models.database import UserSession
from app.utils.config import get_db
from app.utils.jwt_security import decode_token

security = HTTPBearer()

def get_current_user(
    credentials=Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)

    session = db.query(UserSession).filter(
        UserSession.access_token == token,
        UserSession.is_active == True
    ).first()

    if not session:
        raise HTTPException(status_code=401, detail="Session invalid")

    return payload



# Role based dependency
def require_role(min_level: int):
    def wrapper(user=Depends(get_current_user)):
        if user.get("role_level") < min_level:
            raise HTTPException(status_code=403, detail="Access denied")
        return user

    return wrapper
