from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from services.materiales_services import *
from schemas.esquemas import MaterialCreate, MaterialUpdate, MaterialSumar

router = APIRouter(prefix="/materiales", tags=["Materiales"])

@router.get("/") 
def obtener_materiales(session: Session = Depends(get_db)):
    return obtener_materiales_service(session)

@router.post("/", status_code=201)
def crear_materiales(data: MaterialCreate, session: Session = Depends(get_db)):
    return crear_materiales_service(data, session)

@router.patch("/{id_material}")
def actualizar_material(id_material: int, data: MaterialUpdate, session: Session = Depends(get_db)):
    return actualizar_material_service(data=data, id_material=id_material, session=session)

@router.patch("/sumar") 
def sumar_materiales(data: MaterialSumar, session: Session = Depends(get_db)):
    return sumar_materiales_service(data, session)

