import sys

from db.database import Base, engine

sys.path.append(".")
from fastapi import APIRouter

from db.database import check_db_connection

health = APIRouter()


@health.get("/db")
async def check_db():
    is_connected = check_db_connection()
    print(is_connected)
    if is_connected:
        Base.metadata.create_all(bind=engine)
        return {"Database": "Connected", "status": True}
    return {"Database": "Not Connected", "status": False}
