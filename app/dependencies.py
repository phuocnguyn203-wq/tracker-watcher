from typing import Annotated

from fastapi import Depends, HTTPException, status

#-----------------------------------------------
#database dependency import
from app.database.database import LocalSession 
#-----------------------------------------------

#-----------------------------------------------
#user dependency import
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.schemas.users import TokenData, Token
from app.config import settings

import jwt
from app.services.users import get_user
#-----------------------------------------------


def get_db():
    db = LocalSession()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()

get_db_deps = Depends(get_db)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)] 
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Can\'t validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.secret_key,
            algorithms=[settings.algorithm]
        )
        username = payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credential_exception
    
    user = get_user(token_data.username) #type: ignore
    if user is None:
        raise credential_exception
    return user

get_current_user_dep = Depends(get_current_user)
