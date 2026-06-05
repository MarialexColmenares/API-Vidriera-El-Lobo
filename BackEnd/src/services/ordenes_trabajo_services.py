from fastapi import HTTPException
from sqlmodel import Session, select
from datetime import datetime
import random
from models.modelos import OrdenTrabajo, OrdenDetalle, Material
from schemas.esquemas import OrdenTrabajoCreate

def obtener_ordenes_trabajo_service(session: Session):
    ordenes = session.exec(select(OrdenTrabajo)).all()
    
    if not ordenes:
        raise HTTPException(status_code=404, detail="No se Encontraron Ordenes Registradas")
    
    return ordenes

#  por ahora funciona y hace un codigo de orden autogenerado pero me gustariaque el numero-aleatorio sino sumativo para que se lleve como un orden en los codigos de orden 

def crear_orden_con_detalles(data: OrdenTrabajoCreate, session: Session):
    # generar código único para la orden (Ej: ORD-26-XXXX) 
    año_actual = datetime.now().strftime("%y")
    numero_aleatorio = random.randint(1000, 9999)
    codigo_autogenerado = f"ORD-{año_actual}-{numero_aleatorio}"

    # 1. Instanciamos la cabecera de la orden con los datos generales
    nueva_orden = OrdenTrabajo(
        codigo_orden=codigo_autogenerado,
        cliente_id=data.cliente_id,
        fecha_entrega_estimado=data.fecha_entrega_estimado,
        estado="Pendiente",      # Valores por defecto de tus modelos
        estado_pago="Pendiente",
        monto_total=0.0          # Empezamos en 0 para calcularlo abajo
    )
    
    session.add(nueva_orden)
    session.flush() # Envía a Postgres para que genere el ID de la orden sin cerrar la transacción
    
    total_orden = 0.0

    # 2. Recorremos la lista de vidrios del esquema e insertamos en detalles_de_orden
    for item in data.detalles:
        
        # no he probado que si se busque el material 
        precio_por_metro_cuadrado = session.exec(select(Material.precio).where(Material.id == item.material_id)).first()
        
        # Cálculo de metros cuadrados esenciales para el taller
        metros_cuadrados = item.ancho_m * item.alto_m
        costo_detalle = metros_cuadrados * item.cantidad * precio_por_metro_cuadrado
        total_orden += costo_detalle
        
        # Instanciamos el modelo OrdenDetalle usando el orden_id recién obtenido
        nuevo_detalle = OrdenDetalle(
            descripcion=item.descripcion,
            orden_id=nueva_orden.id, # <--- El ID amarrado a la cabecera
            material_id=item.material_id,
            ancho_m=item.ancho_m,
            alto_m=item.alto_m,
            cantidad=item.cantidad
        )
        session.add(nuevo_detalle)
    
    # 3. Asignamos el monto total calculado a la orden
    nueva_orden.monto_total = total_orden
    session.add(nueva_orden)
    
    # Guardamos todo de golpe de forma segura
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





