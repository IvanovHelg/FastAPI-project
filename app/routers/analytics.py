from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal
from app.deps import get_db

router = APIRouter(prefix="/analytics")

@router.get("/top-authors")
def top_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return sorted(
        [(a.name, len(a.books)) for a in authors],
        key=lambda x: x[1], reverse=True
    )