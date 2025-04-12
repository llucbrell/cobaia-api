import requests
import json

def get_response_content(response_json):
    print("Response format")
    print(response_json)
    if 'choices' in response_json:
        print("LM Studio")
        # LM studio
        # Asumiendo que 'choices' es una lista de objetos y queremos extraer 'content' del objeto 'message'
        #choices = [choice['message']['content'] for choice in response_json['choices']]
        return response_json['choices'][0]['message']['content']
    elif 'textResponse' in response_json:
        # Anything LM
        print("Anything LM")
        return response_json['textResponse']
    elif 'response' in response_json:  # Ejemplo de un nuevo tipo de respuesta
        print("Ollama")
        return response_json['response']
    else:
        return 'Unknown response format ' + str(response_json)


def send_request(request_url, payload):
    try:
        response = requests.post(request_url, json=payload)
        response.raise_for_status()
        response_json = response.json()
        print("Response from LLM Server correct")
        #return get_response_content(response_json)
        return response_json
    except requests.exceptions.HTTPError as http_err:
        return f'HTTP error occurred: {http_err}\nResponse content: {response.content}'
    except Exception as err:
        print(err)
        return f'Other error occurred: {err}'


def build_payload( url, model_name ,processed_text, template_request_text):
     
    # Escapar el texto procesado como JSON
    #processed_text_json = json.dumps(processed_text)
    #processed_as_objs = json.loads(processed_text)
    print("PROCESSED")
    print(json.dumps(processed_text)[2:-1])
    processed_text_escaped = json.dumps(processed_text)[2:-2]

    # Asegurarse de que el texto JSON está doblemente escapado para ser insertado en otra cadena JSON
    print(processed_text)


    # Reemplazar {{url}}, {{api_key}} y {{prompt}} en la plantilla de solicitud
    template_request_text = template_request_text.replace('{{url}}', url).replace('{{prompt}}', processed_text_escaped).replace('{{model_name}}', model_name)


    print(template_request_text)
    # Convertir el texto JSON en un diccionario de Python
    template_dict = json.loads(template_request_text)

    payload = template_dict.get('payload', {})
    return payload


"""
   {
    "ur": "{url}}/chat",
    "payload": {
        "message": "{{prompt}}",
        "mode": "chat"
    },
    "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer {{api_key}}"
    }
} 
"""

#https://localhost:3001/api/v1/workspace/your_workspace_name_with_dashes_instead_of_spaces/chat 
#https://localhost:3001/api/v1/workspace/Long_Pdf_Test/chat

# http://localhost:3001/api/v1/workspace/Test
# http://localhost:3001/api/v1/auth
# KH2KRJ8-GAA4VQR-K6CR5QZ-JHM75PR
# http://localhost:3001/api/v1/workspace/Test
# http://localhost:3001/api/v1/auth
# KH2KRJ8-GAA4VQR-K6CR5QZ-JHM75PR