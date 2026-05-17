from fastapi import FastAPI
from database.conexion import create_tables

app = FastAPI()

@app.get("/")
def inicio():
    return {"message":"Bienvenidos a la api de Vidrieria el Lobo 🐺"}


@app.on_event("startup")
def on_startup():
    print("Construyendo las tablas en lobo_db...")
    create_tables()
    print("¡Tablas creadas con éxito! 🐺")
    
