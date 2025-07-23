# Ejemplo de uso de replace para reemplazar palabras en una cadena
# STRING DE EJEMPLO
s = 'one two one two one'

###############################
# PRACTICA 1    
sub = s.replace('one', 'uno')
sub2 = sub.replace('two', '', 1)  # Reemplaza solo la primera ocurrencia de '  ' por un espacio simple
print("Practica 1: ",sub2.replace('  ', ' '))

#################################
# PRACTICA 2
print("Practica 2: ",s.replace('one', 'uno').replace('two', '', 1).replace('  ', ' '))

#################################
# PRACTICA 3
# evitar uso anidado de replace por conflicto de reemplazos sin 
# tener que usar una variable temporal
print("Practica 3 incorrecto: ",s.replace('one', 'two').replace('two','one')) 

# uso de variable temporal
# para evitar conflicto de reemplazos
# uso de temporal al inicio de la cadena y final de la cadena
print("Practica 3 correcto: ", s.replace('one', 'temp').replace('two', 'one').replace('temp', 'two'))