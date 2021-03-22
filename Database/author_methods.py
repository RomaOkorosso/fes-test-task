# created by RomaOkorosso at 21.03.2021
# author_methods.py

from datetime import datetime, timedelta, date
from typing import Optional
from Models.models import Author
from Models import schemas
from sqlalchemy.orm import Session
from Database.exceptions import *
from pydantic import ValidationError


class AuthorMethods:
    @staticmethod
    def add_author(db: Session, author: schemas.AddAuthor):
        author = Author(**author.dict())
        db.add(author)
        db.commit()
        return author

    @staticmethod
    def get_author(db: Session, author_id: int):
        try:
            author = db.query(Author).filter(Author.id == author_id).first()
        except Exception as err:
            print(err)
        else:
            if author is None:
                raise ItemNotFound(f"No such publisher with id: {author_id} in database")
            return author
