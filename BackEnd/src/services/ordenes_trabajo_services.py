from fastapi import HTTPException
from sqlmodel import Session
from models.modelos import OrdenTrabajo
from sqlmodel import select

# aun no se prueban las funciones


def obtener_ordenes_trabajo_service(session: Session):
    ordenes = session.exec(select(OrdenTrabajo)).all()
    
    if not ordenes:
        raise HTTPException(status_code=404, detail="No se Encontraron Ordenes Registradas")
    
    return ordenes

def crear_ordenes_trabajo_service(data, session: Session):
    nueva_orden = OrdenTrabajo(
        **data.model_dump()     
    )
    
    session.add(nueva_orden)
    session.commit()
    session.refresh(nueva_orden)
    
    return nueva_orden

# faltya asociar ordenes con abonos 

#estado de orden
def estado_orden_service(id_orden, nuevo_estado, session):
    orden = session.get(OrdenTrabajo, id_orden)
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden.estado = nuevo_estado
    
    session.add(orden)
    session.commit()
    session.refresh(orden)
    
    return orden