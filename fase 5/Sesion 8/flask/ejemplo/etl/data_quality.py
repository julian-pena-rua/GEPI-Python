# etl/data_quality.py - Módulo de calidad de datos
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

class DataQualityValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.quality_report = {
            'total_records': 0,
            'valid_records': 0,
            'issues': []
        }
    
    def validate_emails(self, df: pd.DataFrame) -> pd.DataFrame:
        """Valida formato de emails"""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        invalid_emails = df[~df['email'].str.match(email_pattern, na=False)]
        
        if len(invalid_emails) > 0:
            self.quality_report['issues'].append({
                'type': 'invalid_emails',
                'count': len(invalid_emails),
                'percentage': (len(invalid_emails) / len(df)) * 100
            })
            
            self.logger.warning(f"Encontrados {len(invalid_emails)} emails inválidos")
        
        return df
    
    def validate_academic_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Valida datos académicos"""
        # Validar promedios
        invalid_grades = df[(df['promedio'] < 0) | (df['promedio'] > 5.0)]
        if len(invalid_grades) > 0:
            self.quality_report['issues'].append({
                'type': 'invalid_grades',
                'count': len(invalid_grades),
                'details': 'Promedios fuera del rango 0-5.0'
            })
        
        # Validar semestres
        invalid_semesters = df[(df['semestre'] < 1) | (df['semestre'] > 12)]
        if len(invalid_semesters) > 0:
            self.quality_report['issues'].append({
                'type': 'invalid_semesters',
                'count': len(invalid_semesters),
                'details': 'Semestres fuera del rango 1-12'
            })
        
        return df
    
    def check_completeness(self, df: pd.DataFrame, required_fields: List[str]) -> Dict:
        """Verifica completitud de campos requeridos"""
        completeness = {}
        
        for field in required_fields:
            if field in df.columns:
                null_count = df[field].isnull().sum()
                completeness[field] = {
                    'null_count': null_count,
                    'completeness_percentage': ((len(df) - null_count) / len(df)) * 100
                }
        
        return completeness
    
    def generate_quality_report(self, df: pd.DataFrame) -> Dict:
        """Genera reporte completo de calidad de datos"""
        self.quality_report['total_records'] = len(df)
        
        # Campos requeridos
        required_fields = ['nombre', 'apellido', 'email', 'programa_academico']
        completeness = self.check_completeness(df, required_fields)
        
        # Validaciones específicas
        self.validate_emails(df)
        self.validate_academic_data(df)
        
        # Estadísticas generales
        self.quality_report.update({
            'completeness': completeness,
            'duplicate_emails': df['email'].duplicated().sum(),
            'missing_data_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        })
        
        return self.quality_report

