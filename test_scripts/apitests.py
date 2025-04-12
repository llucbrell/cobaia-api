import os
import requests
import json

def testear_api(directorio_entrada, directorio_salida, token_acceso, url_api):
    """
    Testea una API enviando el texto de archivos .txt y guardando los informes en .md.

    Args:
        directorio_entrada (str): Ruta del directorio con los archivos .txt.
        directorio_salida (str): Ruta del directorio para guardar los informes .md.
        token_acceso (str): Token de acceso para la API.
        url_api (str): URL de la API.
    """

    # Asegurarse de que el directorio de salida existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    resultados_testeo = []

    # Recorrer los archivos .txt en el directorio de entrada
    for nombre_archivo in os.listdir(directorio_entrada):
        if nombre_archivo.endswith('.txt'):
            ruta_archivo = os.path.join(directorio_entrada, nombre_archivo)

            try:
                # Leer el contenido del archivo
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    texto = f.read()

                # Construir el cuerpo de la petición JSON
                payload = {
                    "messages": [{"text": texto}],
                    "validation": True,  # Habilitar la validación si es necesario
                    "reportMarkdown": True, # Habilitar la generación de markdown
                }

                # Enviar la solicitud a la API con datos JSON
                headers = {'Authorization': f'{token_acceso}', 'Content-Type': 'application/json'}
                respuesta = requests.post(url_api, headers=headers, data=json.dumps(payload))
                respuesta.raise_for_status()  # Lanza una excepción para códigos de error HTTP

                # Obtener el informe de la API
                api_response = respuesta.json()
                print(api_response)
                informe_api = api_response.get('kf_report', {}).get('md', '')

                # Guardar el informe en un archivo .md
                nombre_archivo_salida = os.path.splitext(nombre_archivo)[0] + '.md'
                ruta_archivo_salida = os.path.join(directorio_salida, nombre_archivo_salida)
                with open(ruta_archivo_salida, 'w', encoding='utf-8') as f:
                    f.write(informe_api)

                print(f"Informe guardado de {nombre_archivo} a {nombre_archivo_salida}")

                # Registrar el resultado del testeo
                resultados_testeo.append({
                    'archivo': nombre_archivo,
                    'estado': 'Éxito',
                    'mensaje': 'Informe guardado correctamente.'
                })

            except requests.exceptions.RequestException as e:
                print(f"Error al procesar {nombre_archivo}: {e}")
                resultados_testeo.append({
                    'archivo': nombre_archivo,
                    'estado': 'Error',
                    'mensaje': str(e)
                })
            except Exception as e:
                print(f"Error inesperado al procesar {nombre_archivo}: {e}")
                resultados_testeo.append({
                    'archivo': nombre_archivo,
                    'estado': 'Error',
                    'mensaje': str(e)
                })

    # Generar el informe de resultados del testeo
    generar_informe_resultados(resultados_testeo, directorio_salida)

def generar_informe_resultados(resultados_testeo, directorio_salida):
    """Genera un informe de resultados del testeo en formato .txt."""

    ruta_informe_resultados = os.path.join(directorio_salida, 'resultados_testeo.txt')
    with open(ruta_informe_resultados, 'w', encoding='utf-8') as f:
        f.write("Resultados del Testeo de la API\n\n")
        f.write("Archivo\tEstado\tMensaje\n")
        for resultado in resultados_testeo:
            f.write(f"{resultado['archivo']}\t{resultado['estado']}\t{resultado['mensaje']}\n")

    print(f"Informe de resultados generado en {ruta_informe_resultados}")

# Ejemplo de uso
directorio_entrada = 'D:/Desarrollo/IA/cobaia/test_scripts/doc_origins/soap_output_txt'  # Reemplaza con la ruta de tu directorio de entrada
directorio_salida = 'D:/Desarrollo/IA/cobaia/test_scripts/doc_output'    # Reemplaza con la ruta de tu directorio de salida
token_acceso = 'surpass'                    # Reemplaza con tu token de acceso
url_api = 'http://127.0.0.1:5000/api/surpass/patient'                # Reemplaza con la URL de tu API

testear_api(directorio_entrada, directorio_salida, token_acceso, url_api)