from fastapi import HTTPException
from sqlmodel import Session, select
from models.modelos import Rol

def obtener_roles_services(session):
    roles = session.exec(select(Rol)).all()
    if not roles:
        raise HTTPException (status_code=404,detail="No se encontraron roles")
    return roles

def crear_rol_service(data, session):
    nuevo_rol = Rol(
        **data.model_dump()
    )
    
    session.add(nuevo_rol)
    session.commit()
    session.refresh(nuevo_rol)
    
    return {"message": "Rol creado exitosamente", "Rol": nuevo_rol}

def asociar_permiso_a_rol_service(rol_id: int, permiso_id: int, session: Session):
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

def obtener_permisos_de_rol_service(rol_nombre: str, session: Session):
    rol = session.query(Rol).filter(Rol.nombre_rol == rol_nombre).first()
    if not rol:
        raise HTTPException(status_code=404, detail="El rol especificado no existe.")
    
    return {"permisos": rol.permisos}