from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.conexion import create_tables
from routers import router_central


app = FastAPI()

@app.get("/")
def inicio():
    return {"message":"Bienvenidos a la api de Vidrieria el Lobo 🐺"}

@asynccontextmanager
async def lifespan():
    create_tables()

app.include_router(router_central)
