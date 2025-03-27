from app.ia_tools.markdown_generator import MarkdownGenerator
from app.ia_tools.text_replacer import JSONReplacer
import json
from flatten_json import flatten



class MarkdownReporter:

    def __init__(self, text, endpoint, usage=None):
        # Crear una instancia del generador de Markdown
        self.md_gen = MarkdownGenerator(endpoint=endpoint)

        # Definir el encabezado e introducción
        self.md_gen.set_header(
            title="Report", 
            introduction="Automatically generated report, used to check model precision and help in handheld reviews."
        )
    
    def add_original_text(self, text):
        self.md_gen.add_markdown("#### Original Text\n")
        self.md_gen.add_markdown(f"{text}\n")
    
    def append(self, text):
        self.md_gen.add_markdown(f"{text}\n")


    def add_to_report(self, text, model_response, json_data=None, is_valid=None):
        # Aplana el diccionario para que todas las claves anidadas sean accesibles
        flattened_data = self.my_flatten_json_deep(json_data)

        # Verificar si el dato aplanado es un diccionario
        if isinstance(flattened_data, dict):
            # Itera sobre el diccionario aplanado
            for key, value in flattened_data.items():
                print(f"{key}: {value}")
        elif isinstance(flattened_data, list):
            # Si es una lista, maneja cada elemento
            for item in flattened_data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                else:
                    # Manejar otros tipos dentro de la lista si es necesario
                    print(f"List item: {item}")

        # Agregar Markdown estructurado para modelos
        self.md_gen.add_model("KeFHIR Model v1.0")

        # Agregar contenido dinámico adicional
        self.md_gen.add_markdown("\n### Results\n#### Extracted JSON 1\n")
        markdown_content = self.format_json_for_markdown(json_data)
        self.md_gen.add_markdown(f"`\n{markdown_content}\n`")

    def add_model_usage(self, usage):
        # No encontrado
        model_usage = usage
        self.md_gen.set_usage(usage_info=model_usage)

    def add_model_usage(self, usage):
        # No encontrado
        model_usage = usage
        self.md_gen.set_usage(usage_info=model_usage)



    def add_kf_config(self, configs):
        # No encontrado
        self.md_gen.set_config(config_details=configs)
        
    def add_kf_validation(self, validation):
        # No encontrado
        self.md_gen.add_validation(validation=validation)
    
    def mark_text_keys(self, text, json_array):
        print(text)
        # Crear la instancia del reemplazador
        replacer = JSONReplacer()

        # Reemplazar en el texto
        resultado = replacer.replace_in_text(text, json_array)
        print(resultado)

        # Agregar Markdown para los datos encontrados usando contenido dinámico
        self.md_gen.add_markdown("\n#### Data found in text\n")
        self.md_gen.add_markdown(f"{resultado}")

        # No encontrado
        not_found_objs = replacer.get_keywords_not_found()
        self.md_gen.add_decoupled_concepts(not_found_objs)
    
    def get_report(self):
        # Obtener el Markdown final como string
        markdown_string = self.md_gen.get_markdown()
        return markdown_string

    def my_flatten_json_deep(self, json_data):
        """
        Aplana recursivamente un JSON hasta que no queden listas ni diccionarios anidados.
        
        :param json_data: Estructura de datos JSON anidada (diccionarios, listas)
        :return: Diccionario aplanado con claves concatenadas
        """
        def is_flattened(data):
            """
            Verifica si el JSON está completamente aplanado.
            Devuelve True si no contiene listas ni diccionarios, False en caso contrario.
            """
            if isinstance(data, dict):
                for value in data.values():
                    if isinstance(value, (list, dict)):
                        return False
                return True
            return False  # Los tipos no diccionario se consideran no aplanados

        def recursive_flatten(data):
            """
            Función recursiva para aplanar datos, maneja diccionarios y listas.
            """
            if isinstance(data, list):
                # Manejar cada elemento de la lista individualmente si es necesario
                return [recursive_flatten(item) if isinstance(item, (dict, list)) else item for item in data]
            elif isinstance(data, dict):
                # Solo aplanar si es necesario
                if not is_flattened(data):
                    return recursive_flatten(flatten(data))
                return data
            return data  # Retorna primitivos sin cambio

        return recursive_flatten(json_data)


    def format_json_for_markdown(self, json_data):
        """
        Toma un diccionario JSON y lo convierte en una cadena formateada para insertar en Markdown.
        
        :param json_data: Diccionario JSON
        :return: Cadena de texto formateada para Markdown
        """
        # Convertir el diccionario JSON en una cadena JSON con indentación
        formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        
        # Envolver la cadena en un bloque de código para Markdown
        markdown_json = f"```json\n{formatted_json}\n```"
        
        return markdown_json
