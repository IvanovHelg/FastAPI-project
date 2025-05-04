from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.deps import get_db, get_current_user

router = APIRouter(prefix="/books")

@router.post("/", response_model=schemas.BookOut)
def create(book: schemas.BookCreate, db: Session = Depends(get_db), user: schemas.UserOut = Depends(get_current_user)):
    return crud.create_book(db, book)

@router.get("/", response_model=list[schemas.BookOut])
def read_all(db: Session = Depends(get_db)):
    return crud.get_books(db)