-- SQL file to create the data warehouse table in PostgreSQL

CREATE TABLE estudiantes_limpios (
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
