from sqlmodel import create_engine, SQLModel
from database.datos import DATABASE_URL
from models.modelos import *

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)