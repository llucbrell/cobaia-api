from tokenizers import Tokenizer
import json

class TokenizerWrapper:
    def __init__(self, model_name="distilbert-base-uncased", error_log_path="kefhir-logs/error_log.txt"):
        """
        Inicializa el tokenizador con un modelo preentrenado y establece la ruta del archivo de log de errores.
        :param model_name: El nombre del modelo preentrenado a utilizar (por defecto: distilbert-base-uncased).
        :param error_log_path: La ruta donde se guardarán los errores.
        """
        self.model_name = model_name
        self.error_log_path = error_log_path
        self.tokenizer = None

        try:
            # Intentar cargar el tokenizador preentrenado
            self.tokenizer = Tokenizer.from_pretrained(self.model_name)
        except Exception as e:
            self.log_error(f"Error al cargar el tokenizador para el modelo '{self.model_name}': {str(e)}")

    def tokenize(self, text):
        """
        Tokeniza un texto dado, conviertiendo el contenido a cadena si es necesario.
        Maneja errores si ocurren.
        :param text: El texto, JSON, lista, número, etc. que se desea tokenizar.
        :return: Lista de tokens o None si ocurre un error.
        """
        if not self.tokenizer:
            self.log_error("Error: Tokenizador no cargado correctamente.")
            return None

        try:
            # Convertir todo el input a una cadena de texto
            if isinstance(text, (dict, list, set)):
                text = json.dumps(text)  # Convertir a JSON si es una lista, dict o set
            elif not isinstance(text, str):
                text = str(text)  # Convertir números u otros tipos a cadena

            # Realizar la tokenización
            encoding = self.tokenizer.encode(text)
            tokens = encoding.tokens
            return tokens
        except Exception as e:
            self.log_error(f"Error durante la tokenización del texto: {str(e)}")
            return None

    def log_error(self, message):
        """
        Registra un mensaje de error en el archivo de log especificado.
        :param message: El mensaje de error a registrar.
        """
        with open(self.error_log_path, "a") as log_file:
            log_file.write(message + "\n")

    def count_tokens(self, tokens):
        """
        Cuenta el número de tokens en una lista de tokens dada.
        :param tokens: La lista de tokens.
        :return: Número de tokens o None si ocurre un error.
        """
        if isinstance(tokens, list):
            return len(tokens)
        else:
            self.log_error("Error: Los tokens no son una lista.")
            return None
