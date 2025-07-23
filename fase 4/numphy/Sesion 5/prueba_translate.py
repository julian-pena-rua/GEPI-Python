s = 'Albañil Japonés Árabe Javier Peña AfGanIsTáN México Méxicoño Méxicoña Méxicoñoña Méxicoñoñas Méxicoñoñita'

print(str.lower(s.translate(str.maketrans({
    'ñ': 'n', 
    'é': 'e', 
    'á': 'a', 
    'í': 'i', 
    'ó': 'o',
    'ü': 'u',
    'ç': 'c',
    'Á': 'A',
    'É': 'E',
    'Í': 'I',
    'Ó': 'O',
    'Ü': 'U',
    'Ñ': 'N',
    ' ': ' '
    }))))
