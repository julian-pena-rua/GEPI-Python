# Flask: Agregar variables a tu aplicación web

En esta sección, aprenderás cómo agregar variables a tu aplicación Flask para mostrar contenido dinámico en tus páginas web.

## Uso de variables en las rutas

Puedes pasar variables en las rutas de Flask para capturar valores desde la URL y usarlos en tus funciones.

### Ejemplo

```python
from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    # Muestra el perfil del usuario
    return f'Perfil de usuario: {username}'

if __name__ == '__main__':
    app.run()
```

En este ejemplo, cuando accedes a `/user/John`, la página mostrará "Perfil de usuario: John".

## Tipos de variables

Flask permite especificar el tipo de variable para mayor control:

- `<string:variable_name>`: Cadena de texto (por defecto).
- `<int:variable_name>`: Entero.
- `<float:variable_name>`: Número decimal.
- `<path:variable_name>`: Ruta, acepta barras diagonales.

### Ejemplo con tipos

```python
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post número {post_id}'
```

## Uso de variables en plantillas

Para mostrar variables en HTML, puedes usar plantillas con Jinja2.

### Ejemplo básico

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
```

Y en el archivo `hello.html`:

```html
<!doctype html>
<html>
  <head><title>Saludo</title></head>
  <body>
    <h1>Hola, {{ name }}!</h1>
  </body>
</html>
```

## Conclusión

Agregar variables a tus rutas y plantillas te permite crear aplicaciones web dinámicas y personalizadas con Flask.

Para más detalles, consulta la documentación oficial de Flask o el artículo original en [GeeksforGeeks](https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/).
