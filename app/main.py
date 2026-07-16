from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.database import init_db
from app.scheduler import start_scheduler, shutdown_scheduler

from app.routers import users
from app.routers import watchers

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield
    shutdown_scheduler()

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(watchers.router)
