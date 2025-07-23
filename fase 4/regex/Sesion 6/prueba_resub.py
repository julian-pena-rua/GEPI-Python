import re

s = 'aaa@xxx.com bbb@yyy.net ccc@zzz.org'

# el primer argumento es el patrón de expresión regular, 
# el segundo es la cadena de reemplazo y 
# el tercero es la cadena de destino.

print(re.sub('[a-z]+@', 'ABC@', s))
# ABC@xxx.com ABC@yyy.net ABC@zzz.org