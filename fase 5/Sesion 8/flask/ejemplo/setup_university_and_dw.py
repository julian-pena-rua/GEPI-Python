import os
from config import Config
from sqlalchemy import create_engine, text
import logging

class DatabaseSetup:
    def __init__(self, target_uri: str):
        self.engine = create_engine(target_uri)
        self.logger = logging.getLogger(__name__)
    
    def create_tables(self):
        """Crea las tablas necesarias en el data warehouse"""
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

def execute_sql_file(engine, filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        sql_commands = file.read()
    with engine.connect() as conn:
        for command in sql_commands.split(';'):
            cmd = command.strip()
            if cmd:
                conn.execute(text(cmd))
        conn.commit()

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Database URIs - adjust as needed
    config = Config()
    source_db_uri = os.getenv('SOURCE_DB_URI', config.SOURCE_DATABASE_URI)
    dw_db_uri = os.getenv('DW_DB_URI', config.TARGET_DATABASE_URI)

    # Create engines
    source_engine = create_engine(source_db_uri)
    dw_engine = create_engine(dw_db_uri)

    try:
        logger.info("Creando tabla fuente en la base de datos universidad...")
        create_source_sql_path = os.path.join(os.path.dirname(__file__), 'etl\\create_source_table.sql')
        execute_sql_file(source_engine, create_source_sql_path)
        logger.info("Tabla fuente creada correctamente.")

        logger.info("Insertando datos de prueba en la base de datos universidad...")
        insert_test_data_path = os.path.join(os.path.dirname(__file__), 'etl\\insert_test_data.sql')
        execute_sql_file(source_engine, insert_test_data_path)
        logger.info("Datos de prueba insertados correctamente.")

        logger.info("Creando tablas en el data warehouse...")
        db_setup = DatabaseSetup(dw_db_uri)
        db_setup.create_tables()
        logger.info("Tablas del data warehouse creadas correctamente.")

    except Exception as e:
        logger.error(f"Error durante la configuración de la base de datos: {str(e)}")

if __name__ == '__main__':
    main()
