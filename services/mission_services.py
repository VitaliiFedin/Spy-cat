import sys

sys.path.append(".")

import os
from typing import Optional

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import Mission, SpyCat, Target
from schemas.mission_schemas import MissionCreate


async def create_mission(mission: MissionCreate, db: Session):
    if len(mission.targets) < 1 or len(mission.targets) > 3:
        raise HTTPException(status_code=400, detail="Mission must have 1-3 targets")

    db_mission = Mission(is_complete=False)
    db.add(db_mission)
    db.flush()

    for target in mission.targets:
        db_target = Target(**target.dict(), mission_id=db_mission.id)
        db.add(db_target)

    db.commit()
    db.refresh(db_mission)
    return db_mission


async def get_missions(db: Session):
    return db.query(Mission).all()


async def assign_cat(mission_id: int, cat_id: int, db: Session):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    cat = db.query(SpyCat).filter(SpyCat.id == cat_id).first()

    if not mission or not cat:
        raise HTTPException(status_code=404, detail="Mission or cat not found")

    # Check if cat already has an active mission
    active_mission = (
        db.query(Mission)
        .filter(Mission.cat_id == cat_id, Mission.is_complete == False)
        .first()
    )

    if active_mission:
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    mission.cat_id = cat_id
    db.commit()
    return {"message": "Mission assigned successfully"}


async def delete_mission(mission_id: int, db: Session):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id:
        raise HTTPException(status_code=400, detail="Cannot delete assigned mission")
    db.delete(mission)
    db.commit()
    return {"message": "Mission deleted"}


async def get_mission(mission_id: int, db: Session):
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


async def update_mission_target(
    mission_id: int,
    target_id: int,
    db: Session,
    notes: Optional[str] = None,
    is_complete: Optional[bool] = None,
):
    target = (
        db.query(Target)
        .filter(Target.id == target_id, Target.mission_id == mission_id)
        .first()
    )

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    mission = target.mission
    if mission.is_complete or target.is_complete:
        raise HTTPException(
            status_code=400, detail="Cannot update completed target/mission"
        )

    if notes is not None:
        target.notes = notes
    if is_complete is not None:
        target.is_complete = is_complete
        # Check if all targets are complete to update mission status
        if is_complete and all(t.is_complete for t in mission.targets):
            mission.is_complete = True

    db.commit()
    return {"message": "Target updated successfully"}
