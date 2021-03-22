# created by RomaOkorosso at 21.03.2021
# models.py

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Date
)

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from Database.database import Base


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    taken_count = Column(Integer, default=0)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    count = Column(Integer)
    taken_count = Column(Integer)
    authors_id = Column(postgresql.ARRAY(Integer), default=None)
    publisher_id = Column(Integer)
    publishing_year = Column(Integer)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    full_name = Column(String)
    taken_books_now_id = Column(postgresql.ARRAY(Integer), default=[])
    all_taken_books_id = Column(postgresql.ARRAY(Integer), default=[])


class TakenBook(Base):
    __tablename__ = "taken_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    taken_date = Column(Date)
    return_date = Column(Date, default=None)
