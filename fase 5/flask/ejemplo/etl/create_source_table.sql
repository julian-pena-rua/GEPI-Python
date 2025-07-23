-- Drops the table if it exists and creates a new one

DROP TABLE IF EXISTS estudiantes;

-- SQL script to create the source table 'estudiantes' in MySQL database 'universidad'

CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento VARCHAR(100),
    nacionalidad VARCHAR(50),
    programa_academico VARCHAR(100),
    semestre INT,
    promedio DECIMAL(3,2),
    estado VARCHAR(20),
    fecha_ingreso VARCHAR(100),
    ciudad_origen VARCHAR(100)
);
