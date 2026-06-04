from fastapi import HTTPException
from sqlmodel import Session
from models.modelos import Abono
from sqlmodel import select

# aun no se prueban las funciones

def obtener_ordenes_trabajo_service(session: Session):
    ordenes = session.exec(select(Abono)).all()
    
    if not ordenes:
        raise HTTPException(status_code=404, detail="No se Encontraron Abonos Registradas")
    
    return ordenes

def crear_ordenes_trabajo_service(data, session: Session):
    nueva_orden = Abono(
        **data.model_dump()    
    )
    
    session.add(nueva_orden)
    session.commit()
    session.refresh(nueva_orden)
    
    return nueva_orden

# faltan funciones de filtros y asociar abonos con ordenes 