def clear_characters(text: str) -> str:
        """Reemplaza caracteres acentuados por sus equivalentes sin acento"""
        if text is None or text == '':
            return ''

        # Usar translate para reemplazar caracteres específicos
        # Este método es más eficiente y directo para reemplazar múltiples caracteres
        #text = unidecode(text)  # Elimina acentos y convierte a ASCII


        clean_text = str(text).translate(str.maketrans({
            'á': 'a',
            'é': 'e',
            'í': 'i',
            'ó': 'o',
            'ú': 'u',
            'ü': 'u',
            'ä': 'a',
            'ë': 'e',
            'ï': 'i',
            'ö': 'o',
            'ÿ': 'y',
            'à': 'a',
            'è': 'e',
            'ì': 'i',
            'ò': 'o',
            'ù': 'u',
            'â': 'a',
            'ê': 'e',
            'î': 'i',
            'ô': 'o',
            'û': 'u',
            'ã': 'a',
            'õ': 'o',
            'ñ': 'n',
            'ç': 'c',
            'Á': 'A',
            'É': 'E',
            'Í': 'I',
            'Ó': 'O',
            'Ú': 'U',
            'Ü': 'U',
            'Ñ': 'N',
            'Ä': 'A',
            'Ë': 'E',
            'Ï': 'I',
            'Ö': 'O',
            'Ÿ': 'Y',
            'À': 'A',
            'È': 'E',
            'Ì': 'I',
            'Ò': 'O',
            'Ù': 'U',
            'Â': 'A',
            'Ê': 'E',
            'Î': 'I',
            'Ô': 'O',
            'Û': 'U',
            'Ã': 'A',
            'Õ': 'O',
            ' ': ' ',  # Espacio se mantiene igual
            '  ': ' ',  # Doble espacio se reemplaza por un solo espacio
            # Espacio se mantiene igual
        }))

        # Convertir a string y limpiar espacios
        clean_text = str(clean_text).strip()
        
        # Normalizar a minúsculas
        clean_text = clean_text.lower()
        
        # Capitalizar primera letra de cada palabra
        clean_text = clean_text.title()
        
        return clean_text


s = 'Albañil Japonés Árabe Javier Peña AfGanIsTáN México Méxicoño Méxicoña Méxicoñoña Méxicoñoñas Méxicoñoñita'
print(clear_characters(s))