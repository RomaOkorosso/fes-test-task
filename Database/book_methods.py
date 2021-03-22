# created by RomaOkorosso at 21.03.2021
# book_methods.py

from datetime import datetime, timedelta, date
from typing import Optional
from Models.models import Book, TakenBook
from Models import schemas
from sqlalchemy.orm import Session
from Database.exceptions import *
from pydantic import ValidationError


class BookMethods:

    @staticmethod
    def add_book(db: Session, add_book: schemas.AddBook):
        new_book = Book(**add_book.dict())
        db.add(new_book)
        db.commit()
        return new_book

    @staticmethod
    def get_book(db: Session, book_id: int):
        try:
            book = db.query(Book).filter(Book.id == book_id).first()
        except Exception as err:
            print(err)
        else:
            if book is None:
                raise ItemNotFound(f"No such book id: {book_id} in database")
            return book

    @staticmethod
    def update_book(db: Session, update_book: schemas.Book):
        try:
            book = BookMethods.get_book(db, update_book.id)
        except ItemNotFound as err:
            print(err)
        else:
            for key, value in update_book.__dict__.iteritems():
                setattr(book, key, value)
            db.commit()

    @staticmethod
    def add_book_to_taken(db: Session, taken_book: schemas.TakenBook):
        to_add_taken_book = TakenBook(**taken_book.dict())
        db.add(to_add_taken_book)
        db.commit()

    @staticmethod
    def get_taken_book_by_id(db: Session, taken_book_id: int):
        try:
            taken_book = db.query(TakenBook).filter(TakenBook.id == taken_book_id).first()
        except Exception as err:
            print(err)
        else:
            if taken_book is None:
                raise ItemNotFound(f"No such taken_book id: {taken_book_id} in database")
            return taken_book

    @staticmethod
    def get_taken_book_by_client_and_book(db: Session, book_id: int, client_id: int):
        try:
            taken_book = db.query(TakenBook).filter(
                TakenBook.book_id == book_id and TakenBook.client_id == client_id).first()
        except Exception as err:
            print(err)
        else:
            if taken_book is None:
                raise ItemNotFound(f"No such taken_book in database")
            return taken_book

    @staticmethod
    def update_taken_book(db: Session, taken_book_update: schemas.TakenBook):
        try:
            taken_book: TakenBook = BookMethods.get_taken_book_by_id(db, taken_book_update.id)
        except ItemNotFound as err:
            print(err)
        else:

            for key, value in dict(taken_book_update).iteritems():
                setattr(taken_book, key, value)
            db.commit()

    @staticmethod
    def return_book(db: Session, taken_book_id: int):
        taken_book: TakenBook = BookMethods.get_taken_book_by_id(db, taken_book_id)
        taken_book.return_date = datetime.now().date()