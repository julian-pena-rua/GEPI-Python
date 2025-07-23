# Proyecto Flask ETL - Guía de Uso

## 1. Configurar Variables de Entorno

Crea un archivo `.env` en el directorio `fase 5/flask/ejemplo`.  
Define las siguientes variables con las credenciales de tu base de datos y configuración:

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=universidad
DB_USER=root
DB_PASSWORD=tu_contrasena_mysql

DW_HOST=localhost
DW_PORT=5432
DW_NAME=universidad_dw
DW_USER=postgres
DW_PASSWORD=tu_contrasena_postgres

SECRET_KEY=tu_clave_secreta_flask
FLASK_ENV=development
```

> El archivo `config.py` utiliza estas variables para configurar las conexiones a las bases de datos y otros parámetros de la aplicación.

## 2. Instalación y Configuración de Bases de Datos con Docker (Opcional pero Recomendado)

Para facilitar la configuración de las bases de datos MySQL y PostgreSQL, puedes usar Docker siguiendo esta guía:

- Instala Docker desde https://www.docker.com/get-started
- Descarga las imágenes oficiales:
  ```
  docker pull mysql:8.0
  docker pull postgres:15
  ```
- Ejecuta los contenedores con las variables de entorno adecuadas:
  ```
  docker run --name mysql-universidad -e MYSQL_ROOT_PASSWORD=tu_contrasena_mysql -e MYSQL_DATABASE=universidad -p 3306:3306 -d mysql:8.0
  docker run --name postgres-universidad_dw -e POSTGRES_PASSWORD=tu_contrasena_postgres -e POSTGRES_DB=universidad_dw -p 5432:5432 -d postgres:15
  ```
- Verifica que los contenedores estén corriendo con:
  ```
  docker ps
  ```
- Para más detalles, consulta el archivo `README_data_DB.md` y `README_data_warehouse.md`.

## 3. Instalar Dependencias

Ejecuta el siguiente comando para instalar todos los paquetes de Python requeridos:

```
pip install -r 'fase 5/flask/ejemplo/requerimientos.txt'
```

## 4. Inicializar Directorios y bases de datos

Ejecuta el script `setup_university_and_datawarehouse.py` para crear las bases de datos y los directorios necesarios:

```
python 'fase 5/flask/ejemplo/setup_university_and_dw.py'
```

Luego, ejecuta el script del scheduler con la opción `--setup` para crear los directorios necesarios para logs, estáticos y plantillas:

```
python 'fase 5/flask/ejemplo/etl/scheduler.py' --setup
```

## 5. Ejecutar Proceso ETL Manualmente

Para ejecutar el proceso ETL una sola vez y cargar los datos en el data warehouse, ejecuta:

```
python 'fase 5/flask/ejemplo/etl/scheduler.py'
```

## 6. Programar Ejecución Automática del ETL

Para ejecutar el proceso ETL de forma programada (por defecto diariamente a las 2:00 AM), usa:

```
python 'fase 5/flask/ejemplo/etl/scheduler.py' --schedule
```

Para personalizar la hora de ejecución (por ejemplo, a las 02:00 AM):

```
python 'fase 5/flask/ejemplo/etl/scheduler.py' --schedule --time 02:00
```

Para ejecutar el ETL en intervalos regulares (por ejemplo, cada 6 horas):

```
python 'fase 5/flask/ejemplo/etl/scheduler.py' --schedule --interval 6
```

## 7. Ejecutar el Dashboard Flask

Inicia la aplicación Flask para servir el dashboard con:

```
python 'fase 5/flask/ejemplo/app.py'
```

Luego, accede al dashboard en tu navegador en la dirección:

```
http://localhost:5000/
```

### Endpoints API del Dashboard

La aplicación Flask expone varios endpoints API para obtener datos y estadísticas que se muestran en el dashboard:

- `/api/stats`: Estadísticas básicas (total estudiantes, programas, promedio general, nacionalidades).
- `/api/nationality`: Cantidad de estudiantes por nacionalidad (top 10).
- `/api/programs`: Cantidad y promedio por programa académico (top 15).
- `/api/performance`: Distribución de rendimiento académico por categorías.
- `/api/enrollment`: Tendencias de inscripción por año.
- `/api/age`: Distribución de edades en rangos.
- `/api/search`: Búsqueda de estudiantes con filtros (nombre, programa, nacionalidad, semestre).
- `/api/filters`: Opciones disponibles para filtros (programas y nacionalidades).

Estos endpoints permiten la interacción dinámica con el dashboard para visualizar y filtrar datos.

## 8. Verificar Logs

Los logs del proceso ETL y del scheduler se encuentran en la carpeta:

```
etl/logs/
```

Revisa estos archivos para monitorear la ejecución y detectar posibles errores.

---

Este proyecto utiliza las siguientes librerías principales:

- Flask para el servidor web y dashboard.
- Pandas y SQLAlchemy para manejo y consulta de datos.
- Plotly para visualización interactiva.
- Schedule para la programación de tareas ETL.
- python-dotenv para manejo de variables de entorno.

Asegúrate de tener configuradas correctamente las variables de entorno y las conexiones a las bases de datos para un funcionamiento adecuado.
