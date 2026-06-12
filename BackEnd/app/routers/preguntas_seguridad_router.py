from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import PreguntasSegurdadCreate, PreguntasSegurdadUpdate
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

@router.put("/{pregunta_id}")
def actualizar_pregunta_seguridad(
    pregunta_id: int,
    data: PreguntasSegurdadUpdate,
    session: Session = Depends(get_db)
):
    return actualizar_pregunta_seguridad_service(pregunta_id=pregunta_id, data=data, session=session)

