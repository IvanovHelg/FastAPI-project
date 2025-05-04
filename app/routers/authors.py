from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/authors")

@router.post("/", response_model=schemas.AuthorOut)
def create(author: schemas.AuthorCreate, db: Session = Depends(get_db), user: schemas.UserOut = Depends(get_current_user)):
    return crud.create_author(db, author)

@router.get("/", response_model=list[schemas.AuthorOut])
def read_all(db: Session = Depends(get_db)):
    return crud.get_authors(db)