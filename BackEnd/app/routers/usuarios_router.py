from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from database.conexion import get_db
from schemas.esquemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioRespuestaSeguridadCreate, UsuarioRespuestaSeguridadResponse
from services.usuarios_services import *

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
def obtener_usuarios(
    session: Session = Depends(get_db)
):
    return obtener_usuarios_service(session)

@router.post("/")
def crear_usuario(
    data: UsuarioCreate,
    session: Session = Depends(get_db)
):
    return crear_usuario_service(data=data, session=session)

@router.patch("/{usuario_id}")
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate, session: Session = Depends(get_db)):
    return actualizar_usuario_service(usuario_id=usuario_id, data=data, Session=session)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario_por_id(
    usuario_id: int, 
    session: Session = Depends(get_db)
):
    return obtener_usuario_por_id_service(usuario_id=usuario_id, session=session)


@router.post("/{usuario_id}/preguntas-seguridad", response_model=list[UsuarioRespuestaSeguridadResponse])
def registrar_preguntas_seguridad(
    usuario_id: int, 
    data_respuestas: list[UsuarioRespuestaSeguridadCreate], 
    session: Session = Depends(get_db)
):
    return registrar_preguntas_seguridad_service(usuario_id=usuario_id, data_respuestas=data_respuestas, session=session)

# antes filtraba solo por documento, ahora se puede filtrar por documento, nombre, correo o rol_id. Todos los filtros son opcionales y combinables entre sí.
@router.get("/filter/", response_model=list[UsuarioResponse])
def get_usuarios_filter(
    session: Session = Depends(get_db),
    # aqui el Query recalca que es un query parameter y permite agregarle una descripción que se verá en la documentación de FastAPI
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    documento: Optional[str] = Query(None, description="Filtrar por documento"),
    correo: Optional[str] = Query(None, description="Filtrar por correo"),
    rol_id: Optional[int] = Query(None, description="Filtrar por rol_id") # luego se podria colocar para que filtre por el nombre del rol en vez del id, pero eso implicaría hacer un join con la tabla de roles, lo cual es un poco más complejo. Por ahora lo dejo así para que sea más sencillo de implementar
):

    # Endpoint para listar usuarios. Todos los filtros son opcionales.
    # Si no se envía ninguno, devolverá la lista completa.
    
    # Pasamos los parámetros sueltos directamente al servicio
    usuarios = get_usuarios_filtrados_service(
        session=session,
        nombre=nombre,
        documento=documento,
        correo=correo,
        rol_id=rol_id
    )
    return usuarios

# PUEDO AGREGAR UN FILTER A TODAS LAS ENTIDADES ?