from fastapi import HTTPException
from models.modelos import UsuarioRespuestasSeguridad, Usuarios

def obtener_usuarios_service(session):
    usuarios = session.query(Usuarios).all()
    if not usuarios:
        raise HTTPException (status_code=404,detail="No se encontraron usuarios")
    
    return usuarios

def crear_usuario_service(data, session):
    nuevo_usuario = Usuarios(
        **data.model_dump()
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    
    return nuevo_usuario

def registrar_preguntas_seguridad_service(usuario_id: int, data_respuestas: list, session):
    respuestas_guardadas = []

    for item in data_respuestas:
        nueva_relacion = UsuarioRespuestasSeguridad(
            usuario_id=usuario_id,
            pregunta_id=item.pregunta_id,
            respuesta=item.respuesta
        )
        session.add(nueva_relacion)
        respuestas_guardadas.append(nueva_relacion)

    session.commit()
    for resp in respuestas_guardadas:
        session.refresh(resp)

    return respuestas_guardadas