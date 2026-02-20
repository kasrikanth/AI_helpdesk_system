from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.config import get_db
from app.utils.jwt_security import verify_password,hash_password,create_access_token
from app.utils.dependencies import require_role
from app.apis.api_schema import LoginRequest, CreateUserRequest
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.models.database import UserSession, User, Role

auth_router = APIRouter()

@auth_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(403, "User disabled")

    token_data = {
        "sub": str(user.id),
        "role": user.role.name,
        "role_level": user.role.level,}
    access_token = create_access_token(token_data)

    # CREATE SESSION ENTRY
    session = UserSession(
        user_id=user.id,
        access_token=access_token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )

    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "session_id": str(session.id)  # return session id
    }

# create user with all roles (Admin only)
@auth_router.post("/create-user")
def create_user(
    request: CreateUserRequest,
    user=Depends(require_role(80)),
    db: Session = Depends(get_db)):
    creator_level = user["role_level"]
    
    # extract role id from name
    role = db.query(Role).filter(Role.name == request.role_name).first()

    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    if creator_level == 80 and role.level >= 80:
        raise HTTPException(status_code=403, detail="Admin cannot create admin")

    new_user = User(
        email=request.email,
        full_name=request.full_name,
        password_hash=hash_password(request.password),
        role_id=role.id)

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}
