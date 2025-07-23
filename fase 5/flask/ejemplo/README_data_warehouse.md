# Configuración del Data Warehouse para PostgreSQL

Este proyecto contiene archivos para configurar y poblar un data warehouse en PostgreSQL.

## Archivos

- `data_warehouse_create_table.sql`: Script SQL para crear la tabla principal del data warehouse `estudiantes_limpios`.
- `database_setup.py`: Script en Python para crear las tablas necesarias en el data warehouse usando SQLAlchemy.
- `data_processor.py`: Script en Python que implementa el proceso ETL:
  - Extraer datos de la base de datos fuente.
  - Limpiar y transformar los datos.
  - Cargar los datos en la tabla del data warehouse.

## Uso

1. Ejecutar `database_setup.py` para crear las tablas en el data warehouse de PostgreSQL.
2. Configurar las URIs de la base de datos fuente y destino en `data_processor.py`.
3. Ejecutar el proceso ETL usando `data_processor.py` para extraer, transformar y cargar los datos.

## Registro (Logging)

Los registros del proceso ETL se guardan en `etl/logs/etl_process.log`.

## Notas

- El esquema de la tabla del data warehouse está diseñado para datos de estudiantes con campos como nombre, correo electrónico, nacionalidad, programa académico y categoría de desempeño.
- El proceso ETL incluye pasos de validación y normalización de datos.
