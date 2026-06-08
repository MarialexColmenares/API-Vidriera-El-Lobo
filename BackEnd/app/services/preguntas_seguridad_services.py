from fastapi import HTTPException
from sqlmodel import select
from models.modelos import PreguntaSeguridad

def obtener_preguntas_seguridad_service(session):
    preguntas = session.exec(select(PreguntaSeguridad)).all()
    if not preguntas:
        raise HTTPException (status_code=404,detail="No se encontraron preguntas de seguridad")
    return preguntas

def crear_pregunta_seguridad_service(data, session):
    nueva_pregunta = PreguntaSeguridad(
        pregunta=data.pregunta
    )
    session.add(nueva_pregunta)
    session.commit()
    session.refresh(nueva_pregunta)
    
    return {"message": "Pregunta de Seguridad creada exitosamente", "Pregunta de Seguridad ": nueva_pregunta}