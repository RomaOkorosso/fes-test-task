# created by RomaOkorosso at 21.03.2021
# publisher_methods.py

from datetime import datetime, timedelta, date
from typing import Optional
from Models.models import Publisher
from Models import schemas
from sqlalchemy.orm import Session
from Database.exceptions import *
from pydantic import ValidationError


class PublisherMethods:
    @staticmethod
    def create_publisher(db: Session, publisher: schemas.AddPublisher):
        try:
            publisher = Publisher(**publisher.dict())
        except Exception as err:
            print(err)
        else:
            db.add(publisher)
            db.commit()

    @staticmethod
    def get_publisher(db: Session, publisher_id: int):
        try:
            publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
        except Exception as err:
            print(err)
        else:
            if publisher is None:
                raise ItemNotFound(f"No such publisher with id: {publisher_id} in database")
            return publisher
