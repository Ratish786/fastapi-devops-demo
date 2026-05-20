# app/repository/user_repo.py

from model.model import User
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

def get_user_by_email(db, email):
    return db.query(User).filter(User.email == email).first()

def get_user_by_phone(db, phone):
    return db.query(User).filter(User.phone == phone).first()

def create_user(db, user_data):
    try:
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User with given email or phone already exists")



def get_user_by_id(db, user_id):
    return db.query(User).filter(User.id == user_id).first()

