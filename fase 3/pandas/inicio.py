# funciones para analizar, limpiar, explorar, y manipular datos.

# Pandas nos permite analizar grandes cantidades de datos y sacar conclusiones basadas en ellos.

# pandas nos permite limpiar conjuntos de datos desorganizados y hacerlos legibles y relevantes

# Los datos relevantes son muy importantes en la ciencia de datos.

# Repositorio github https://github.com/pandas-dev/pandas

import pandas

miset = {
  'carros': ["BMW", "Volvo", "Ford"],
  'pasajeros': [3, 7, 2]
}

# Crear una tabla
mivar = pandas.DataFrame(miset)

print(mivar)

# Visualizar versión
print(pandas.__version__)