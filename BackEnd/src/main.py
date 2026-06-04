from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.conexion import create_tables
from routers import router_central

@asynccontextmanager #lifespan es una función especial que se ejecuta antes de que la API empiece a recibir peticiones y también cuando el servidor se apaga
async def lifespan(app: FastAPI):
    # Todo lo que se escriba AQUÍ adentro se ejecutará ANTES de que la API empiece a recibir peticiones
    print("Verificando y creando tablas en la base de datos...")
    create_tables()
    yield
    # Lo que se escriba después del yield se ejecuta cuando el servidor se apaga (Clean up)
    print("Apagando el servidor...")

# 2. Pasamos el lifespan a la instancia de FastAPI
app = FastAPI(
    title="Sistema De Gestion para Vidrios Y Aceros el Lobo  - API",
    version="1.0.0",
    description="API para la gestión de ordenes de trabajo, clientes, productos y stock en Vidrieria el Lobo 🐺",
    lifespan=lifespan # <--- IMPORTANTE: Vinculamos el ciclo de vida
)
@app.get("/")
def inicio():
    return {"message":"Bienvenidos a la api de Vidrieria el Lobo 🐺"}

@asynccontextmanager
async def lifespan():
    create_tables()

app.include_router(router_central)
