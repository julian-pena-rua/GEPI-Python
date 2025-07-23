# etl/data_processor.py
import pandas as pd
import numpy as np
import re
from unidecode import unidecode
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
from typing import Dict, List, Tuple

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
        """Extrae datos de la base de datos origen"""
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
            # Example for a database that might need explicit encoding in the connection string
            df = pd.read_sql(query, self.source_engine)
            self.logger.info(f"Extraídos {len(df)} registros de la base de datos origen")
            return df
        except Exception as e:
            self.logger.error(f"Error en extracción: {str(e)}")
            raise
    
    @staticmethod
    def clear_characters(text: str) -> str:
        """Reemplaza caracteres acentuados por sus equivalentes sin acento"""
        if text is None or text == '':
            return ''

        # Usar translate para reemplazar caracteres específicos
        # Este método es más eficiente y directo para reemplazar múltiples caracteres
        #text = unidecode(text)  # Elimina acentos y convierte a ASCII
        
        # Reemplazar caracteres acentuados por sus equivalentes sin acento
        clean_text = str(text).translate(str.maketrans({
            'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u',
            'ü': 'u',
            'ä': 'a',
            'ë': 'e',
            'ï': 'i',
            'ö': 'o',
            'ÿ': 'y',
            'à': 'a',
            'è': 'e',
            'ì': 'i',
            'ò': 'o',
            'ù': 'u',
            'â': 'a',
            'ê': 'e',
            'î': 'i',
            'ô': 'o',
            'û': 'u',
            'ã': 'a',
            'õ': 'o',
            'ñ': 'n',
            'ç': 'c',
            'Á': 'A',
            'É': 'E',
            'Í': 'I',
            'Ó': 'O',
            'Ú': 'U',
            'Ü': 'U',
            'Ñ': 'N',
            'Ä': 'A',
            'Ë': 'E',
            'Ï': 'I',
            'Ö': 'O',
            'Ÿ': 'Y',
            'À': 'A',
            'È': 'E',
            'Ì': 'I',
            'Ò': 'O',
            'Ù': 'U',
            'Â': 'A',
            'Ê': 'E',
            'Î': 'I',
            'Ô': 'O',
            'Û': 'U',
            'Ã': 'A',
            'Õ': 'O',
            ' ': ' ',  # Espacio se mantiene igual
            # '  ': ' ',  # Doble espacio se reemplaza por un solo espacio (removed because invalid key for translate)
            # Espacio se mantiene igual
        }))

        # Convertir a string y limpiar espacios
        clean_text = str(clean_text).strip()
        
        # Normalizar a minúsculas
        clean_text = clean_text.lower()
        
        # Capitalizar primera letra de cada palabra
        clean_text = clean_text.title()
        
        return clean_text
    
    def normalize_nationality(self, nationality: str) -> str:
        """Normaliza nacionalidades a categorías estándar"""
        if pd.isna(nationality) or nationality == '':
            return 'No especificado'
        
        nationality = str(nationality).lower().strip()
        
        # Diccionario de normalización de nacionalidades
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
        """Elimina duplicados basándose en múltiples criterios"""
        initial_count = len(df)
        
        # Eliminar duplicados exactos
        df = df.drop_duplicates()
        
        # Eliminar duplicados basados en email (más confiable)
        df = df.drop_duplicates(subset=['email'], keep='first')
        
        # Eliminar duplicados basados en nombre completo y fecha de nacimiento
        df['nombre_completo'] = df['nombre'] + ' ' + df['apellido']
        df = df.drop_duplicates(subset=['nombre_completo', 'fecha_nacimiento'], keep='first')
        
        final_count = len(df)
        removed = initial_count - final_count
        
        self.logger.info(f"Eliminados {removed} registros duplicados")
        
        return df.drop('nombre_completo', axis=1)
    
    def validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Valida y limpia datos inconsistentes"""
        # Validar emails
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        df['email_valido'] = df['email'].apply(
            lambda x: bool(re.match(email_pattern, str(x))) if pd.notna(x) else False
        )
        
        # Validar rangos de promedio (0-5.0 para sistema colombiano)
        df['promedio'] = pd.to_numeric(df['promedio'], errors='coerce')
        df.loc[df['promedio'] > 5.0, 'promedio'] = np.nan
        df.loc[df['promedio'] < 0.0, 'promedio'] = np.nan
        
        # Validar semestre (1-12 típicamente)
        df['semestre'] = pd.to_numeric(df['semestre'], errors='coerce')
        df.loc[df['semestre'] > 12, 'semestre'] = np.nan
        df.loc[df['semestre'] < 1, 'semestre'] = np.nan
        
        # Validar fechas
        df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'], format="%Y-%m-%d", errors='coerce')
        df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso'], format="%Y-%m-%d", errors='coerce')
        
        # Calcular edad
        df['edad'] = (datetime.now() - df['fecha_nacimiento']).dt.days // 365
        
        return df
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica todas las transformaciones de datos"""
        self.logger.info("Iniciando transformación de datos...")
        
        # Eliminar duplicados
        df = self.remove_duplicates(df)
        
        # Limpiar nombres y apellidos
        df['nombre'] = df['nombre'].apply(DataProcessor.clear_characters)
        df['apellido'] = df['apellido'].apply(DataProcessor.clear_characters)
        
        # Normalizar nacionalidades
        df['nacionalidad'] = df['nacionalidad'].apply(self.normalize_nationality)
        
        # Validar datos
        df = self.validate_data(df)
        
        # Agregar campos calculados
        df['nombre_completo'] = df['nombre'] + ' ' + df['apellido']
        df['anio_ingreso'] = df['fecha_ingreso'].dt.year
        df['mes_ingreso'] = df['fecha_ingreso'].dt.month
        
        # Categorizar rendimiento académico
        df['categoria_rendimiento'] = pd.cut(
            df['promedio'], 
            bins=[0, 3.0, 3.5, 4.0, 4.5, 5.0],
            labels=['Bajo', 'Regular', 'Bueno', 'Muy Bueno', 'Excelente'],
            include_lowest=True
        )
        
        self.logger.info("Transformación completada")
        return df
    
    def load_data(self, df: pd.DataFrame):
        """Carga datos transformados al data warehouse"""
        try:
            # Crear tabla si no existe
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
            
            # Insertar datos
            df.to_sql('estudiantes_limpios', self.target_engine, 
                     if_exists='replace', index=False, method='multi')
            
            self.logger.info(f"Cargados {len(df)} registros al data warehouse")
            
        except Exception as e:
            self.logger.error(f"Error en carga: {str(e)}")
            raise
    
    def run_etl_process(self):
        """Ejecuta el proceso ETL completo"""
        try:
            self.logger.info("=== INICIANDO PROCESO ETL ===")
            
            # Extract
            raw_data = self.extract_data()
            
            # Transform
            clean_data = self.transform_data(raw_data)
            
            # Load
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