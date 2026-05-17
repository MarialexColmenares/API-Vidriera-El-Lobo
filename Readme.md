# 🐺 API - Vidriería El Lobo

¡Bienvenido! Esta es la API para la gestión y automatización de órdenes de trabajo de **Vidriería El Lobo**. Este sistema fue desarrollado como un proyecto universitario para optimizar el flujo de trabajo, control de inventario y cálculo de costos de la empresa.

---

## 🎯 Objetivos del Proyecto

El sistema está diseñado para cubrir las siguientes necesidades de la empresa:

- **Gestión de Órdenes:** Control total del flujo de trabajo, estados de las órdenes y trazabilidad de cada pedido.
- **Cálculo Automático de Costos:** Automatización del monto total de las órdenes basado en los precios unitarios y dimensiones.
- **Control de Inventario:** Manejo eficiente del catálogo de materiales disponibles en el almacén.
- **Estadísticas Mensuales:** Reportes y métricas de rendimiento para la toma de decisiones.
- **Gestión de Usuarios:** Sistema de autenticación y autorización basado en roles y permisos específicos.

---

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python con [FastAPI](https://fastapi.tiangolo.com/) / [Uvicorn](https://www.uvicorn.org/)
- **Base de Datos:** PostgreSQL
- **ORM / Conector:** (Opcional: puedes agregar aquí si usas SQLAlchemy o Tortoise, por ejemplo)

---

## 🚀 Preparación del Entorno

Sigue estos pasos para clonar el proyecto y ejecutarlo en tu entorno local.

### 1. Requisitos Previos

Asegúrate de tener instalado Python 3.8+ y PostgreSQL en tu equipo.

### 2. Instalar Dependencias

Primero, instala las librerías necesarias utilizando el archivo `requirements.txt`:

```bash
    pip install requirements.txt
```

### 3. Variables de Entorno y Configuración

Para que el proyecto se conecte a la base de datos, debes crear un archivo llamado **datos.py** en la raíz del proyecto e incluir tu cadena de conexión:

```bash
  url_db="postgresql://usuario:contraseña@localhost:puerto/nombre_database”
```

### Ejecutar api

Una vez configurado todo, inicia el servidor de desarrollo con:

```bash
    uvicorn main:app --reload
```

- El servidor se ejecutará en http://127.0.0.1:8000. Puedes acceder a la documentación interactiva de la API en:
  - Swagger UI: http://127.0.0.1:8000/docs
  - ReDoc: http://127.0.0.1:8000/redoc

## 🔗 Creador

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](www.linkedin.com/in/marialex-colmenares-480171388)
