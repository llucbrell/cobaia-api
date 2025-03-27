import requests
import json
import sys
from datetime import date
import time
from app.ia_tools.send_request import *


class ModelCommunication:
    def __init__(self, endpoint ,error_log_path="error_log.txt"):
        """
        Prepara el endpoint para comunicar con el modelo
        :param error_log_path: La ruta donde se guardarán los errores de validación.
        :target_url: La ruta donde se envía el prompt
        :str_chema: El schema que se le pasa al modelo
        """
        
        self.error_log_path = error_log_path
        self.target_url = endpoint.target_url
        self.str_schema = endpoint.schema
        self.payload = endpoint.request
        self.model_name = endpoint.model_name
        self.usage = {}
        self.response_time = 0

    def get_usage(self):
        return self.usage

    def get_response_time(self):
        return self.response_time

    def send_to_model(self, prompt):
        """
        Envía un prompt al endpoint de chat
        :prompt: string de entrada al modelo 
        :return: string de salida del modelo
        """
        default_request_payload ={
            "model": f"{self.model_name}",
            #"messages":[
            #    {"role": "user", "content": f"You are a helpful AI assistant. The user will enter some data in any format or way, it even could be disorderd an you will reorder the data and set it due to the schema privided. Output in JSON using the schema defined here {schema}"},
            #    {"role": "user", "content": country}
            #],
            "format": "json",
            "options": {
                "temperature": 0.0
            },
            "stream": False
        }
        if self.payload:
            print("Sending with custom payload")
            print(self.model_name)
            self.payload = build_payload(url=self.target_url, model_name=self.model_name, processed_text=prompt, template_request_text=self.payload)

        else:
            print("sending with default payload")
            self.payload = default_request_payload
            self.payload["model"] = self.model_name
            self.payload["messages"] = prompt

        # Registrar el tiempo antes de enviar la solicitud
        start_time = time.time()
        response = requests.post(f"{self.target_url}", json=self.payload)
        # Registrar el tiempo después de recibir la respuesta
        end_time = time.time()

        # Calcular el tiempo de respuesta en segundos
        self.response_time = end_time - start_time
        

         # Intenta interpretar la respuesta como JSON
        model_response = {
            "status": "inactive"
        }
        try:
            response_json = response.json()
            print("Response JSON:", json.dumps(response_json, indent=2))  # Imprime el JSON formateado
            if response_json.get("error") != None:
                model_response["status"] = "error"
                model_response["message"] = response_json["error"]
                return model_response
        except json.JSONDecodeError:
            # Si no es JSON, imprime el texto crudo
            print("Response text:", response.text)

        # Extraer el contenido del primer choice en el JSON de la respuesta
        if "choices" in response_json:
            model_response["message"] = response_json["choices"][0]["message"]["content"]
        
        if "usage" in response_json:
            self.usage = response_json["usage"]
            # Obtener la fecha de hoy
            hoy = date.today()
            self.usage["date"] = hoy
    
        if "usage" in response_json and "model" in response_json:
            self.usage["model_id_name"] = response_json["model"]
        
#        for message in response.iter_lines():
#            print(message)
#            jsonstr = json.loads(message)
            #print(jsonstr)
            #print(jsonstr["message"]["content"], end="")
#            model_response["message"] += jsonstr["message"]["content"]

        if model_response["status"] == "inactive":
            model_response["status"] = "success"
        return model_response