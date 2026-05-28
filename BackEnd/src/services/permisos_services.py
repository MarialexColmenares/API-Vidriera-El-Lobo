from fastapi import HTTPException
from database.conexion import get_db
from models.modelos import Permisos
from sqlmodel import select

def permisos( session = get_db()):
# Dentro de tu función:
    permisos = session.exec(select(Permisos)).all()    
    if not permisos: 
        raise HTTPException(status_code=404, detail="No se encontraron permisos")
    return {"permisos": permisos}