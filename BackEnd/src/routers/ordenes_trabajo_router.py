from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from services.ordenes_trabajo_services import *
from schemas.esquemas import OrdenTrabajoCreate

router = APIRouter(prefix="/ordenes_trabajo", tags=["Ordenes de Trabajo"])

@router.get("/") # faltan esquemas de respuesta 
def obtener_ordenes_trabajo(
    session: Session = Depends(get_db)
):
    return obtener_ordenes_trabajo_service(session)

    
@router.post("/", status_code=201)
def crear_orden_trabajo(
    data: OrdenTrabajoCreate ,
    session: Session = Depends(get_db)
):
    return crear_ordenes_trabajo_service(data=data, session=session)



