from sqlmodel import create_engine, SQLModel, Session
from database.datos import DATABASE_URL
from models.modelos import *

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)
    
def get_db():
    with Session(engine) as session:
        yield session