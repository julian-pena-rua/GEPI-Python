import pandas as pd
import numpy as np
import re
from unidecode import unidecode
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

class DataProcessor:
    def __init__(self, source_uri: str, target_uri: str):
        self.source_engine = create_engine(source_uri)
        self.target_engine = create_engine(target_uri)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('etl/logs/etl_process.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def extract_data(self) -> pd.DataFrame:
        query = """
        SELECT 
            id_estudiante,
            nombre,
            apellido,
            email,
            telefono,
            fecha_nacimiento,
            nacionalidad,
            programa_academico,
            semestre,
            promedio,
            estado,
            fecha_ingreso,
            ciudad_origen
        FROM estudiantes
        """
        try:
            df = pd.read_sql(query, self.source_engine)
            self.logger.info(f"Extraídos {len(df)} registros de la base de datos origen")
            return df
        except Exception as e:
            self.logger.error(f"Error en extracción: {str(e)}")
            raise
    
    def clean_names(self, text: str) -> str:
        if pd.isna(text) or text == '':
            return ''
        text = str(text).strip()
        text = text.lower()
        replacements = {
            'jose': 'josé',
            'maria': 'maría',
            'jesus': 'jesús',
            'monica': 'mónica',
            'sebastian': 'sebastián',
            'adrian': 'adrián',
            'martin': 'martín',
            'victor': 'víctor',
            'hector': 'héctor',
            'oscar': 'óscar',
            'cesar': 'césar',
            'ruben': 'rubén',
            'raul': 'raúl',
            'angel': 'ángel',
            'andres': 'andrés',
            'nicolas': 'nicolás',
            'fabian': 'fabián',
            'german': 'germán',
            'hernan': 'hernán',
            'julian': 'julián',
            'adrian': 'adrián',
            'dario': 'darío',
            'mario': 'mario',
            'patricia': 'patricia',
            'veronica': 'verónica',
            'beatriz': 'beatriz',
            'ines': 'inés',
            'angeles': 'ángeles',
            'soledad': 'soledad',
            'belen': 'belén',
            'natalia': 'natalia',
            'alejandra': 'alejandra',
            'elizabeth': 'elizabeth'
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
        text = ' '.join(word.capitalize() for word in text.split())
        return text
    
    def normalize_nationality(self, nationality: str) -> str:
        if pd.isna(nationality) or nationality == '':
            return 'No especificado'
        nationality = str(nationality).lower().strip()
        nationality_map = {
            'colombia': 'Colombiano/a',
            'colombiano': 'Colombiano/a',
            'colombiana': 'Colombiano/a',
            'col': 'Colombiano/a',
            'venezuela': 'Venezolano/a',
            'venezolano': 'Venezolano/a',
            'venezolana': 'Venezolano/a',
            'ven': 'Venezolano/a',
            'ecuador': 'Ecuatoriano/a',
            'ecuatoriano': 'Ecuatoriano/a',
            'ecuatoriana': 'Ecuatoriano/a',
            'ecu': 'Ecuatoriano/a',
            'peru': 'Peruano/a',
            'peruano': 'Peruano/a',
            'peruana': 'Peruano/a',
            'per': 'Peruano/a',
            'brasil': 'Brasileño/a',
            'brazil': 'Brasileño/a',
            'brasileño': 'Brasileño/a',
            'brasileña': 'Brasileño/a',
            'bra': 'Brasileño/a',
            'argentina': 'Argentino/a',
            'argentino': 'Argentino/a',
            'argentina': 'Argentino/a',
            'arg': 'Argentino/a',
            'chile': 'Chileno/a',
            'chileno': 'Chileno/a',
            'chilena': 'Chileno/a',
            'chi': 'Chileno/a',
            'mexico': 'Mexicano/a',
            'mexicano': 'Mexicano/a',
            'mexicana': 'Mexicano/a',
            'mex': 'Mexicano/a',
            'españa': 'Español/a',
            'spain': 'Español/a',
            'español': 'Español/a',
            'española': 'Español/a',
            'esp': 'Español/a',
            'estados unidos': 'Estadounidense',
            'usa': 'Estadounidense',
            'us': 'Estadounidense',
            'american': 'Estadounidense',
            'estadounidense': 'Estadounidense'
        }
        return nationality_map.get(nationality, 'Otro')
    
    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        initial_count = len(df)
        df = df.drop_duplicates()
        df = df.drop_duplicates(subset=['email'], keep='first')
        df['nombre_completo'] = df['nombre'] + ' ' + df['apellido']
        df = df.drop_duplicates(subset=['nombre_completo', 'fecha_nacimiento'], keep='first')
        final_count = len(df)
        removed = initial_count - final_count
        self.logger.info(f"Eliminados {removed} registros duplicados")
        return df.drop('nombre_completo', axis=1)
    
    def validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        df['email_valido'] = df['email'].apply(
            lambda x: bool(re.match(email_pattern, str(x))) if pd.notna(x) else False
        )
        df['promedio'] = pd.to_numeric(df['promedio'], errors='coerce')
        df.loc[df['promedio'] > 5.0, 'promedio'] = np.nan
        df.loc[df['promedio'] < 0.0, 'promedio'] = np.nan
        df['semestre'] = pd.to_numeric(df['semestre'], errors='coerce')
        df.loc[df['semestre'] > 12, 'semestre'] = np.nan
        df.loc[df['semestre'] < 1, 'semestre'] = np.nan
        df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'], errors='coerce')
        df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'], errors='coerce')
        df['edad'] = (datetime.now() - df['fecha_nacimiento']).dt.days // 365
        return df
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Iniciando transformación de datos...")
        df = self.remove_duplicates(df)
        df['nombre'] = df['nombre'].apply(self.clean_names)
        df['apellido'] = df['apellido'].apply(self.clean_names)
        df['nacionalidad'] = df['nacionalidad'].apply(self.normalize_nationality)
        df = self.validate_data(df)
        df['nombre_completo'] = df['nombre'] + ' ' + df['apellido']
        df['anio_ingreso'] = df['fecha_ingreso'].dt.year
        df['mes_ingreso'] = df['fecha_ingreso'].dt.month
        df['categoria_rendimiento'] = pd.cut(
            df['promedio'], 
            bins=[0, 3.0, 3.5, 4.0, 4.5, 5.0],
            labels=['Bajo', 'Regular', 'Bueno', 'Muy Bueno', 'Excelente'],
            include_lowest=True
        )
        self.logger.info("Transformación completada")
        return df
    
    def load_data(self, df: pd.DataFrame):
        try:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS estudiantes_limpios (
                id_estudiante INTEGER PRIMARY KEY,
                nombre VARCHAR(100),
                apellido VARCHAR(100),
                nombre_completo VARCHAR(200),
                email VARCHAR(150),
                email_valido BOOLEAN,
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
            with self.target_engine.connect() as conn:
                conn.execute(text(create_table_sql))
                conn.commit()
            df.to_sql('estudiantes_limpios', self.target_engine, 
                     if_exists='replace', index=False, method='multi')
            self.logger.info(f"Cargados {len(df)} registros al data warehouse")
        except Exception as e:
            self.logger.error(f"Error en carga: {str(e)}")
            raise
    
    def run_etl_process(self):
        self.logger.info("=== INICIANDO PROCESO ETL ===")
        try:
            raw_data = self.extract_data()
            clean_data = self.transform_data(raw_data)
            self.load_data(clean_data)
            self.logger.info("=== PROCESO ETL COMPLETADO EXITOSAMENTE ===")
            return {
                'status': 'success',
                'records_processed': len(clean_data),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error en proceso ETL: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
