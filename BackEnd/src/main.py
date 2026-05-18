from fastapi import FastAPI
from database.conexion import create_tables
from routers.permisos_router import router as permisos_router
from routers.roles_router import router as roles_router
from routers.preguntas_seguridad_router import router as preguntas_seguridad_router
from routers.usuarios_router import router as usuarios_router

app = FastAPI()

@app.get("/")
def inicio():
    return {"message":"Bienvenidos a la api de Vidrieria el Lobo 🐺"}

@app.on_event("startup")
def on_startup():
    create_tables()
    print("¡Tablas creadas con éxito! 🐺")

app.include_router(permisos_router)
app.include_router(roles_router)
app.include_router(preguntas_seguridad_router)
app.include_router(usuarios_router)