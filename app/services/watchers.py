from sqlalchemy.orm import Session

from app.schemas.watchers import CreateWatcher

from app.models.models import Watcher

def create_watcher(
    db: Session,
    create_watcher: CreateWatcher,
    user_id: int,
):
    watcher = Watcher(
        user_id=user_id,
        **create_watcher.model_dump()
    )
    db.add(watcher)
    db.commit()
    