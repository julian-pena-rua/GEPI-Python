# etl/scheduler.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import scheduler
import time
import logging
import os
import signal
import sys
from datetime import datetime
from data_processor import DataProcessor
from config import Config

class ETLScheduler:
    def __init__(self, schedule_time="02:00", interval_hours=None):
        self.config = Config()
        self.processor = DataProcessor(
            self.config.SOURCE_DATABASE_URI,
            self.config.TARGET_DATABASE_URI
        )
        self.schedule_time = schedule_time
        self.interval_hours = interval_hours
        self.setup_logging()
        self.should_stop = False
        self.ensure_log_directory()
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
    
    def ensure_log_directory(self):
        log_dir = os.path.dirname('etl/logs/scheduler.log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('etl/logs/scheduler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_scheduled_etl(self):
        """Ejecuta el proceso ETL programado"""
        self.logger.info("=== INICIANDO ETL PROGRAMADO ===")
        try:
            result = self.processor.run_etl_process()
            self.logger.info(f"ETL completado: {result}")
        except Exception as e:
            self.logger.error(f"Error en ETL programado: {str(e)}")
    
    def start_scheduler(self):
        """Inicia el programador de tareas"""
        if self.interval_hours:
            self.logger.info(f"Programando ETL cada {self.interval_hours} horas")
            scheduler.every(self.interval_hours).hours.do(self.run_scheduled_etl)
        else:
            self.logger.info(f"Programando ETL diario a las {self.schedule_time}")
            scheduler.every().day.at(self.schedule_time).do(self.run_scheduled_etl)
        
        self.logger.info("Programador ETL iniciado")
        
        while not self.should_stop:
            scheduler.run_pending()
            time.sleep(60)  # Verificar cada minuto
        
        self.logger.info("Programador ETL detenido")
    
    def handle_shutdown(self, signum, frame):
        self.logger.info(f"Recibida señal de terminación ({signum}), deteniendo scheduler...")
        self.should_stop = True

def create_directories():
    """Crea directorios necesarios"""
    dirs = ['etl/logs', 'static/css', 'static/js', 'templates']
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

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

def run_scheduler(schedule_time="02:00", interval_hours=None):
    """Ejecuta el programador ETL"""
    print("Iniciando programador ETL...")
    scheduler = ETLScheduler(schedule_time, interval_hours)
    scheduler.start_scheduler()

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Ejecutar proceso ETL')
    parser.add_argument('--schedule', action='store_true', 
                       help='Ejecutar en modo programado (continuo)')
    parser.add_argument('--setup', action='store_true',
                       help='Configurar directorios iniciales')
    parser.add_argument('--time', type=str, default="02:00",
                       help='Hora para ejecutar ETL diario (formato HH:MM)')
    parser.add_argument('--interval', type=int, default=None,
                       help='Intervalo en horas para ejecutar ETL repetidamente')
    
    args = parser.parse_args()
    
    if args.setup:
        create_directories()
        print("✅ Directorios creados correctamente")
        return
    
    # Crear directorios si no existen
    create_directories()
    
    if args.schedule:
        run_scheduler(args.time, args.interval)
    else:
        run_etl_once()

if __name__ == "__main__":
    main()

