from fastapi import HTTPException
from models.modelos import UsuarioRespuestaSeguridad, Usuario
from sqlmodel import select, Session
from typing import Optional

#  podria eliminarse este y dejar el filter que igual devuleve la lista de todos los usuarios si no se le pasan filtros, pero lo dejo por si acaso
def obtener_usuarios_service(session):
    usuarios = session.query(Usuario).all()
    if not usuarios:
        raise HTTPException (status_code=404,detail="No se encontraron usuarios")
    
    return usuarios

def crear_usuario_service(data, session):
    nuevo_usuario = Usuario(
        **data.model_dump()
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    
    return nuevo_usuario

def registrar_preguntas_seguridad_service(usuario_id: int, data_respuestas: list, session):
    respuestas_guardadas = []

    for item in data_respuestas:
        nueva_relacion = UsuarioRespuestaSeguridad(
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

def get_usuarios_filtrados_service(
    # en python no se puede poner un atributo obligatorio luego de atributos opcionales por lo que en este caso colocamos la session de primera
    session: Session,
    nombre: Optional[str] = None,
    documento: Optional[str] = None,
    correo: Optional[str] = None,
    rol_id: Optional[int] = None
):
    # filtros dinámicos y opcionales.

    # 1. Traer todos los usuarios
    consulta = select(Usuario)
    
    # 2. Modificamos la consulta dinámicamente según los filtros

    if nombre:
        consulta = consulta.where(Usuario.nombre.contains(nombre))
        
    if documento:
        consulta = consulta.where(Usuario.documento == documento)
        
    if correo:
        consulta = consulta.where(Usuario.correo == correo)
        
    if rol_id:
        consulta = consulta.where(Usuario.rol_id == rol_id)
        
    # 3. Se ejecuta la consulta final en la base de datos
    resultados = session.exec(consulta).all()
    
    return resultados
