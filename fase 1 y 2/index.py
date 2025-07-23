
print("Bienvenido a la tienda de comida")
comida      = input ("¿Qué deseas comprar?")
bebida      = input ("¿Qué deseas de bebida?")
print ("Digita ninguna o no si no deseas nada")
if comida == "no" and bebida == "no":
    print("Gracias por visitar nuestra tienda") 
elif comida != "no" and bebida != "no":
    print("Has comprado " + comida + " y " + bebida + ".")
if comida == "ninguna" and bebida == "ninguna":
    print("Gracias por visitar nuestra tienda") 

