from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from schemas.esquemas import RolCreate
from models.modelos import Rol, Permisos
from database.conexion import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/")
def obtener_roles(
    session: Session = Depends(get_db)
):
    roles = session.query(Rol).all()
    if not roles:
        raise HTTPException (status_code=404,detail="No se encontraron roles")
    return roles

@router.post("/")
def crear_rol(
    data: RolCreate,
    session: Session = Depends(get_db)
):
    nuevo_rol = Rol(
        **data.model_dump()
    )
    
    session.add(nuevo_rol)
    session.commit()
    session.refresh(nuevo_rol)
    
    return {"message": "Rol creado exitosamente", "Rol": nuevo_rol}

@router.post("/{rol_id}/permisos/{permiso_id}")
def asociar_permiso_a_rol(rol_id: int, permiso_id: int, session: Session = Depends(get_db)):
    # 1. Verificar que el rol exista
    rol = session.get(Rol, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="El rol especificado no existe.")
        
    # 2. Verificar que el permiso exista
    permiso = session.get(Permisos, permiso_id)
    if not permiso:
        raise HTTPException(status_code=404, detail="El permiso especificado no existe.")
        
    # 3. Validar si ya tiene asignado el permiso para no duplicarlo en la lista en memoria
    if permiso in rol.permisos:
        raise HTTPException(status_code=400, detail="Este rol ya cuenta con el permiso solicitado.")
        
    # 4. Asignar y guardar cambios
    rol.permisos.append(permiso)
    session.add(rol)
    session.commit()
    
    return {"message": f"Permiso '{permiso.nombre}' asignado correctamente al rol '{rol.nombre_rol}'."}

@router.get("/{rol_nombre}/permisos")
def obtener_permisos_de_rol(
    rol_nombre: str, 
    session: Session = Depends(get_db)
):
    rol = session.query(Rol).filter(Rol.nombre_rol == rol_nombre).first()
    if not rol:
        raise HTTPException(status_code=404, detail="El rol especificado no existe.")
    
    return {"permisos": rol.permisos}