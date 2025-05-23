from pydantic import BaseModel, Field
from typing import Optional, List


# ---------- Target ----------
class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    is_complete: bool = False

class TargetCreate(TargetBase):
    pass

class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None

class TargetOut(TargetBase):
    id: int

    class Config:
        orm_mode = True


# ---------- Mission ----------
class MissionBase(BaseModel):
    is_complete: bool = False

class MissionCreate(MissionBase):
    targets: List[TargetCreate]

class MissionAssignCat(BaseModel):
    cat_id: int

class MissionOut(MissionBase):
    id: int
    cat_id: Optional[int]
    targets: List[TargetOut]

    class Config:
        orm_mode = True


# ---------- Cat ----------
class CatBase(BaseModel):
    name: str
    years_experience: int = Field(..., ge=0)
    breed: str
    salary: float = Field(..., ge=0)

class CatCreate(CatBase):
    pass

class CatUpdate(BaseModel):
    salary: float = Field(..., ge=0)

class CatOut(CatBase):
    id: int

    class Config:
        orm_mode = True
