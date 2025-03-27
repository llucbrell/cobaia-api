from jinja2 import Environment, FileSystemLoader
import os

class SimplePrompt:
    def __init__(self, templates_dir=None, error_log_path="error_log.txt"):
        """
        Crea prompts simples y funcionales
        :param error_log_path: La ruta donde se guardarán los errores de validación.
        :param templates_dir: La ruta donde se encuentran los templates de prompt.
        """
        self.error_log_path = error_log_path
        self.total_text_num_tokens = 0
        self.kf_error = None
        # Obtener la ruta absoluta del directorio actual (donde está el script)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Establecer la ruta de los templates, si no se proporciona, usa la ruta por defecto
        if templates_dir is None:
            templates_dir = os.path.join(current_dir, '../templates/prompts')
 
        # Configurar Jinja2 para cargar los templates desde el directorio absoluto indicado
        self.env = Environment(loader=FileSystemLoader(templates_dir))
 
    def get_simple_prompt(self, schema, text, extra_prompt=None):
        """
        Devuelve el prompt usando parámetros de datos de entrada
        :param schema: El schema de json para construir el objeto
        :param text: El texto a formatear
        """
        kf_instruct_template = self.env.get_template('simple_instruct_template.txt')
        kf_prompt_instruct = kf_instruct_template.render({'schema': schema})
        prompt = f"{kf_prompt_instruct}\n{extra_prompt}\nThe user input data is down below:\n{text}",
        print("pormpt")
        print(prompt)
        return prompt

    def get_simple_image_prompt(self, schema, extra_prompt=None):
        """
        Devuelve el prompt usando parámetros de datos de entrada
        :param schema: El schema de json para construir el objeto
        :param text: El texto a formatear
        """
        kf_instruct_template = self.env.get_template('image_prompt_template.txt')
        kf_prompt_instruct = kf_instruct_template.render({'schema': schema})
        prompt = f"{kf_prompt_instruct}\n{extra_prompt}\n",
        print("pormpt")
        print(prompt)
        return prompt
 
        
class DynamicPrompt:
    def __init__(self, templates_dir=None ,error_log_path="error_log.txt"):
        """
        Crea prompts simples y funcionales para funcionar con la memoria dinámica de prompt
        :param error_log_path: La ruta donde se guardarán los errores de validación.
        """
        self.prompt = []
        self.error_log_path = error_log_path
        self.total_text_num_tokens = 0
        self.kf_error = None
        # Obtener la ruta absoluta del directorio actual (donde está el script)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Establecer la ruta de los templates, si no se proporciona, usa la ruta por defecto
        if templates_dir is None:
            templates_dir = os.path.join(current_dir, '../templates/prompts')
 
        # Configurar Jinja2 para cargar los templates desde el directorio absoluto indicado
        self.env = Environment(loader=FileSystemLoader(templates_dir))
 
    def add_message(self, content, role="user"):
        self.prompt.append({"role": role, "content": content})

    def get_initial_prompt(self, schema, text, extra_prompt=None):
        """
        Devuelve el prompt inicial usando parámetros de datos de entrada
        :param schema: El schema de json para construir el objeto
        :param text: El texto a formatear
        """
        kf_instruct_template = self.env.get_template('dynamic_init_template.txt')
        kf_prompt_instruct = kf_instruct_template.render({'schema': schema})

        prompt = f"{kf_prompt_instruct}\n{extra_prompt}\nThe user input data is down below:\n{text}",
        print("pormpt")
        print(prompt)
        return prompt

    def get_reptition_prompt(self, schema, json_object, text, extra_prompt=None):
        """
        Devuelve el prompt de repetición usando parámetros de datos de entrada
        :param schema: El schema de json para construir el objeto
        :param text: El texto a formatear"
        """
        kf_repeat_template = self.env.get_template('dynamic_repeat_template.txt')
        kf_prompt_instruct = kf_repeat_template.render({'schema': schema, "json_object": json_object})
        prompt = f"{kf_prompt_instruct}\n{extra_prompt}\nThe user input data is down below:\n{text}",
        print("pormpt")
        print(prompt)
        return prompt
