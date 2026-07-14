from typing import Annotated
from app.config import settings

from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.users import Token, User, CreateUser

from datetime import timedelta
from app.dependencies import get_db_dep, get_current_user_dep
from app.services import users as users_service

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.post('/token')
async def login_for_access_token(
    db: Annotated[Session, get_db_dep],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = users_service.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='username or password is wrong',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = users_service.create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires,
    )
    
    return Token(
        access_token=access_token,
        token_type='bearer'
    )

@router.post('/create_user')
async def create_user(
    db: Annotated[Session, get_db_dep],
    create_user: Annotated[CreateUser, Body()],
):
    try:
        users_service.create_user(
            db,
            **create_user.model_dump()
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username or email already exists'
        )

@router.get('/me')
async def read_user_me(
    user: Annotated[User, get_current_user_dep],
) -> User:
    return user
