# Libreria: Numpy
NumPy es una librería de Python especializada en el cálculo numérico y el análisis de datos, especialmente para un gran volumen de datos.

Incorpora una nueva clase de objetos llamados arrays que permite representar colecciones de datos de un mismo tipo en varias dimensiones, y funciones muy eficientes para su manipulación.

# Guia de instalación

## 1 Primero se instala numpy
(Si ya tienes Python y PIP instalado, este paso será muy sencillo)

Lenguaje batch, terminal
```
pip install numpy
```

NOTA: Si tienes problemas con la instalación, puedes usar un software que ya tenga una distribución de Python con PIP instalado, como Anaconda, Spyder, PyCharm, etc.

## 2 Uso de Numpy
En tu archivo de prueba .py, puedes importar numpy: 

Lenguaje python
```
import numpy
```

Ahora que numpy ha sido importado, lo puedes usar:

Lenguaje python
```
import numpy
arreglo = numpy.array([1, 2, 3, 4, 5])

print(arreglo)
```

## Notas sobre el uso de numpy:
- Los arrays de numpy pueden ser de cualquier tipo de dato (enteros, flotantes, booleanos, etc.) y pueden tener varias dimensiones.
- Los arrays de numpy pueden ser creados a partir de listas o tuplas de Python. Por ejemplo: numpy.array([1, 2, 3, 4, 5]) o numpy.array((1, 2, 3, 4, 5))
- Los arrays de numpy pueden ser indexados y recorridos de manera similar a las listas de Python.
- Los arrays de numpy tienen muchas funciones útiles para realizar operaciones matemáticas, estadísticas, etc.
- Numpy generalmente es utilizado con el alias "np" para evitar escribir "numpy" cada vez que se quiera usar una función o clase de numpy.
- Numpy tiene una gran cantidad de funciones y métodos, por lo que es recomendable revisar la documentación oficial de numpy para obtener más información sobre cómo usarlo.


