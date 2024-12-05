from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.mission_schemas import MissionCreate, MissionList
from services.mission_services import (
    assign_cat,
    create_mission,
    delete_mission,
    get_mission,
    get_missions,
    update_mission_target,
)

mission = APIRouter()


@mission.post("/missions", response_model=MissionCreate)
async def create_spy_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    return await create_mission(mission, db)


@mission.get("/missions", response_model=List[MissionList])
async def list_missions(db: Session = Depends(get_db)):
    return await get_missions(db)


@mission.post("/missions/{mission_id}/assign/{cat_id}")
async def assign_mission(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    return await assign_cat(mission_id, cat_id, db)


@mission.delete("/mission/{mission_id}")
async def delete_spy_mission(mission_id: int, db: Session = Depends(get_db)):
    return await delete_mission(mission_id, db)


@mission.get("/mission/{mission_id}", response_model=MissionList)
async def get_spy_mission(mission_id: int, db: Session = Depends(get_db)):
    return await get_mission(mission_id, db)


@mission.patch("/missions/{mission_id}/targets/{target_id}")
async def update_target(
    mission_id: int,
    target_id: int,
    db: Session = Depends(get_db),
    notes: Optional[str] = None,
    is_complete: Optional[bool] = None,
):
    return await update_mission_target(mission_id, target_id, db, notes, is_complete)
