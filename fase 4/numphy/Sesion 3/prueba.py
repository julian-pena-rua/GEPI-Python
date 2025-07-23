import pandas as pd
import numpy as np
import os


# importar archivo csv
archivo = pd.read_csv('https://rplumber.ilo.org/data/indicator/?id=EAR_4HRL_SEX_AGE_CUR_NB_A&lang=es&type=label&format=.csv&channel=ilostat&title=ganancias-promedio-por-hora-de-los-asalariados-seg%C3%BAn-sexo-y-edad-anual')

# ver las primeras filas
print(archivo.head())

# imprime un mensaje y captura la palabra a buscar
palabra_a_buscar = input('¿Qué palabra quieres buscar? \nPalabra: ')

# Ver la palabra a buscar
print ('Buscando la palabra:', palabra_a_buscar)

# buscar una palabra en el archivo
# Esto mostrará todos los elementos que son iguales a palabra_a_buscar
print(archivo[archivo == palabra_a_buscar])

# ver las columnas sin eliminar contenido

# Busque filas que contengan la palabra clave "palabra_a_buscar" en la "columna_deseada" 
# y extraiga la información relevante

# ver las columnas
print("Mostrando las columnas del archivo")
print(archivo.columns)

# Captura la columna a buscar
columna_deseada = input(" ¿En qué columna deseas buscar la palabra? \nColumna: ")
print ('Buscando la palabra:', palabra_a_buscar, 'en la columna:', columna_deseada)

# Filtrar el archivo para mostrar solo las filas que contienen la palabra a buscar
filas_resultado = archivo[archivo[columna_deseada].str.contains(palabra_a_buscar,case=False)]

# Mostrar el resultado
print(filas_resultado)


#crea el archivo de salida
# Crear la carpeta de salida si no existe

#crear el archivo de salida
archivo_salida_txt    = open('numphy/Sesion 3/resultado/resultado.txt', 'x')
archivo_salida_csv    = open('numphy/Sesion 3/resultado/resultado.csv', 'x')
archivo_salida_excel  = open('numphy/Sesion 3/resultado/resultado.xlsx', 'x')

# Guardar el resultado en un nuevo archivo CSV  
filas_resultado.to_csv('numphy/Sesion 3/resultado/resultado.csv', index=False)
# Guardar el resultado en un nuevo archivo Excel
filas_resultado.to_excel('numphy/Sesion 3/resultado/resultado.xlsx', index=False)
# Guardar el resultado en un nuevo archivo Txt
filas_resultado.to_csv('numphy/Sesion 3/resultado/resultado.txt', index=False, sep='\t')