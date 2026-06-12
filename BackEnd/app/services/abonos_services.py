from fastapi import HTTPException
from models.modelos import Abono
from sqlmodel import select

def obtener_abonos_service(session):
    abonos = session.exec(select(Abono)).all()
    
    if not abonos:
        raise HTTPException(status_code=404, detail="No hay Abonos Registrados")
    
    return abonos

def crear_abono_service(data, session):
    #  aqui deberia evaluar si la orden ya fue pagada en su totalidad 
    
    nuevo_abono = Abono(
        **data.model_dump()
    )
    
    session.add(nuevo_abono)
    session.commit()
    session.refresh(nuevo_abono)
    
    return nuevo_abono
    
def obtener_abono_id_service(id_abono, session):
    abono = session.get(Abono, id_abono)
    
    if not abono:
        raise HTTPException(status_code=404, detail="No existe ese Abono")
    
    return abono
