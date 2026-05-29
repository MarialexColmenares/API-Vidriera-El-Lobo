from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import PermisoCreate
from services.permisos_services import *

router = APIRouter(prefix="/permisos", tags=["Permisos"])

@router.get("/")
def obtener_permisos(session: Session = Depends(get_db)):
    return obtener_permisos_service(session)

@router.post("/", status_code=201)
def crear_permiso(data: PermisoCreate, session: Session = Depends(get_db)):
    return crear_permiso_service(data, session)
