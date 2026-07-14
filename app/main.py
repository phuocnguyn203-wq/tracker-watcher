from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.database import init_db

from app.routers import users
from app.routers import watchers

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(watchers.router)
