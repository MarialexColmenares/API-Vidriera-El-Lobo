from typing import Optional, List
from datetime import datetime, date 
from sqlmodel import Field, SQLModel, Relationship

class Rol_Permiso(SQLModel, table=True):
    __tablename__: str = "roles_permisos"
    
    # utiliza llave primaria compuesta por rol_id y permiso_id
    rol_id: int = Field(foreign_key="roles.id", primary_key=True)
    permiso_id: int = Field(foreign_key="permisos.id", primary_key=True)

class Permiso(SQLModel, table=True):
    __tablename__: str = "permisos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    nombre: str = Field(unique=True, index=True)
    descripcion: str
    
    roles: List["Rol"] = Relationship(back_populates="permisos", link_model=Rol_Permiso) # relacion a muchos roles a traves de la tabla intermedia Rol_Permiso

class Rol(SQLModel, table=True):
    __tablename__: str = "roles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_rol: str = Field(unique=True, index=True)
    descripcion: str
    
    usuarios: List["Usuario"] = Relationship(back_populates="rol") # relacion a muchos usuarios
    permisos: List[Permiso] = Relationship(back_populates="roles", link_model=Rol_Permiso) # relacion a muchos permisos a traves de la tabla intermedia Rol_Permiso


# los uysuarios necesitaran registrarse un preguntas de seguridad y repuestas
class PreguntaSeguridad(SQLModel, table=True):
    __tablename__: str = "preguntas_seguridad"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    pregunta: str
    
    respuestas: List["UsuarioRespuestaSeguridad"] = Relationship(back_populates="pregunta")
    
class UsuarioRespuestaSeguridad(SQLModel, table=True):
    __tablename__: str = "usuario_respuestas_seguridad"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # llaves foraneas para saber de quien son estas respuestas y a que pregunta corresponden
    usuario_id: int = Field(foreign_key="usuarios.id")
    pregunta_id: int = Field(foreign_key="preguntas_seguridad.id")
    respuesta: str 
    
    # relacion con usuario y pregunta para facilitar consultas
    usuario: Optional["Usuario"] = Relationship(back_populates="respuestas_seguridad")
    pregunta: Optional[PreguntaSeguridad] = Relationship(back_populates="respuestas")

#  Tabla Unica de Actores
class Usuario(SQLModel, table=True):
    __tablename__: str = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    correo: str = Field(unique=True, index=True)
    password: str
    documento: str = Field(unique=True, index=True)
    
    rol_id: int = Field(foreign_key="roles.id")
    # Son obligatorios para los clientes pero no para los vendedores, por eso se pueden dejar como opcionales, el vendedor puede registrarse sin necesidad de colocar estos datos pero el cliente si debe colocarlos
    telefono: Optional[str] = Field(default=None, index=True)
    direccion: Optional[str] = Field(default=None)
    

    # Relaciones existentes
    rol: Optional["Rol"] = Relationship(back_populates="usuarios")
    respuestas_seguridad: List["UsuarioRespuestaSeguridad"] = Relationship(back_populates="usuario")
    
    # Relaciones para las Órdenes (Doble vía)
    ordenes: List["OrdenTrabajo"] = Relationship(
        back_populates="cliente", 
        sa_relationship_kwargs={"foreign_keys": "[OrdenTrabajo.cliente_id]"}
        # Esto le dice a SQLAlchemy: "Oye, cuando vayas a buscar al vendedor, usa la columna vendedor_id, no te confundas con la de cliente_id". Es obligatorio cuando una tabla tiene más de una relación hacia otra misma tabla.
    )
    ordenes_vendidas: List["OrdenTrabajo"] = Relationship(
        back_populates="vendedor", 
        sa_relationship_kwargs={"foreign_keys": "[OrdenTrabajo.vendedor_id]"}
    )

class Material(SQLModel, table=True):
    __tablename__: str = "material"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    espesor_mm: float
    color: str
    stock_disponible: float # el material lleva el estock en la misma tabla para facilitar la consulta y actualizacion del stock
    precio_m2: float
    
class OrdenTrabajo(SQLModel, table=True):
    __tablename__: str = "orden"

    id: Optional[int] = Field(default=None, primary_key=True)
    codigo_orden: str = Field(unique=True, index=True)
    
    # Llaves foráneas apuntando a la misma tabla (usuarios)
    cliente_id: Optional[int] = Field(default=None, foreign_key="usuarios.id")
    vendedor_id: Optional[int] = Field(default=None, foreign_key="usuarios.id") 
    
    fecha_entrega_estimado: date 
    estado: Optional[str] = Field(default="Pendiente") 
    monto_total: Optional[float] = Field(default=None)
    estado_pago: str = Field(default="Pendiente") 

    # Aquí especificamos cuál FK le pertenece a cada relación
    cliente: Optional[Usuario] = Relationship(
        back_populates="ordenes",
        sa_relationship_kwargs={"foreign_keys": "[OrdenTrabajo.cliente_id]"}
    )
    vendedor: Optional[Usuario] = Relationship(
        back_populates="ordenes_vendidas",
        sa_relationship_kwargs={"foreign_keys": "[OrdenTrabajo.vendedor_id]"}
    )
    
    abonos: List["Abono"] = Relationship(back_populates="orden")
# cada orden puede tener varios detalles de orden, cada detalle de orden se relaciona con un material especifico y con una orden especifica

class OrdenDetalle(SQLModel, table=True):
    __tablename__: str = "detalles_de_orden"
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    orden_id: int = Field(foreign_key="orden.id")  
    material_id: int = Field(foreign_key="material.id")
    ancho_m: float
    alto_m: float
    cantidad: int
    
class Abono(SQLModel, table=True):
    __tablename__: str = "abonos" # 

    id: Optional[int] = Field(default=None, primary_key=True) # 
    monto: float = Field(default=0.0) # 
    
    # Usamos datetime.now para que registre la fecha y hora local del servidor al hacer el pago
    fecha_pago: datetime = Field(default_factory=datetime.now) 
    
    metodo_pago: str # Ej: "Efectivo", "Transferencia", "Pago Móvil" 
    observaciones: Optional[str] = Field(default=None) 
    
    orden_id: int = Field(foreign_key="orden.id") 

    # Relación inversa en doble vía con la orden de trabajo
    orden: Optional["OrdenTrabajo"] = Relationship(back_populates="abonos")
    
class trazabilidad(SQLModel, table=True):
    __tablename__: str = "trazabilidad"
    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: int = Field(foreign_key="orden.id")
    etapa: str
    operador_id: Optional[int] = Field(foreign_key="usuarios.id")
    autorizado_por: Optional[int] = Field(foreign_key="usuarios.id")
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = Field(default=None)
    observaciones: Optional[str] = Field(default=None)
