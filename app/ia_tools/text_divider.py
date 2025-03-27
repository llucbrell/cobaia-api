import re


class TextDivider:
    def __init__(self, error_log_path="error_log.txt"):
        print("initiated")

    def token_slice(self, texto, max_tokens, offset, tokenizer_name="bert-base-uncased"):
        # Verificar si el texto es una cadena y no está vacío
        print("MAX TOKNS")
        print(max_tokens)
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("El texto proporcionado debe ser una cadena no vacía.")
        
        # Definimos una expresión regular para dividir el texto en oraciones usando delimitadores jerárquicos
        delimitadores = r'(?<=[\.\:\;\n,])\s+'
        
        # Dividimos el texto según los delimitadores definidos
        oraciones = re.split(delimitadores, texto)
        
        # Inicializamos variables para almacenar los fragmentos
        partes = []
        fragmento_actual = []
        token_count = 0
        
        # Iteramos sobre las oraciones
        for oracion in oraciones:
            tokens_oracion = oracion.split()
            num_tokens_oracion = len(tokens_oracion)
            
            # Si agregar la oración actual excede el número máximo de tokens, cerramos el fragmento actual
            if token_count + num_tokens_oracion > max_tokens:
                partes.append(" ".join(fragmento_actual))
                
                # Calculamos el solapamiento
                solapamiento_tokens = int(len(fragmento_actual) * offset)
                
                # Iniciamos el siguiente fragmento con el solapamiento
                fragmento_actual = fragmento_actual[-solapamiento_tokens:]
                token_count = len(fragmento_actual)
            
            # Añadimos la oración actual al fragmento
            fragmento_actual.extend(tokens_oracion)
            token_count += num_tokens_oracion
        
        # Agregar el último fragmento si hay contenido
        if fragmento_actual:
            partes.append(" ".join(fragmento_actual))
        
        return partes

    