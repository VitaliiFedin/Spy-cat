from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import SpyCat
from schemas.cat_schemas import SpyCatBase, SpyCatList
from services.cat_services import (
    create_cat,
    delete_cat,
    get_cat_by_id,
    get_cats,
    update_cat,
)

cat = APIRouter()


@cat.post("/add", response_model=SpyCatBase)
async def create_spy_cat(cat: SpyCatBase, db: Session = Depends(get_db)):
    return await create_cat(cat, db)


@cat.get("/cats", response_model=List[SpyCatList])
async def list_spy_cats(db: Session = Depends(get_db)):
    return await get_cats(db)


@cat.get("/{cat_id}", response_model=SpyCatList)
async def get_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    return await get_cat_by_id(cat_id, db)


@cat.delete("/cats/{cat_id}")
async def delete_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    return await delete_cat(cat_id, db)


@cat.patch("/cats/{cat_id}", response_model=SpyCatBase)
async def update_spy_cat(cat_id: int, salary: float, db: Session = Depends(get_db)):
    return await update_cat(cat_id, salary, db)
