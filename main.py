"""
Main file.
Run with `uvicorn main:app --reload`
"""
from fastapi import FastAPI, Depends, HTTPException
from Models import models, schemas
from Database.database import SessionLocal, engine
from Database import client_methods, book_methods, author_methods
from Database.exceptions import *
from pydantic import ValidationError

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def home():
    return {'test': 'Hello world'}


@app.post("/add-client", response_model=schemas.Client, tags=["public"])
async def add_client(client: schemas.AddClient, db=Depends(get_db)):
    """create the client, add to Database and return that one"""
    new_client = client_methods.ClientMethods.add_client(db, client)
    return new_client


@app.get("/get-client", response_model=schemas.Client, tags=["public"])
async def get_client(client_id: int, db=Depends(get_db)):
    """Get client from Database and return it"""
    try:
        client = client_methods.ClientMethods.get_client(db, client_id)
    except ItemNotFound as err:
        raise HTTPException(status_code=404, detail=err.__cause__)
    else:
        return client


@app.post("/add-book", response_model=schemas.Book, tags=["public"])
async def add_book(book: schemas.AddBook, db=Depends(get_db)):
    """Create book, add it into Database and return it"""
    new_book = book_methods.BookMethods.add_book(db, book)
    return new_book


@app.get("/get-book", response_model=schemas.Book, tags=["public"])
async def get_client(book_id: int, db=Depends(get_db)):
    """Get book from Database and return it"""
    try:
        book = book_methods.BookMethods.get_book(db, book_id)
    except ItemNotFound as err:
        raise HTTPException(status_code=404, detail=err.__cause__)
    else:
        return book


@app.post("/add-author", response_model=schemas.Author, tags=["public"])
async def add_author(author: schemas.AddAuthor, db=Depends(get_db)):
    """Add author to the Database"""
    new_author = author_methods.AuthorMethods.add_author(db, author)
    return new_author


@app.post("/take-book", response_model=schemas.Book, tags=["public"])
async def take_book(book_id: int, client_id: int, db=Depends(get_db)):
    """
    Reduce books counter in books table,
     add book id to the client table in rows taken_books_now_id and all_taken_books_id
     add record to the taken_books table
     """

    book = client_methods.ClientMethods.take_book(db, book_id, client_id)
    return book


@app.post("/return-book", response_model=schemas.Book, tags=["public"])
async def return_book(taken_book_id: int, db=Depends(get_db)):
    """
    Return book at shelf,
     add book id to the client table in rows taken_books_now_id and all_taken_books_id
     complete record to the taken_books table
     """

    book = client_methods.ClientMethods.return_book(db, taken_book_id)
    return book
