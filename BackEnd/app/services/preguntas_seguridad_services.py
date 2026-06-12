from fastapi import HTTPException
from sqlmodel import select
from models.modelos import PreguntaSeguridad
from schemas.esquemas import PreguntasSegurdadUpdate

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

def actualizar_pregunta_seguridad_service(pregunta_id: int, data: PreguntasSegurdadUpdate, session):
    pregunta = session.get(PreguntaSeguridad, pregunta_id)
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta de seguridad no encontrada")

    # Actualizar campos permitidos
    if data.pregunta is not None:
        pregunta.pregunta = data.pregunta

    session.add(pregunta)
    session.commit()
    session.refresh(pregunta)

    return {"message": "Pregunta de seguridad actualizada", "pregunta": pregunta}