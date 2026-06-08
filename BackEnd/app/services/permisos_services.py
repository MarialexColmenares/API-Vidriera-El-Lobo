from fastapi import HTTPException
from models.modelos import Permiso
from sqlmodel import select

def obtener_permisos_service(session):
    permisos = session.exec(select(Permiso)).all()    
    if not permisos: 
        raise HTTPException(status_code=404, detail="No se encontraron permisos")
    return permisos

def obtener_permiso_por_id_service(permiso_id, session):
    permiso = session.get(Permiso, permiso_id)
    if not permiso:
        raise HTTPException(status_code=404, detail="No se encontro el permiso con el ID especificado")
    return permiso

def crear_permiso_service(data, session):
    nuevo_permiso = Permiso(
        **data.model_dump()
    )
    session.add(nuevo_permiso)
    session.commit()
    session.refresh(nuevo_permiso)
    
    return nuevo_permiso

def update_permiso_service(permiso_id, data, session):
    permiso = session.get(Permiso, permiso_id)
    if not permiso:
        raise HTTPException(status_code=404, detail="No se encontro el permiso con el ID especificado")
   
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(permiso, key, value)


    session.add(permiso)
    session.commit()
    session.refresh(permiso)
   
    return permiso