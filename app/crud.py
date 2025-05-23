from sqlalchemy.orm import Session
from app import models, schemas
import requests

# ----------- CAT ------------
def get_cats(db: Session):
    return db.query(models.Cat).all()

def get_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()

def create_cat(db: Session, cat: schemas.CatCreate):
    # Validate breed
    r = requests.get("https://api.thecatapi.com/v1/breeds")
    breeds = [b["name"].lower() for b in r.json()]
    if cat.breed.lower() not in breeds:
        raise ValueError("Breed not found in TheCatAPI")

    db_cat = models.Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_cat_salary(db: Session, cat_id: int, salary: float):
    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return None
    db_cat.salary = salary
    db.commit()
    return db_cat

def delete_cat(db: Session, cat_id: int):
    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return False
    db.delete(db_cat)
    db.commit()
    return True

# ----------- MISSION ------------
def get_missions(db: Session):
    return db.query(models.Mission).all()

def get_mission(db: Session, mission_id: int):
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()

def create_mission(db: Session, mission: schemas.MissionCreate):
    if not (1 <= len(mission.targets) <= 3):
        raise ValueError("Mission must have between 1 and 3 targets")

    db_mission = models.Mission(is_complete=False)
    db.add(db_mission)
    db.flush()  # get db_mission.id

    for target_data in mission.targets:
        target = models.Target(**target_data.dict(), mission_id=db_mission.id)
        db.add(target)

    db.commit()
    db.refresh(db_mission)
    return db_mission

def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    db_mission = get_mission(db, mission_id)
    if not db_mission:
        return None
    if db_mission.cat_id:
        raise ValueError("Mission already assigned to a cat")

    db_cat = get_cat(db, cat_id)
    if not db_cat:
        return None
    if db_cat.mission:
        raise ValueError("Cat already has a mission")

    db_mission.cat_id = cat_id
    db.commit()
    return db_mission

def delete_mission(db: Session, mission_id: int):
    db_mission = get_mission(db, mission_id)
    if not db_mission:
        return False
    if db_mission.cat_id:
        raise ValueError("Can't delete a mission assigned to a cat")
    db.delete(db_mission)
    db.commit()
    return True

# ----------- TARGET NOTES / COMPLETE ------------
def update_target_notes(db: Session, target_id: int, notes: str):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target or target.is_complete or target.mission.is_complete:
        raise ValueError("Cannot update notes - target or mission is complete")
    target.notes = notes
    db.commit()
    return target

def mark_target_complete(db: Session, target_id: int):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        return None
    target.is_complete = True
    db.commit()

    # Check if all targets are complete -> mark mission complete
    mission = target.mission
    if all(t.is_complete for t in mission.targets):
        mission.is_complete = True
        db.commit()

    return target
