from fastapi import HTTPException
from models.modelos import Material
from sqlmodel import select
from schemas.esquemas import MaterialCreate


#los materiales se gastaran en las ordenes de trabajo, por lo que no se eliminaran, solo se podran crear nuevos materiales y consultar los existentes, pero no eliminar ni modificar los materiales ya creados, esto es para mantener un historial de los materiales utilizados en cada orden de trabajo. No se si sea buena idea poner algo de material utilizado como un estado 

def obtener_materiales_service(session):
    materiales = session.exec(select(Material)).all()
    if not materiales:
        raise HTTPException(status_code=404, detail="No se encontraron materiales")
    return materiales

#  funcion para crear materiales
def crear_materiales_service(data, session):
    nuevo_material = Material(
        **data.model_dump()
    )
    
    # Validar material existente 
    if session.exec(select(Material).where(Material.nombre == nuevo_material.nombre)).first():
        raise HTTPException(status_code= 400, detail="El material ya existe")
    
    session.add(nuevo_material)
    session.commit()
    session.refresh(nuevo_material)

    return nuevo_material

def sumar_materiales_service(data, session):
    
    material = session.get(Material, data.id)
    
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    
    material.stock_disponible += data.cantidad_a_sumar
    
    session.add(material)
    session.commit()
    session.refresh(material)
    
    return material