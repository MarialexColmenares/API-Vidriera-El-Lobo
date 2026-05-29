from database.conexion import get_db
from models.modelos import Material
from sqlmodel import select

def obtener_materiales_service(session = get_db()):
    materiales = session.exec(select(Material)).all()
    return materiales
