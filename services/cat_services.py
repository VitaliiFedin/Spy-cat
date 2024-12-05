import sys

sys.path.append(".")
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import SpyCat
from schemas.cat_schemas import SpyCatCreate

load_dotenv()


async def validate_breed(breed: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.thecatapi.com/v1/breeds/search",
            params={"q": breed},
            headers={"x-api-key": os.getenv("CAT_API_KEY", "")},
        )
        if response.status_code != 200 or not response.json():
            raise HTTPException(status_code=400, detail="Invalid cat breed")


async def create_cat(cat: SpyCatCreate, db: Session):
    await validate_breed(cat.breed)
    db_cat = SpyCat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


async def get_cats(db: Session):
    return db.query(SpyCat).all()


async def get_cat_by_id(cat_id: int, db: Session):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


async def delete_cat(cat_id: int, db: Session):
    cat_to_delete = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat_to_delete:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(cat_to_delete)
    db.commit()
    return {"message": "Cat deleted"}


async def update_cat(cat_id: id, salary: float, db: Session):
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    cat.salary = salary
    db.commit()
    db.refresh(cat)
    return cat
