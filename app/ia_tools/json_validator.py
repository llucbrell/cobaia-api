import jsonschema
from jsonschema import validate
import json

class JSONValidator:
    def __init__(self, error_log_path="error_log.txt"):
        """
        Inicializa el validador JSON y establece la ruta del archivo de log de errores.
        :param error_log_path: La ruta donde se guardarán los errores de validación.
        """
        self.error_log_path = error_log_path

    def validate_json(self, json_data, schema):
        """
        Valida un JSON contra un esquema proporcionado.
        :param json_data: El documento JSON a validar.
        :param schema: El esquema JSON que define la estructura esperada.
        :return: True si el JSON es válido, False si es inválido.
        """
        try:
            print(schema)
            print(json_data)
            validate(instance=json_data, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            self.log_error(f"Error de validación: {e.message}")
            self.info = f"{e.message}"
            return False
        except jsonschema.exceptions.SchemaError as e:
            self.log_error(f"Error en el esquema proporcionado: {e.message}")
            self.error = f"Error in the provided schema: {e.message}"
            return False

    def log_error(self, message):
        """
        Registra un mensaje de error en el archivo de log especificado.
        :param message: El mensaje de error a registrar.
        """
        with open(self.error_log_path, "a") as log_file:
            log_file.write(message + "\n")

    def get_errors(self):
        return self.error

    def get_info(self):
        return self.info
