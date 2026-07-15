from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi import Body, Path

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.models import User, Watcher
from app.schemas.watchers import CreateWatcher, ReturnedWatcher, UpdateWatcher

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
async def get_watchers_by_user_id(
    db: Annotated[Session, get_db_dep],
    current_user: Annotated[User, get_current_user_dep]
):
    all_watchers = watchers_service.get_all_watchers_for_users(
        db=db,
        user_id=current_user.id
    )
    return all_watchers

@router.get('/{watcher_id}', response_model=ReturnedWatcher)
async def get_specific_watcher_by_id(
    db: Annotated[Session, get_db_dep],
    current_user: Annotated[User, get_current_user_dep],
    watcher_id: Annotated[int, Path()]
):
    watcher = watchers_service.get_specific_watcher(
        db=db,
        user_id=current_user.id,
        watcher_id=watcher_id,
    )
    if watcher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Could not find watcher {watcher_id}'
        )
    return watcher

@router.put('/{watcher_id}', response_model=ReturnedWatcher)
async def modify_watcher(
    db: Annotated[Session, get_db_dep],
    current_user: Annotated[User, get_current_user_dep],
    watcher_id: Annotated[int, Path()],
    update_watcher: Annotated[UpdateWatcher, Body()]
):
    updated_watcher = watchers_service.modify_watcher(
        db=db,
        user_id=current_user.id,
        watcher_id=watcher_id,
        update_watcher=update_watcher
    )
    
    if updated_watcher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Could not found watcher {watcher_id}'
        )
    
    return updated_watcher
    