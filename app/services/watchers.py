from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.watchers import CreateWatcher, UpdateWatcher

from app.models.models import Watcher

def create_watcher(
    db: Session,
    create_watcher: CreateWatcher,
    user_id: int,
) -> Watcher:
    watcher = Watcher(
        user_id=user_id,
        **create_watcher.model_dump()
    )
    try:
        db.add(watcher)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise e
    
    return watcher

def get_all_watchers_for_users(
    db: Session,
    user_id: int,
) -> Sequence[Watcher]:
    stmt = select(Watcher).where(Watcher.user_id==user_id)
    all_watchers = db.scalars(stmt).all()
    
    return all_watchers

def get_specific_watcher(
    db: Session,
    user_id: int,
    watcher_id: int,
) -> Watcher | None:
    stmt = (
        select(Watcher).
        where(Watcher.user_id==user_id).
        where(Watcher.id==watcher_id)
    )
    
    watcher = db.scalar(stmt)
    return watcher

def modify_watcher(
    db: Session,
    user_id: int,
    watcher_id: int,
    update_watcher: UpdateWatcher
):
    stmt = (
        select(Watcher)\
            .where(Watcher.user_id==user_id)\
                .where(Watcher.id==watcher_id)
    )
    watcher = db.scalar(stmt)
    
    if watcher is not None:
        update_watcher_in_dict = update_watcher.model_dump()
        for k, v in update_watcher_in_dict.items():
            setattr(watcher, k, v)
        db.commit()

    return watcher

def delete_watcher(
    db: Session,
    user_id: int,
    watcher_id: int
):
    stmt = (
        select(Watcher)\
            .where(Watcher.user_id==user_id)\
                .where(Watcher.id==watcher_id)
    )
    watcher = db.scalar(stmt)

    if watcher is not None:
        db.delete(watcher)
        db.commit()

    return watcher