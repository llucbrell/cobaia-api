import os

def extraer_texto_y_guardar(directorio_entrada, directorio_salida):
    """
    Extrae el texto de archivos .txt en un directorio y los guarda como archivos .txt en otro directorio.

    Args:
        directorio_entrada (str): La ruta del directorio de entrada.
        directorio_salida (str): La ruta del directorio de salida.
    """

    # Asegurarse de que el directorio de salida existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    # Recorrer todos los archivos en el directorio de entrada
    for nombre_archivo in os.listdir(directorio_entrada):
        ruta_archivo = os.path.join(directorio_entrada, nombre_archivo)

        # Verificar si es un archivo .txt
        if os.path.isfile(ruta_archivo) and nombre_archivo.endswith('.txt'):
            try:
                # Leer el texto del archivo .txt
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    texto = f.read()

                # Crear el nombre del archivo de salida
                nombre_archivo_salida = os.path.splitext(nombre_archivo)[0] + '.txt'
                ruta_archivo_salida = os.path.join(directorio_salida, nombre_archivo_salida)

                # Guardar el texto en un archivo .txt
                with open(ruta_archivo_salida, 'w', encoding='utf-8') as f:
                    f.write(texto)

                print(f"Texto extraído y guardado de {nombre_archivo} a {nombre_archivo_salida}")

            except Exception as e:
                print(f"Error al procesar {nombre_archivo}: {e}")

# Ejemplo de uso
directorio_entrada = 'D:/Desarrollo/IA/cobaia/test_scripts/doc_origins/soap_notes'  # Usar barras inclinadas
directorio_salida = 'D:/Desarrollo/IA/cobaia/test_scripts/doc_origins/soap_output_txt' # Usar barras inclinadas

extraer_texto_y_guardar(directorio_entrada, directorio_salida)