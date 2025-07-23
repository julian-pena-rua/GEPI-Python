import arrr
from pyscript import document


def traducir_ingles(event):
    input_text = document.querySelector("#ingles")
    english = input_text.value
    output_div = document.querySelector("#salida")
    output_div.innerText = arrr.translate(english)