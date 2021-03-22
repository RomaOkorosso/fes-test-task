# created by RomaOkorosso at 21.03.2021
# schemas.py

import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, validator, ValidationError


class AddAuthor(BaseModel):
    full_name: str

    class Config:
        orm_mode = True


class Author(AddAuthor):
    id: int
    taken_count: int

    class Config:
        orm_mode = True


class AddPublisher(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Publisher(AddPublisher):
    id: int

    class Config:
        orm_mode = True


class AddBook(BaseModel):
    title: str
    count: int
    authors_id: List[int]
    publisher_id: Optional[int]
    publishing_year: int

    class Config:
        orm_mode = True


class Book(AddBook):
    id: int
    taken_count: Optional[int]

    class Config:
        orm_mode = True


class AddClient(BaseModel):
    full_name: str
    type: str

    @validator('type')
    def validate_user_type(cls, v):
        if v not in ["student", "professor", "worker"]:
            raise ValueError(f"type must be 'student', 'professor' or 'worker' not '{v}'")
        return v

    class Config:
        orm_mode = True


class Client(AddClient):
    id: int
    taken_now_books_id: Optional[List[int]]
    all_taken_books_id: Optional[List[int]]

    class Config:
        orm_mode = True


class TakenBook(BaseModel):
    id: int
    book_id: int
    client_id: int
    taken_date: datetime.date
    return_date: Optional[datetime.date]

    class Config:
        orm_mode = True
