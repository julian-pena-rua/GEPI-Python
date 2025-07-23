# run_etl.py - Script principal para ejecutar ETL manualmente
#!/usr/bin/env python3
"""
Script principal para ejecutar el proceso ETL
Uso: python run_etl.py [--schedule]
"""

import argparse
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

from etl.data_processor import DataProcessor
from scheduler import ETLScheduler
from config import Config

def create_directories():
    """Crea directorios necesarios"""
    dirs = ['fase 5/flask/ejemplo/etl/logs', 
            'fase 5/flask/ejemplo/static/css', 
            'fase 5/flask/ejemplo/static/js', 
            'fase 5/flask/ejemplo/templates']
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def run_etl_once():
    """Ejecuta el proceso ETL una sola vez"""
    config = Config()
    processor = DataProcessor(
        config.SOURCE_DATABASE_URI,
        config.TARGET_DATABASE_URI
    )
    
    print("Iniciando proceso ETL...")
    result = processor.run_etl_process()
    
    if result['status'] == 'success':
        print(f"✅ ETL completado exitosamente!")
        print(f"📊 Registros procesados: {result['records_processed']}")
        print(f"⏰ Timestamp: {result['timestamp']}")
    else:
        print(f"❌ Error en ETL: {result['error']}")
        sys.exit(1)

def run_scheduler():
    """Ejecuta el programador ETL"""
    print("Iniciando programador ETL...")
    scheduler = ETLScheduler()
    scheduler.start_scheduler()

def main():
    parser = argparse.ArgumentParser(description='Ejecutar proceso ETL')
    parser.add_argument('--schedule', action='store_true', 
                       help='Ejecutar en modo programado (continuo)')
    parser.add_argument('--setup', action='store_true',
                       help='Configurar directorios iniciales')
    
    args = parser.parse_args()
    
    if args.setup:
        create_directories()
        print("✅ Directorios creados correctamente")
        return
    
    # Crear directorios si no existen
    create_directories()
    
    if args.schedule:
        run_scheduler()
    else:
        run_etl_once()

if __name__ == "__main__":
    main()

