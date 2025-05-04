from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorOut(AuthorBase):
    id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author_id: int

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int

    class Config:
        orm_mode = True