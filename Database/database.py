# created by RomaOkorosso at 21.03.2021
# database.py

import config

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine(
    config.db_url
)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
