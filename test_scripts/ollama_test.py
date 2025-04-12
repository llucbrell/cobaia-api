import requests
import json

# --- Inicio de la Modificación ---

# Define el host de Ollama explícitamente
OLLAMA_HOST = 'http://127.0.0.1:11434'
OLLAMA_CHAT_API_URL = f'{OLLAMA_HOST}/api/chat'

# Define la configuración para deshabilitar los proxies para este cliente
# Le decimos que para los protocolos http y https, no use ningún proxy ('None')
DISABLED_PROXY_CONFIG = {
    'http://': None,
    'https://': None,
}

# --- Fin de la Modificación ---

# Initializing an empty list for storing the chat messages and setting up the initial system message
chat_messages = []
system_message = 'You are a helpful assistant.'

# Defining a function to create new messages with specified roles ('user' or 'assistant')
def create_message(message, role):
    return {
        'role': role,
        'content': message
    }

# Starting the main conversation loop
def chat():
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': 'gemma3:1b',
        'stream': True,
        'messages': chat_messages
    }

    try:
        response = requests.post(OLLAMA_CHAT_API_URL, headers=headers, json=data, stream=True, proxies=DISABLED_PROXY_CONFIG)
        response.raise_for_status()  # Raise an exception for bad status codes

        assistant_message = ''
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line.decode('utf-8'))
                    if 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        assistant_message += content
                        print(content, end='', flush=True)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON chunk: {line}")

        # Adding the finalized assistant message to the chat log
        chat_messages.append(create_message(assistant_message, 'assistant'))

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama API: {e}")

# Function for asking questions - appending user messages to the chat logs before starting the `chat()` function
def ask(message):
    # Opcional: Añadir mensaje de sistema si no existe ya
    # if not any(msg['role'] == 'system' for msg in chat_messages):
    #     chat_messages.insert(0, create_message(system_message, 'system'))

    chat_messages.append(
        create_message(message, 'user')
    )
    print(f'\n\n--{message}--\n\n')
    chat()

# Sending two example requests using the defined `ask()` function
ask('Lista los nombres de 10 personajes más importantes del tebeo de mortadelo y filemón')
# ask('How many of the cities listed are in South America?')