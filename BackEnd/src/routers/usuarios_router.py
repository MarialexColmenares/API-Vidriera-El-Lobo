from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import UsuarioRespuestaSeguridadResponse, usuarioCreate, UsuarioRespuestaSeguridadCreate
from models.modelos import  Usuarios, UsuarioRespuestasSeguridad
from services.usuarios_services import *

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
def obtener_usuarios(
    session: Session = Depends(get_db)
):
    return obtener_usuarios_service(session)

@router.post("/")
def crear_usuario(
    data: usuarioCreate,
    session: Session = Depends(get_db)
):
    return crear_usuario_service(data=data, session=session)


@router.post("/{usuario_id}/preguntas-seguridad", response_model=list[UsuarioRespuestaSeguridadResponse])
def registrar_preguntas_seguridad(
    usuario_id: int, 
    data_respuestas: list[UsuarioRespuestaSeguridadCreate], 
    session: Session = Depends(get_db)
):
    return registrar_preguntas_seguridad_service(usuario_id=usuario_id, data_respuestas=data_respuestas, session=session)


# filtrar usuarios por documento

# este se podria cambiar por un filtro por todos los campos 
@router.get("/documento/{documento}")
def obtener_usuario_por_documento(
    documento: str,
    session: Session = Depends(get_db)
):
    usuario = session.query(Usuarios).filter(Usuarios.documento == documento).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="No se encontró un usuario con el documento proporcionado.")
    
    return usuario