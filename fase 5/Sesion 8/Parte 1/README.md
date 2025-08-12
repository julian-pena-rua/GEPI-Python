# Flask: Creando la primera aplicación simple

## Instalación

Para instalar Flask, usa el siguiente comando:

```bash
pip install Flask
```

## Introducción

Flask es un micro framework para Python basado en Werkzeug, Jinja 2 y buenas intenciones. Es una herramienta ligera y fácil de usar para crear aplicaciones web.

## Creando la primera aplicación Flask

Para crear una aplicación Flask simple, sigue estos pasos:

1. Importa la clase `Flask` desde el paquete `flask`.
2. Crea una instancia de la clase `Flask`. Esta instancia será nuestra aplicación WSGI.
3. Usa el decorador `@app.route()` para decirle a Flask qué URL debe activar la función asociada.
4. Define una función que devuelva el contenido que quieres mostrar en esa URL.
5. Ejecuta la aplicación usando el método `run()`.

### Ejemplo de código

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola, Mundo!'

if __name__ == '__main__':
    app.run()
```

Este código crea una aplicación web simple que muestra "¡Hola, Mundo!" cuando accedes a la raíz del servidor.

## Explicación

- `Flask(__name__)`: Crea una instancia de la aplicación Flask.
- `@app.route('/')`: Define la ruta para la URL raíz.
- `def hello_world()`: Función que devuelve el texto que se mostrará en la página.
- `app.run()`: Ejecuta la aplicación en el servidor local.

Este es un resumen básico para comenzar con Flask. Para más detalles, consulta la documentación oficial de Flask o el artículo original en [GeeksforGeeks](https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/).
