from fastapi import Depends
from app.database.database import LocalSession

def get_db():
    db = LocalSession()
    try:
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()