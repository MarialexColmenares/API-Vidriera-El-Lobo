from fastapi import HTTPException
from database.conexion import get_db
from models.modelos import Permisos
from sqlmodel import select

def obtener_permisos_service(session):
    permisos = session.exec(select(Permisos)).all()    
    if not permisos: 
        raise HTTPException(status_code=404, detail="No se encontraron permisos")
    return {"permisos": permisos}

def crear_permiso_service(data, session):
    nuevo_permiso = Permisos(
        **data.model_dump()
    )
    session.add(nuevo_permiso)
    session.commit()
    session.refresh(nuevo_permiso)
    
    return {"message": "Permiso creado exitosamente", "permiso": nuevo_permiso}