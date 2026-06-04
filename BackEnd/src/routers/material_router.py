from fastapi import APIRouter, Depends
from sqlmodel import Session
from database.conexion import get_db
from services.materiales_services import *
from schemas.esquemas import MaterialCreate, MaterialUpdate

router = APIRouter(prefix="/materiales", tags=["Materiales"])

@router.get("/") 
def obtener_materiales(session: Session = Depends(get_db)):
    return obtener_materiales_service(session)

@router.post("/", status_code=201)
def crear_materiales(data: MaterialCreate, session: Session = Depends(get_db)):
    return crear_materiales_service(data, session)

@router.patch("/sumar") 
def sumar_materiales(data: MaterialUpdate, session: Session = Depends(get_db)):
    return sumar_materiales_service(data, session)