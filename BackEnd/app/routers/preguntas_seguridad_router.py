from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import PreguntasSegurdadCreate
from services.preguntas_seguridad_services import *

router = APIRouter(prefix="/preguntas-seguridad", tags=["Preguntas de Seguridad"])

@router.get("/")
def obtener_preguntas_seguridad(
    session: Session = Depends(get_db)
):
    return obtener_preguntas_seguridad_service(session)
    
@router.post("/", status_code=201)
def crear_pregunta_seguridad(
    data: PreguntasSegurdadCreate,
    session: Session = Depends(get_db)
):
    return crear_pregunta_seguridad_service(data=data, session =session)

