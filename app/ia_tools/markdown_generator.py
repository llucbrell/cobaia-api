import os
import json
from jinja2 import Environment, FileSystemLoader

class MarkdownGenerator:
    def __init__(self, endpoint, templates_dir=None):
        # Obtener la ruta absoluta del directorio actual (donde está el script)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Establecer la ruta de los templates, si no se proporciona, usa la ruta por defecto
        if templates_dir is None:
            templates_dir = os.path.join(current_dir, '../templates/markdown')
        schema_string = endpoint.schema  # Esto es un string JSON
        schema_dict = json.loads(schema_string)  # Convierte el string a un diccionario
        formatted_schema = json.dumps(schema_dict, indent=4, ensure_ascii=False)  # Aplica indentación
 
        # Configurar Jinja2 para cargar los templates desde el directorio absoluto indicado
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.header_data = {}
        self.usage = []
        self.kf_endpoint_info = {
            'endpoint_url': getattr(endpoint, 'endpoint_url', None),
            'target_url': getattr(endpoint, 'target_url', None),
            'model_name': getattr(endpoint, 'model_name', None),
            'context_window': getattr(endpoint, 'context_window', None),
            'additional_prompt': getattr(endpoint, 'additional_prompt', None),
            'request': getattr(endpoint, 'request', None)
        }
        
        self.kf_format_info = {
            'validation': None,
            'schema':  formatted_schema
        }
        self.configs = {}
        self.body_data = {
            'models': [],
            'usage': None,
            'config': None
        }
        self.decoupled_concepts_table = {
            'words_not_found': [],
        }

        self.additional_content = ""  # Aquí se acumulará el contenido añadido dinámicamente

    def set_header(self, title, introduction):
        """Configura los datos del encabezado para el markdown."""
        self.header_data['title'] = title
        self.header_data['introduction'] = introduction

    def add_model(self, model_name):
        """Añade un modelo a la lista de modelos en el cuerpo del markdown."""
        self.body_data['models'].append(model_name)

    def add_validation(self, validation):
        """Añade un modelo a la lista de modelos en el cuerpo del markdown."""
        self.kf_format_info['validation'] = validation
        print("VALIDATION")
        print(self.kf_format_info['validation'])
    

    def add_decoupled_concepts(self, words_not_found):
        """Añade una lista de palabras no encontradas en el texto con respecto al json"""
        print(words_not_found)
        for key, value in words_not_found.items():
            self.decoupled_concepts_table['words_not_found'].append({"key": key, "value": value})

    def set_usage(self, usage_info):
        """Establece la información de uso."""
        self.usage= usage_info

    def set_config(self, config_details):
        """Establece los detalles de configuración."""
        self.configs = config_details

    def add_markdown(self, markdown):
        """Añade markdown arbitrario al contenido adicional."""
        self.additional_content += markdown + "\n\n"

    def get_markdown(self):
        """Renderiza el markdown completo usando los datos acumulados."""
        # Renderizar el encabezado
        header_template = self.env.get_template('header_template.md')
        header_content = header_template.render(self.header_data)
        usage_template = self.env.get_template('model_usage.md')
        # Asegurarse de que self.usage no sea None, proporcionando un valor por defecto
        if self.usage and isinstance(self.usage, list):  # Verifica que self.usage sea una lista
            header_usage = usage_template.render(usage_list=self.usage)  # Pasar la lista a la plantilla


        kf_endpoint_template = self.env.get_template('endpoint_data.md')
        kf_endpoint = kf_endpoint_template.render(self.kf_endpoint_info)
        kf_configs_template = self.env.get_template('kf_run_config.md')
        kf_configs = kf_configs_template.render(self.configs)
        kf_info_template = self.env.get_template('kf_format_info.md')
        kf_format_info = kf_info_template.render(self.kf_format_info)

        # Renderizar el cuerpo estructurado con los modelos, uso y configuración
        body_template = self.env.get_template('body_template.md')
        body_content = body_template.render(self.body_data)
        decoupled_template = self.env.get_template('not_found_list.md')
        body_decoupled = decoupled_template.render(self.decoupled_concepts_table)

        # Devolver el markdown completo (encabezado + cuerpo + contenido adicional)
        return header_content  + self.additional_content + kf_format_info + body_content + body_decoupled + kf_configs + header_usage +  kf_endpoint


