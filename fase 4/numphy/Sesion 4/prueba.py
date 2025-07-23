# pide que creamos un programa que nos permita reemplazar 
# caracteres como acentos, tildes, etc. en una cadena de texto.
# Para ello, se nos proporciona una función llamada `reemplazar_caracteres` 
# que toma una cadena de texto como entrada y devuelve la cadena con los caracteres
# reemplazados.

# se importan las librerias necesarias
import pandas as pd
import numpy as np


# se define la función que reemplaza caracteres especiales
def reemplazar_caracteres(texto):
    # Definimos un diccionario de reemplazos
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ñ': 'n',
        'ü': 'u'
    }
    
    # Reemplazamos los caracteres especiales en el texto
    for caracter, reemplazo in reemplazos.items():
        texto = texto.replace(caracter, reemplazo)
    
    return texto

# se importan los datos CSV
datos = pd.read_csv('https://rplumber.ilo.org/data/indicator/?id=EAR_4HRL_SEX_AGE_CUR_NB_A&lang=es&type=label&format=.csv&channel=ilostat&title=ganancias-promedio-por-hora-de-los-asalariados-seg%C3%BAn-sexo-y-edad-anual')

# filtro por algún valor que tenga acentos o caracteres especiales
columna_deseada = 'ref_area.label'
palabra_a_buscar = 'AfGanIsTáN'

filas_resultado = datos[datos[columna_deseada].str.contains(palabra_a_buscar,case=False)]

# Sustituir una subcadena de un string con replace()
# El método replace(sub, nuevo) de la clase string 
# devuelve una copia del string con todas las 
# ocurrencias del substring sub reemplazadas por 
# el substring nuevo.

palabra_sustitucion = 'Albania'
#nuevas_filas = filas_resultado[columna_deseada].replace(palabra_a_buscar, palabra_sustitucion)
"""
    Lowercases all string values in a Pandas DataFrame, 
    handling mixed data types and missing values.
"""
nuevas_filas = filas_resultado.applymap(lambda x: x.lower() if isinstance(x, str) else x).replace(palabra_a_buscar.lower(), palabra_sustitucion)

# Mostrar las filas originales y las filas con el reemplazo
print("Filas originales:")
print(filas_resultado)
print("\nFilas con reemplazo:")
print(nuevas_filas)
