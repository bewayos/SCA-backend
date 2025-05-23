from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

# Dependency: отримаємо сесію БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- GET all cats ----------
@router.get("/", response_model=list[schemas.CatOut])
def read_cats(db: Session = Depends(get_db)):
    return crud.get_cats(db)


# ---------- GET one cat ----------
@router.get("/{cat_id}", response_model=schemas.CatOut)
def read_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = crud.get_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


# ---------- CREATE ----------
@router.post("/", response_model=schemas.CatOut)
def create_cat(cat: schemas.CatCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_cat(db, cat)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------- UPDATE salary ----------
@router.patch("/{cat_id}", response_model=schemas.CatOut)
def update_cat_salary(cat_id: int, data: schemas.CatUpdate, db: Session = Depends(get_db)):
    cat = crud.update_cat_salary(db, cat_id, data.salary)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat


# ---------- DELETE ----------
@router.delete("/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    success = crud.delete_cat(db, cat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cat not found")
    return {"detail": "Cat deleted"}
