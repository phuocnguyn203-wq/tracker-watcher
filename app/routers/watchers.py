from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.models import User, Watcher
from app.schemas.watchers import CreateWatcher, ReturnedWatcher

from app.dependencies import get_db_dep
from app.dependencies import get_current_user_dep 

from app.services import watchers as watchers_service

router = APIRouter(
    prefix='/watchers',
    tags=['watchers']
)

@router.post('/create_watcher', response_model=ReturnedWatcher)
async def create_watcher(
    db: Annotated[Session, get_db_dep],
    user: Annotated[User, get_current_user_dep],
    create_watcher: Annotated[CreateWatcher, Body()]    
):
    try:
        watcher = watchers_service.create_watcher(
            db=db,
            user_id=user.id,
            create_watcher=create_watcher
        )
        return watcher
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Something\'s duplicated'
        )

@router.get('/watchers_by_user_id')
def get_watchers_by_user_id(
    db: Annotated[Session, get_db_dep],
    current_user: Annotated[User, get_current_user_dep]
):
    all_watchers = watchers_service.get_all_watchers_for_users(
        db=db,
        user_id=current_user.id
    )
    return all_watchers