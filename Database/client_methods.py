# created by RomaOkorosso at 21.03.2021
# client_methods.py

from datetime import datetime, timedelta, date
from typing import Optional, List
from Models.models import Client, TakenBook, Book
from Models import schemas
from sqlalchemy.orm import Session
from Database.exceptions import *
from pydantic import ValidationError


class ClientMethods:

    @staticmethod
    def add_client(db: Session, client: schemas.AddClient):
        client = Client(**client.dict())
        db.add(client)
        db.commit()
        return client

    @staticmethod
    def get_client(db: Session, client_id: int):
        client: Client = db.query(Client).filter(Client.id == client_id).first()
        if client is None:
            raise ItemNotFound(f"Have no client with id: {client_id} in database")
        return client

    @staticmethod
    def update_client(db: Session, new_client: schemas.Client):
        client = db.query(Client).filter(Client.id == new_client.id).first()

        if client is None:
            raise ItemNotFound(f"Have no client with id: {new_client.id} in database")

        for key, value in new_client.__dict__.iteritems():
            setattr(client, key, value)
        db.commit()

    @staticmethod
    def take_book(db: Session, book_id: int, client_id: int):
        book: Book = db.query(Book).filter(Book.id == book_id).first()
        try:
            client = ClientMethods.get_client(db, client_id)
        except ItemNotFound as err:
            print(err)
        else:
            if client.taken_books_now_id is None:
                client.taken_books_now_id = [book_id]

            if client.all_taken_books_id is None:
                client.all_taken_books_id = [book_id]

            client.taken_books_now_id = client.taken_books_now_id.append(book_id)
            client.all_taken_books_id = client.all_taken_books_id.append(book_id)

        if book is None:
            raise ItemNotFound(f"Have no such book with id: {book_id}")

        if book.count == 0:
            raise NotEnoughBook(f"Have no enough books with id: {book_id}")

        taken_book = TakenBook(
            book_id=book_id,
            client_id=client_id,
            taken_date=datetime.today().date()
        )
        book.count -= 1
        db.add(taken_book)
        db.commit()
        db.flush()
        db.refresh(book)
        return book

    @staticmethod
    def return_book(db: Session, taken_book_id: int):
        from Database.book_methods import BookMethods
        try:
            book: Book
            client: Client
            BookMethods.return_book(db, taken_book_id)
            taken_book = BookMethods.get_taken_book_by_id(db, taken_book_id)
            book_id = taken_book.id
            client_id = taken_book.client_id
            book = BookMethods.get_book(db, book_id)
            client = ClientMethods.get_client(db, client_id)
        except ItemNotFound as err:
            print(err)
        else:
            print(type(client.taken_books_now_id))
            books: List[int] = client.taken_books_now_id.copy()
            books.remove(book_id)
            client.taken_books_now_id = books

            book.count = book.count + 1
            book.taken_count = book.taken_count + 1
            ClientMethods.update_client(db, client)
            db.commit()
            return book
