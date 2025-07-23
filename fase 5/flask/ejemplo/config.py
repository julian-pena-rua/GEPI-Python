# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base de datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'universidad')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Base de datos limpia (data warehouse)
    DW_HOST = os.getenv('DW_HOST', 'localhost')
    DW_PORT = os.getenv('DW_PORT', '5432')
    DW_NAME = os.getenv('DW_NAME', 'universidad_dw')
    DW_USER = os.getenv('DW_USER', 'postgres')
    DW_PASSWORD = os.getenv('DW_PASSWORD', '')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Configuraciones ETL
    BATCH_SIZE = 1000
    LOG_LEVEL = 'INFO'
    
    @property
    def SOURCE_DATABASE_URI(self):
        #engine = create_engine("mysql+pymysql://user:password@host/database?charset=utf8mb4")
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
    
    @property
    def TARGET_DATABASE_URI(self):
        return f"postgresql://{self.DW_USER}:{self.DW_PASSWORD}@{self.DW_HOST}:{self.DW_PORT}/{self.DW_NAME}?client_encoding=utf8"

