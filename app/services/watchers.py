from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.watchers import CreateWatcher

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
    