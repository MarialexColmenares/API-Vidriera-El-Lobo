from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import PermisoCreate, PermisoUpdate
from services.permisos_services import *

router = APIRouter(prefix="/permisos", tags=["Permisos"])

@router.get("/")
def obtener_permisos(session: Session = Depends(get_db)):
    return obtener_permisos_service(session)

@router.post("/", status_code=201)
def crear_permiso(data: PermisoCreate, session: Session = Depends(get_db)):
    return crear_permiso_service(data, session)

@router.patch("/{permiso_id}")
def actualizar_permiso(permiso_id: int, data: PermisoUpdate, session: Session = Depends(get_db)):
    return actualizar_permiso_service(permiso_id, data, session)

@router.get("/{permiso_id}")
def obtener_permiso_por_id(permiso_id: int, session: Session = Depends(get_db)):
    return obtener_permiso_por_id_service(permiso_id, session)
