import pandas as pd

# define una serie de datos
munecos = {"Up": 420, "Barney": 380, "Rugrats": 390}

# imprime una tabla sin identificador, este es una serie
mivar = pd.Series(munecos)

print(mivar)

# para acceder a un valor de la serie, se usa el nombre del valor
mivar = pd.Series(munecos, index = ["Barney", "Rugrats"]) 
print(mivar)
# Los conjuntos de datos en Pandas son generalmente tablas multidimensionales, llamadas Data Frames
# Series es como una columna, un DataFrame es toda la tabla.

# Para crear un DataFrame, se necesitan dos series
data = {
  "nombres": ["Julian", "Santiago", "Luz"],
  "grupo": ["GEPI", "GEPI", "IUSH" ]
}

mivar = pd.DataFrame(data)

print(mivar)


