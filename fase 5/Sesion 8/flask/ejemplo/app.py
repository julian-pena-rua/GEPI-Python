# app.py
from flask import Flask, render_template, jsonify, request
import pandas as pd
from sqlalchemy import create_engine, text
import plotly.graph_objs as go
import plotly.utils
import json
from datetime import datetime, timedelta
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Conexión a la base de datos limpia
config = Config()
engine = create_engine(config.TARGET_DATABASE_URI)

class DashboardData:
    def __init__(self, db_engine):
        self.engine = db_engine
    
    def get_basic_stats(self):
        """Obtiene estadísticas básicas"""
        query = """
        SELECT 
            COUNT(*) as total_estudiantes,
            COUNT(DISTINCT programa_academico) as total_programas,
            AVG(promedio) as promedio_general,
            COUNT(DISTINCT nacionalidad) as total_nacionalidades
        FROM estudiantes_limpios
        WHERE promedio IS NOT NULL
        """
        
        with self.engine.connect() as conn:
            result = conn.execute(text(query)).fetchone()
            return {
                'total_estudiantes': result[0],
                'total_programas': result[1],
                'promedio_general': round(result[2], 2) if result[2] else 0,
                'total_nacionalidades': result[3]
            }
    
    def get_students_by_nationality(self):
        """Estudiantes por nacionalidad"""
        query = """
        SELECT nacionalidad, COUNT(*) as cantidad
        FROM estudiantes_limpios
        GROUP BY nacionalidad
        ORDER BY cantidad DESC
        LIMIT 10
        """
        
        df = pd.read_sql(query, self.engine)
        return df.to_dict('records')
    
    def get_students_by_program(self):
        """Estudiantes por programa académico"""
        query = """
        SELECT programa_academico, COUNT(*) as cantidad,
               AVG(promedio) as promedio_programa
        FROM estudiantes_limpios
        WHERE promedio IS NOT NULL
        GROUP BY programa_academico
        ORDER BY cantidad DESC
        LIMIT 15
        """
        
        df = pd.read_sql(query, self.engine)
        df['promedio_programa'] = df['promedio_programa'].round(2)
        return df.to_dict('records')
    
    def get_performance_distribution(self):
        """Distribución de rendimiento académico"""
        query = """
        SELECT categoria_rendimiento, COUNT(*) as cantidad
        FROM estudiantes_limpios
        WHERE categoria_rendimiento IS NOT NULL
        GROUP BY categoria_rendimiento
        ORDER BY 
            CASE categoria_rendimiento
                WHEN 'Excelente' THEN 1
                WHEN 'Muy Bueno' THEN 2
                WHEN 'Bueno' THEN 3
                WHEN 'Regular' THEN 4
                WHEN 'Bajo' THEN 5
            END
        """
        
        df = pd.read_sql(query, self.engine)
        return df.to_dict('records')
    
    def get_enrollment_trends(self):
        """Tendencias de inscripción por año"""
        query = """
        SELECT anio_ingreso, COUNT(*) as nuevos_estudiantes
        FROM estudiantes_limpios
        WHERE anio_ingreso IS NOT NULL
        GROUP BY anio_ingreso
        ORDER BY anio_ingreso
        """
        
        df = pd.read_sql(query, self.engine)
        return df.to_dict('records')
    
    def get_age_distribution(self):
        """Distribución de edades"""
        query = """
        SELECT 
            CASE 
                WHEN edad < 18 THEN 'Menor de 18'
                WHEN edad BETWEEN 18 AND 22 THEN '18-22'
                WHEN edad BETWEEN 23 AND 27 THEN '23-27'
                WHEN edad BETWEEN 28 AND 32 THEN '28-32'
                ELSE 'Mayor de 32'
            END as rango_edad,
            COUNT(*) as cantidad
        FROM estudiantes_limpios
        WHERE edad IS NOT NULL
        GROUP BY 
            CASE 
                WHEN edad < 18 THEN 'Menor de 18'
                WHEN edad BETWEEN 18 AND 22 THEN '18-22'
                WHEN edad BETWEEN 23 AND 27 THEN '23-27'
                WHEN edad BETWEEN 28 AND 32 THEN '28-32'
                ELSE 'Mayor de 32'
            END
        ORDER BY MIN(edad)
        """
        
        df = pd.read_sql(query, self.engine)
        return df.to_dict('records')
    
    def search_students(self, filters):
        """Búsqueda de estudiantes con filtros"""
        base_query = """
        SELECT id_estudiante, nombre_completo, email, programa_academico,
               semestre, promedio, nacionalidad, edad, estado
        FROM estudiantes_limpios
        WHERE 1=1
        """
        
        params = {}
        conditions = []
        
        if filters.get('nombre'):
            conditions.append("(LOWER(nombre_completo) LIKE LOWER(:nombre) OR LOWER(email) LIKE LOWER(:nombre))")
            params['nombre'] = f"%{filters['nombre']}%"
        
        if filters.get('programa'):
            conditions.append("programa_academico = :programa")
            params['programa'] = filters['programa']
        
        if filters.get('nacionalidad'):
            conditions.append("nacionalidad = :nacionalidad")
            params['nacionalidad'] = filters['nacionalidad']
        
        if filters.get('semestre_min'):
            conditions.append("semestre >= :semestre_min")
            params['semestre_min'] = filters['semestre_min']
        
        if filters.get('semestre_max'):
            conditions.append("semestre <= :semestre_max")
            params['semestre_max'] = filters['semestre_max']
        
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
        
        base_query += " ORDER BY nombre_completo LIMIT 100"
        
        from sqlalchemy import text
        df = pd.read_sql(text(base_query), self.engine, params=params)
        return df.to_dict('records')

