from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import PreguntasSegurdadCreate
from models.modelos import PreguntasSeguridad

router = APIRouter(prefix="/preguntas-seguridad", tags=["Preguntas de Seguridad"])

@router.get("/")
def obtener_preguntas_seguridad(
    session: Session = Depends(get_db)
):
    preguntas = session.query(PreguntasSeguridad).all()
    if not preguntas:
        raise HTTPException (status_code=404,detail="No se encontraron preguntas de seguridad")
    return preguntas

@router.post("/")
def crear_preguntas_seguridad(
    data: PreguntasSegurdadCreate,
    session: Session = Depends(get_db)
):
    nueva_pregunta = PreguntasSeguridad(
        pregunta=data.pregunta
    )
    session.add(nueva_pregunta)
    session.commit()
    session.refresh(nueva_pregunta)
    
    return {"message": "Pregunta de Seguridad creada exitosamente", "Pregunta de Seguridad ": nueva_pregunta}