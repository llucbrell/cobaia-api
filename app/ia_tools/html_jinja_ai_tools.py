from jinja2 import Environment, FileSystemLoader
import os

class JinjaHtmlTools:
    def __init__(self, templates_dir='app/templates/jinja_tools'):
        # Inicializa el entorno de Jinja2 con el directorio de plantillas
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        # Imprimir el directorio desde el que busca
        print(f"Directorio de trabajo actual: {os.getcwd()}")
        print(f"Buscando plantillas en el directorio: {self.env.loader.searchpath[0]}")
    
    def render(self, template_name, **context):
        """Renderiza una plantilla dada con el contexto proporcionado."""
        # Imprimir la ruta completa de la plantilla
        template_path = os.path.join(self.env.loader.searchpath[0], template_name)
        print(f"Buscando plantilla en: {template_path}")
        
        # Cargar y renderizar la plantilla
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def render_error(self, heading=None, message=None):
        """Renderiza una plantilla de error con parámetros opcionales."""
        # Usa una ruta relativa, no absoluta
        return self.render('error.html', title="Error", heading=heading, message=message)
    
    def render_video(self, title, video_url, description, duration):
        """Renderiza una plantilla de video."""
        return self.render('video_template.html', title=title, video_url=video_url, description=description, duration=duration)
