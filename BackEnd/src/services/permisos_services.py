from fastapi import HTTPException
from models.modelos import Permiso
from sqlmodel import select

def obtener_permisos_service(session):
    permisos = session.exec(select(Permiso)).all()    
    if not permisos: 
        raise HTTPException(status_code=404, detail="No se encontraron permisos")
    return {"permisos": permisos}

def crear_permiso_service(data, session):
    nuevo_permiso = Permiso(
        **data.model_dump()
    )
    session.add(nuevo_permiso)
    session.commit()
    session.refresh(nuevo_permiso)
    
    return {"message": "Permiso creado exitosamente", "permiso": nuevo_permiso}