import os

from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = os.getenv("DATABASE_URL", default="postgresql://localhost/devdb")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)
