from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.conexion import get_db
from services.materiales_services import *

router = APIRouter(prefix="/materiales", tags=["Materiales"])

@router.get("/")
def obtener_materiales(session: Session = Depends(get_db)):
    return obtener_materiales_service(session)