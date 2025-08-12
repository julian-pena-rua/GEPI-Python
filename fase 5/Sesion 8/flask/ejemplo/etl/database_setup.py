# etl/database_setup.py - Configuración de base de datos
from sqlalchemy import create_engine, text
import logging

class DatabaseSetup:
    def __init__(self, target_uri: str):
        self.engine = create_engine(target_uri)
        self.logger = logging.getLogger(__name__)
    
    def create_tables(self):
        """Crea las tablas necesarias en el data warehouse"""
        
        # Tabla principal de estudiantes limpios
        create_students_table = """
        CREATE TABLE IF NOT EXISTS estudiantes_limpios (
            id_estudiante INTEGER PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            nombre_completo VARCHAR(200) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            email_valido BOOLEAN DEFAULT TRUE,
            telefono VARCHAR(20),
            fecha_nacimiento DATE,
            edad INTEGER,
            nacionalidad VARCHAR(50),
            programa_academico VARCHAR(100),
            semestre INTEGER,
            promedio DECIMAL(3,2),
            categoria_rendimiento VARCHAR(20),
            estado VARCHAR(20),
            fecha_ingreso DATE,
            anio_ingreso INTEGER,
            mes_ingreso INTEGER,
            ciudad_origen VARCHAR(100),
            fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_students_table))
                conn.commit()
            self.logger.info("Tablas creadas correctamente en el data warehouse")
        except Exception as e:
            self.logger.error(f"Error creando tablas: {str(e)}")
            raise