# Instancia global de datos del dashboard
dashboard_data = DashboardData(engine)

@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def api_stats():
    """API para estadísticas básicas"""
    stats = dashboard_data.get_basic_stats()
    return jsonify(stats)

@app.route('/api/nationality')
def api_nationality():
    """API para datos de nacionalidad"""
    data = dashboard_data.get_students_by_nationality()
    return jsonify(data)

@app.route('/api/programs')
def api_programs():
    """API para datos de programas"""
    data = dashboard_data.get_students_by_program()
    return jsonify(data)

@app.route('/api/performance')
def api_performance():
    """API para distribución de rendimiento"""
    data = dashboard_data.get_performance_distribution()
    return jsonify(data)

@app.route('/api/enrollment')
def api_enrollment():
    """API para tendencias de inscripción"""
    data = dashboard_data.get_enrollment_trends()
    return jsonify(data)

@app.route('/api/age')
def api_age():
    """API para distribución de edades"""
    data = dashboard_data.get_age_distribution()
    return jsonify(data)

@app.route('/api/search')
def api_search():
    """API para búsqueda de estudiantes"""
    filters = {
        'nombre': request.args.get('nombre'),
        'programa': request.args.get('programa'),
        'nacionalidad': request.args.get('nacionalidad'),
        'semestre_min': request.args.get('semestre_min'),
        'semestre_max': request.args.get('semestre_max')
    }
    
    # Filtrar valores None
    filters = {k: v for k, v in filters.items() if v}
    
    data = dashboard_data.search_students(filters)
    return jsonify(data)

@app.route('/api/filters')
def api_filters():
    """API para obtener opciones de filtros"""
    query_programs = "SELECT DISTINCT programa_academico FROM estudiantes_limpios ORDER BY programa_academico"
    query_nationalities = "SELECT DISTINCT nacionalidad FROM estudiantes_limpios ORDER BY nacionalidad"
    
    programs = pd.read_sql(query_programs, engine)['programa_academico'].tolist()
    nationalities = pd.read_sql(query_nationalities, engine)['nacionalidad'].tolist()
    
    return jsonify({
        'programas': programs,
        'nacionalidades': nationalities
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)