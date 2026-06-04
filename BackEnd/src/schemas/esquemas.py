from pydantic import BaseModel, Field

class PreguntasSegurdadCreate(BaseModel):
    pregunta: str
    class Config:
        from_attributes = True  
        
        json_schema_extra = {
            "example": {
                "pregunta": "¿Cuál fue el nombre de tu primera mascota?"
            }
        }
        
class RolCreate(BaseModel):
    nombre_rol: str
    descripcion: str
    class Config:
        json_schema_extra = {
            "example": {
                "nombre_rol": "cliente",
                "descripcion": "Rol para usuarios clientes"
            }
        }

class PermisoCreate(BaseModel):
    nombre: str
    descripcion: str
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Crear: ordenes",
                "descripcion": "Permiso para crear ordenes de trabajo"
            }
        }

class usuarioCreate(BaseModel):
    nombre: str
    apellido: str
    correo: str
    password: str
    documento: str 
    rol_id: int
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Crear: ordenes",
                "apellido": "Permiso para crear ordenes de trabajo",
                "correo": "persona@examplo.com",
                "password": "contraseña123",
                "documento": "123456789",
                "rol_id": 1
            }
        }
        
# nuevo esquema para leer usuarios 
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: str
    documento: str
    rol_id: int

    class Config:
        from_attributes = True  # En Pydantic v2 (antiguo orm_mode = True) para leer objetos de SQLModel/SQLAlchemy
        
class UsuarioRespuestaSeguridadCreate(BaseModel):
    pregunta_id: int = Field(..., description="El ID de la pregunta predefinida en el catálogo")
    respuesta: str = Field(..., min_length=2, max_length=255, description="La respuesta escrita por el usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "pregunta_id": 1,
                "respuesta": "Mi primer perrito Firulais"
            }
        }
        
class UsuarioRespuestaSeguridadResponse(BaseModel):
    id: int
    usuario_id: int
    pregunta_id: int

    class Config:
        from_attributes = True  # En Pydantic v2 (antiguo orm_mode = True) para leer objetos de SQLModel/SQLAlchemy
        
class OrdenTrabajoCreate(BaseModel):
    descripcion: str
    fecha_inicio: str
    fecha_fin: str #esto no deberia ser str sino date 
    estado: str
    usuario_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "descripcion": "Reparación de aire acondicionado",
                "fecha_inicio": "2024-07-01T10:00:00",
                "fecha_fin": "2024-07-01T12:00:00",
                "estado": "pendiente",
                "usuario_id": 1
            }
        }
        
class MaterialCreate(BaseModel):
    nombre: str 
    espesor_mm: float
    color: str
    stock_disponible: float  # estaba dudando si poner cantidad aqui o en un almacen de stock, pero creo que es mejor ponerlo aqui para tener un control de la cantidad total de cada material, y luego en el stock solo se restaria la cantidad utilizada en cada orden de trabajo, asi se mantiene un historial de los materiales utilizados en cada orden de trabajo y no se pierde informacion al eliminar materiales del stock. Ademas, si se necesita agregar mas materiales en el futuro, solo se tendria que crear un nuevo registro en esta tabla sin afectar el historial de los materiales utilizados en las ordenes de trabajo anteriores.
    precio_m2: float
    
    

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Tornillo M8",
                "espesor_mm": 8.0,
                "color": "Plateado",
                "stock_disponible": 100.0,
                "precio_m2": 10.0
            }
        }

class MaterialUpdate(BaseModel):
    id: int
    cantidad_a_sumar: float

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "cantidad_a_sumar": 50.0
            }
        }
