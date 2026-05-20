# app/services/auth_service.py

from fastapi import HTTPException , status , Request
from repo import user_repo
from passlib.context import CryptContext
import jwt
from setting import settings
from datetime import datetime, timedelta
from helper import create_access_token, create_refresh_token
from sqlalchemy.orm import Session
from schemas import LoginSchema

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password):
    # Hash password using argon2
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password , hashed_password)    


def register_service(db, user_data):

    # check email exists
    if user_repo.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    # check phone exists
    if user_repo.get_user_by_phone(db, user_data.phone):
        raise HTTPException(status_code=400, detail="Phone already exists")

    # convert to dict
    user_dict = user_data.dict()

    # hash password
    user_dict["password"] = hash_password(user_data.password)

    # create user
    return user_repo.create_user(db, user_dict)


def login_user(body: LoginSchema, db: Session):
    user = user_repo.get_user_by_email(db, body.email)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    } 


# Token send

def is_authenticated(request: Request , db:Session):
    token = request.headers.get("Authorization")
    token = token.split(" ")[-1]
    data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id = data.get("id")
    exp = data.get("exp")

    current_time = datetime.utcnow().timestamp()
    if current_time > exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    user = user_repo.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")    
    print(data)
    return user


def refresh_access_token(refresh_token: str, db: Session):
    try:
        data = jwt.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid refresh token")

    if data.get("token_type") != "refresh":
        raise HTTPException(401, "Invalid token type")

    user = user_repo.get_user_by_id(db, data.get("id"))

    if not user:
        raise HTTPException(401, "User not found")

    new_access_token = create_access_token(user.id)

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }