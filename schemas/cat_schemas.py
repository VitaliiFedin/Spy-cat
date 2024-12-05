from pydantic import BaseModel


class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float


class SpyCatList(SpyCatBase):
    id: int


class SpyCatCreate(SpyCatBase):
    pass


class SpyCat(SpyCatBase):
    id: int

    class Config:
        orm_mode = True
