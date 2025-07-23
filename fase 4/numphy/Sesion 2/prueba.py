import numpy as np
import pandas as pd

# importar archivo csv
archivo = pd.read_csv('https://rplumber.ilo.org/data/indicator/?id=EAR_4HRL_SEX_AGE_CUR_NB_A&lang=es&type=label&format=.csv&channel=ilostat&title=ganancias-promedio-por-hora-de-los-asalariados-seg%C3%BAn-sexo-y-edad-anual')

# ver las primeras filas
print(archivo.head())

# ver las columnas
print(archivo.columns)

# describe() muestra estadisticas descriptivas como 
# la media, la desviacion estandar, el min, el max 
# y los percentiles
print(archivo.describe())

# ver el tipo de datos
print(archivo.dtypes)

# convertir el archivo a un arreglo de numpy
arreglo = np.array(archivo)

# Filtrar el arreglo para mostrar solo los elementos que son 'Colombia'
# Esto mostrará todos los elementos que son 'Colombia'
print(arreglo[(arreglo == 'Colombia')])

