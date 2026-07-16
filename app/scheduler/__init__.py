import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import LocalSession
from app.models.models import Watcher
from app.services.alerts.orchestrator import check_watcher

logger = logging.getLogger(__name__)

TICK_JOB_ID = 'watcher-tick'
TICK_INTERVAL_MINUTES = 1

scheduler = AsyncIOScheduler()


def _get_due_watchers(db: Session) -> list[Watcher]:
    now = datetime.now(timezone.utc)
    all_watchers = db.scalars(select(Watcher)).all()

    due_watchers = []
    for watcher in all_watchers:
        last_checked_at = watcher.last_checked_at
        if last_checked_at is None:
            due_watchers.append(watcher)
            continue

        if last_checked_at.tzinfo is None:
            last_checked_at = last_checked_at.replace(tzinfo=timezone.utc)

        elapsed_minutes = (now - last_checked_at).total_seconds() / 60
        if elapsed_minutes >= watcher.interval_minutes:
            due_watchers.append(watcher)

    return due_watchers


def run_due_watchers() -> None:
    db = LocalSession()
    try:
        for watcher in _get_due_watchers(db):
            try:
                check_watcher(db, watcher)
            except Exception:
                logger.exception('Failed to check watcher %s', watcher.id)
    finally:
        db.close()


def start_scheduler() -> None:
    if scheduler.get_job(TICK_JOB_ID) is None:
        scheduler.add_job(
            run_due_watchers,
            trigger=IntervalTrigger(minutes=TICK_INTERVAL_MINUTES),
            id=TICK_JOB_ID,
        )
    scheduler.start()


def shutdown_scheduler() -> None:
    scheduler.shutdown(wait=False)
