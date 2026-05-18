from pydantic import BaseModel, Field

class PreguntasSegurdadCreate(BaseModel):
    pregunta: str
    
    
    class Config:
        from_atributes = True
        
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