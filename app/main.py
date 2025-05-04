from fastapi import FastAPI
from app.routers import users, books, authors, analytics
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(analytics.router)