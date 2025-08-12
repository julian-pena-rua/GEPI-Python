# Flask: Métodos del protocolo HTTP (GET, PUT, DELETE, HEAD)

En esta sección, aprenderás cómo manejar diferentes métodos HTTP en Flask para crear aplicaciones web más completas y funcionales.

## Métodos HTTP en Flask

Flask permite definir rutas que respondan a diferentes métodos HTTP, como GET, POST, PUT, DELETE, HEAD, entre otros.

### Manejo de métodos HTTP

Para especificar qué métodos acepta una ruta, usa el parámetro `methods` en el decorador `@app.route()`.

### Ejemplo con varios métodos

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/resource', methods=['GET', 'PUT', 'DELETE', 'HEAD'])
def resource():
    if request.method == 'GET':
        return 'Solicitud GET recibida'
    elif request.method == 'PUT':
        return 'Solicitud PUT recibida'
    elif request.method == 'DELETE':
        return 'Solicitud DELETE recibida'
    elif request.method == 'HEAD':
        return '', 200

if __name__ == '__main__':
    app.run()
```

En este ejemplo, la función `resource` maneja diferentes métodos HTTP y responde según el tipo de solicitud.

## Explicación de los métodos

- **GET**: Solicita datos del servidor.
- **PUT**: Envía datos para actualizar un recurso existente.
- **DELETE**: Elimina un recurso.
- **HEAD**: Similar a GET, pero solo solicita los encabezados de la respuesta.

## Conclusión

Manejar diferentes métodos HTTP te permite crear APIs RESTful y aplicaciones web más robustas con Flask.

Para más detalles, consulta la documentación oficial de Flask o el artículo original en [GeeksforGeeks](https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/).
