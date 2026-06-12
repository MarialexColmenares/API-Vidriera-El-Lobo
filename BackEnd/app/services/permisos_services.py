from fastapi import HTTPException
from models.modelos import Permiso
from sqlmodel import select, func

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
    
    # convertimos el nombre que envía el usuario a minúsculas
    nombre_normalizado = data.nombre.strip().lower()
    # .strip() borra todos los espacios en blanco que estén de más al principio y al final del texto.
    
    # buscamos en la base de datos ignorando mayúsculas/minúsculas
    permiso_existente = session.exec(
        select(Permiso).where(func.lower(Permiso.nombre) == nombre_normalizado)
    ).first()
    
    if permiso_existente:
        raise HTTPException(status_code=400, detail="Ya existe un permiso con el mismo nombre")
    
    nuevo_permiso = Permiso(
        nombre=nombre_normalizado,
        descripcion=data.descripcion
    )
    
    session.add(nuevo_permiso)
    session.commit()
    session.refresh(nuevo_permiso)
    
    return nuevo_permiso

def actualizar_permiso_service(permiso_id, data, session):
    permiso = session.get(Permiso, permiso_id)
    if not permiso:
        raise HTTPException(status_code=404, detail="No se encontro el permiso con el ID especificado")
   
    # exclude_unset=True para que solo actualice los campos que el usuario envió en la solicitud
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(permiso, key, value)


    session.add(permiso)
    session.commit()
    session.refresh(permiso)
   
    return permiso
