from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import PermisoCreate
from models.modelos import Permisos
from services.permisos_services import permisos

router = APIRouter(prefix="/permisos", tags=["Permisos"])

@router.get("/")
def obtener_permisos(
    session: Session = Depends(get_db)
):
    return permisos(session)

@router.post("/")
def crear_permiso(
    data: PermisoCreate,
    session: Session = Depends(get_db)
):
    nuevo_permiso = Permisos(
        **data.model_dump()
    )
    
    session.add(nuevo_permiso)
    session.commit()
    session.refresh(nuevo_permiso)
    
    return {"message": "Permiso creado exitosamente", "permiso": nuevo_permiso}
