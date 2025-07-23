# Analisis de archivo CSV con Numpy

## Paso 1
Primero, se tiene que elegir un archivo el cual se va a analizar.
En nuestro caso se eligió "Ganancias medias por hora de los asalariados según sexo y edad" reporte generado por la OIT en de su enlace: 
https://ilostat.ilo.org/es/topics/wages/

[Acceso al archivo CSV](https://rplumber.ilo.org/data/indicator/?id=EAR_4HRL_SEX_AGE_CUR_NB_A&lang=es&type=label&format=.csv&channel=ilostat&title=ganancias-promedio-por-hora-de-los-asalariados-seg%C3%BAn-sexo-y-edad-anual)

## Paso 2
Segundo, debemos importar las bibliotecas necesarias: `numpy` y `pandas`. `numpy` nos permite realizar operaciones numéricas y
`pandas` nos permite trabajar con datos estructurados como los de un archivo CSV.

Lenguaje python
```
import numpy as np
import pandas as pd
```


## Paso 3
Tercero, debemos leer el archivo CSV utilizando `pd.read_csv()`. Esto nos permitirá trabajar con los datos del archivo.

Lenguaje python
```
# Leer el archivo CSV
archivo = pd.read_csv('ruta_archivo')
```

## Paso 4
Cuarto, debemos explorar los datos del archivo CSV utilizando `archivo.head()` esto nos permite ver los primeros registros del archivo.

Lenguaje python
```
# Ver los primeros datos del archivo CSV
print(archivo.head())
```

## Paso 5
Quinto, debemos realizar las operaciones que se desean realizar con los datos del archivo CSV.
En nuestro caso, se va a realizar un análisis de los datos del archivo CSV. Esto puede incluir la creación de gráficos, la realización de estadísticas, etc.

Lenguaje python
```
# Realizar operaciones con los datos del archivo CSV
# Por ejemplo, describe() muestra estadisticas descriptivas como la media, la desviacion estandar, el min, el max y los percentiles
archivo.describe()
```