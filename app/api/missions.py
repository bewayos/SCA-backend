from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependency: session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- GET all missions ----------
@router.get("/", response_model=list[schemas.MissionOut])
def read_missions(db: Session = Depends(get_db)):
    return crud.get_missions(db)


# ---------- GET one mission ----------
@router.get("/{mission_id}", response_model=schemas.MissionOut)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = crud.get_mission(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


# ---------- CREATE mission + targets ----------
@router.post("/", response_model=schemas.MissionOut)
def create_mission(data: schemas.MissionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_mission(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- ASSIGN cat to mission ----------
@router.patch("/{mission_id}/assign", response_model=schemas.MissionOut)
def assign_cat(mission_id: int, payload: schemas.MissionAssignCat, db: Session = Depends(get_db)):
    try:
        return crud.assign_cat_to_mission(db, mission_id, payload.cat_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- DELETE mission ----------
@router.delete("/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    try:
        success = crud.delete_mission(db, mission_id)
        if not success:
            raise HTTPException(status_code=404, detail="Mission not found")
        return {"detail": "Mission deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- PATCH notes on target ----------
@router.patch("/targets/{target_id}/notes", response_model=schemas.TargetOut)
def update_target_notes(target_id: int, payload: schemas.TargetUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_target_notes(db, target_id, payload.notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- PATCH mark target as complete ----------
@router.patch("/targets/{target_id}/complete", response_model=schemas.TargetOut)
def complete_target(target_id: int, db: Session = Depends(get_db)):
    target = crud.mark_target_complete(db, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target
