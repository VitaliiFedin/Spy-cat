from typing import List, Optional

from pydantic import BaseModel


class TargetBase(BaseModel):
    name: str
    country: str
    notes: str = ""
    is_complete: bool = False


class TargetCreate(TargetBase):

    class Config:
        orm_mode = True


class Target(TargetBase):
    id: int

    class Config:
        orm_mode = True


class MissionBase(BaseModel):
    targets: List[Target]


class MissionCreate(MissionBase):
    is_complete: bool
    targets: List[TargetCreate]

    class Config:
        orm_mode = True


class MissionList(BaseModel):
    id: int
    targets: List[Target]
    cat_id: Optional[int]
