# Guía para Configurar las Bases de Datos MySQL y PostgreSQL con Docker

Esta guía explica paso a paso cómo crear y configurar las bases de datos MySQL y PostgreSQL necesarias para el proyecto, utilizando Docker. Está orientada a usuarios sin conocimientos previos de Docker.

---

## 1. Instalar Docker

Si aún no tienes Docker instalado, sigue estos pasos:

- Visita la página oficial: https://www.docker.com/get-started
- Descarga e instala Docker Desktop para tu sistema operativo (Windows, macOS, Linux).
- Abre una terminal o consola y ejecuta:
  ```
  docker --version
  ```
  para verificar que Docker está correctamente instalado.

---

## 2. Descargar las imágenes oficiales de MySQL y PostgreSQL

Abre una terminal y ejecuta los siguientes comandos para descargar las imágenes oficiales:

```bash
docker pull mysql:8.0
docker pull postgres:15
```

---

## 3. Ejecutar el contenedor de MySQL

Ejecuta el siguiente comando para iniciar un contenedor de MySQL con las variables de entorno necesarias (ajustadas según el archivo `.env` del proyecto):

```bash
docker run --name mysql-universidad -e MYSQL_ROOT_PASSWORD=tu_contrasena_mysql -e MYSQL_DATABASE=universidad -p 3306:3306 -d mysql:8.0
```

- `--name mysql-universidad`: nombre del contenedor.
- `-e MYSQL_ROOT_PASSWORD`: contraseña del usuario root.
- `-e MYSQL_DATABASE`: base de datos que se crea automáticamente.
- `-p 3306:3306`: mapea el puerto 3306 del contenedor al puerto 3306 de tu máquina.
- `-d`: ejecuta el contenedor en segundo plano.

---

## 4. Ejecutar el contenedor de PostgreSQL

Ejecuta el siguiente comando para iniciar un contenedor de PostgreSQL con las variables de entorno necesarias:

```bash
docker run --name postgres-universidad_dw -e POSTGRES_PASSWORD=tu_contrasena_postgres -e POSTGRES_DB=universidad_dw -p 5432:5432 -d postgres:15
```

- `--name postgres-universidad_dw`: nombre del contenedor.
- `-e POSTGRES_PASSWORD`: contraseña del usuario postgres.
- `-e POSTGRES_DB`: base de datos que se crea automáticamente.
- `-p 5432:5432`: mapea el puerto 5432 del contenedor al puerto 5432 de tu máquina.
- `-d`: ejecuta el contenedor en segundo plano.

---

## 5. Verificar que los contenedores están corriendo

Ejecuta:

```bash
docker ps
```

Deberías ver ambos contenedores `mysql-universidad` y `postgres-universidad_dw` en ejecución.

---

## 6. Conectarse a las bases de datos y crear tablas (opcional)

Puedes conectarte a las bases de datos usando clientes como MySQL Workbench, pgAdmin, o desde la terminal.

Para MySQL (desde la terminal):

```bash
docker exec -it mysql-universidad mysql -uroot -p
```

Luego ingresa la contraseña y ejecuta comandos SQL para crear tablas o verificar la base de datos.

Para PostgreSQL (desde la terminal):

```bash
docker exec -it postgres-universidad_dw psql -U postgres -d universidad_dw
```

Luego ejecuta comandos SQL para crear tablas o verificar la base de datos.

---

## 7. Detener y eliminar contenedores (cuando ya no se necesiten)

Para detener:

```bash
docker stop mysql-universidad
docker stop postgres-universidad_dw
```

Para eliminar:

```bash
docker rm mysql-universidad
docker rm postgres-universidad_dw
```

---

Esta guía cubre desde la instalación de Docker hasta la creación y manejo básico de las bases de datos MySQL y PostgreSQL necesarias para el proyecto, adaptándose a las variables de entorno definidas en el archivo `.env` del proyecto.

Con esta configuración, tu proyecto podrá conectarse a las bases de datos en los puertos locales 3306 (MySQL) y 5432 (PostgreSQL) respectivamente.
