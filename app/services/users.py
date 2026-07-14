from datetime import datetime, timezone, timedelta

import jwt
from pwdlib import PasswordHash

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.models import User
from app.schemas.users import UserInDB

from app.config import settings


password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_hashed_password(plain_password):
    return password_hash.hash(plain_password)

def get_user(
    db: Session,
    username: str
):
    stmt = select(User).where(User.username==username)
    user = db.scalar(stmt)
    if user is not None:
        return UserInDB(**user.__dict__)

def authenticate_user(
    db: Session,
    username: str,
    password: str
):
    user = get_user(
        db=db,
        username=username
    )
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
            
    return encoded_jwt

def create_user(
    db: Session,
    username: str,
    password: str,
    email: str,
):
    new_user = User(
        username=username,
        hashed_password=get_hashed_password(password),
        email=email,
    )
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise e
    