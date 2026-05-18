from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import UsuarioRespuestaSeguridadResponse, usuarioCreate, UsuarioRespuestaSeguridadCreate
from models.modelos import Rol, Usuarios

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
def obtener_usuarios(
    session: Session = Depends(get_db)
):
    usuarios = session.query(Usuarios).all()
    if not usuarios:
        raise HTTPException (status_code=404,detail="No se encontraron usuarios")
    
    return usuarios

@router.post("/")
def crear_usuario(
    data: usuarioCreate,
    session: Session = Depends(get_db)
):
    nuevo_usuario = Usuarios(
        **data.model_dump()
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    
    return {"message": "Usuario creado exitosamente", "usuario": nuevo_usuario}

@router.post("/{usuario_id}/preguntas-seguridad", response_model=list[UsuarioRespuestaSeguridadResponse])
def registrar_preguntas_seguridad(
    usuario_id: int, 
    data_respuestas: list[UsuarioRespuestaSeguridadCreate], 
    session: Session = Depends(get_db)
):
    respuestas_guardadas = []

    for item in data_respuestas:
        nueva_relacion = UsuarioRespuestaSeguridadCreate(
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