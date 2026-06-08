from fastapi import APIRouter, Depends
from sqlmodel import Session
from schemas.esquemas import RolCreate, RolResponse
from database.conexion import get_db
from services.roles_services import *

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/",  response_model= list[RolResponse])
def obtener_roles(
    session: Session = Depends(get_db)
):
    return obtener_roles_services(session)

@router.post("/", status_code=201, response_model=RolResponse)
def crear_rol(
    data: RolCreate,
    session: Session = Depends(get_db)
):
    return crear_rol_service(data=data, session=session)

@router.post("/{rol_id}/permisos/{permiso_id}")
def asociar_permiso_a_rol(
    rol_id: int, 
    permiso_id: int, 
    session: Session = Depends(get_db)
):
   return asociar_permiso_a_rol_service(rol_id=rol_id, permiso_id=permiso_id, session=session)

@router.get("/{rol_nombre}/permisos")
def obtener_permisos_de_rol(
    rol_nombre: str, 
    session: Session = Depends(get_db)
):
    return obtener_permisos_de_rol_service(rol_nombre=rol_nombre, session=session)