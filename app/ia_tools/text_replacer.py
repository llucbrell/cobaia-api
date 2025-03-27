from flatten_json import flatten
from flashtext import KeywordProcessor

class JSONReplacer:
    def __init__(self, threshold=80):
        self.keyword_processor = KeywordProcessor(case_sensitive=False)
        self.keywords_not_found = {}
        self.threshold = threshold  # Umbral de coincidencia aproximada
        self.all_keywords = []  # Mantiene todas las palabras clave agregadas

    def process_jsons(self, json_array):
        """
        Procesa un array de JSONs aplanados.
        Añade cada valor del JSON como palabra clave y lo reemplaza por su formato en markdown.
        """
        valores_omitidos = {"None", "null", "none", "Null", "undefined", "Undefined", None}
        self.keyword_processor = KeywordProcessor(case_sensitive=False)
        self.keywords_not_found = {}
        self.all_keywords = []

        for json_obj in json_array:
            flattened_json = self.flatten_json_data(json_obj)
            if isinstance(flattened_json, list):  # Si el resultado es una lista
                for item in flattened_json:
                    self.add_keywords(item)
            else:
                self.add_keywords(flattened_json)

    def add_keywords(self, flattened_json):
        """
        Añade palabras clave y formatea los valores para markdown.
        """
        valores_omitidos = {"None", "null", "none", "Null", "undefined", "Undefined", None}
        for key, value in flattened_json.items():
            if value in valores_omitidos or not value:
                self.keywords_not_found[key] = value
            else:
                if not isinstance(value, str):
                    value = str(value)
                formatted_value = f"**{value} (key={key})**"
                self.keyword_processor.add_keyword(value, formatted_value)
                self.all_keywords.append((value, key))

    def replace_in_text(self, text, json_array):
        """
        Reemplaza en el texto todos los valores de los JSONs proporcionados por su formato en markdown.
        """
        self.process_jsons(json_array)
        
        # Reemplazar las palabras clave en el texto
        processed_text = self.keyword_processor.replace_keywords(text)

        # Verificar si alguna palabra clave no fue reemplazada
        for value, key in self.all_keywords:
            if value not in processed_text:
                self.keywords_not_found[key] = value  # Añadir a la lista de no encontradas
        
        return processed_text

    def get_keywords_not_found(self):
        """
        Devuelve un diccionario con los elementos del JSON que no se encontraron en el texto.
        """
        return self.keywords_not_found

    def is_flattened(self, json_data):
        """
        Verifica si el JSON está completamente aplanado.
        Un JSON está completamente aplanado si todos los valores son primitivos (no listas ni diccionarios).
        """
        if isinstance(json_data, dict):
            return all(not isinstance(value, (dict, list)) for value in json_data.values())
        return True  # Los tipos primitivos se consideran aplanados

    def flatten_json_data(self, json_data):
        """
        Aplana el JSON si no está aplanado.
        Maneja listas, diccionarios y otros tipos de datos de forma apropiada.
        """
        if isinstance(json_data, dict):
            if not self.is_flattened(json_data):
                return flatten(json_data)  # Solo aplana si es necesario y si es un diccionario
            return json_data
        elif isinstance(json_data, list):
            # Si es una lista, aplane cada elemento que sea un diccionario
            return [self.flatten_json_data(item) if isinstance(item, dict) else item for item in json_data]
        return json_data  # Si no es un diccionario ni una lista, devolver sin cambios
