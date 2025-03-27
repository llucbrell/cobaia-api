from flask import Blueprint, request, jsonify
from .models import Token
from . import db

main = Blueprint('main', __name__)


from flask import Blueprint, request, Response, json

main = Blueprint('main', __name__)

@main.route('/mirror/chat/', methods=['POST'])
def mirror_chat():
    data = request.json
    print(data)
    
    # Obtener el mensaje del usuario desde la estructura recibida
    user_message = data.get("messages", [{}])[0].get("text", "")
    
    print(user_message)
    
    # Formato correcto para Deep Chat
    response = {
                "text": "This is a response from a Flask server. Thank you for your message!",
                "type": "text"
            }

    # Serializar manualmente a JSON y devolver como Response
    response_json = json.dumps(response)
    return Response(response_json, mimetype='application/json')


@main.route('/api/protected')
def protected():
    token_value = request.headers.get('Authorization')
    
    # Imprimir el valor del token recibido
    print(f"Token recibido: {token_value}")
    
    token = Token.query.filter_by(token=token_value).first()
    
    # Verificar si el token es None
    if token is None:
        return jsonify(message="Invalid or missing token"), 401
    
    return jsonify(message=f"Access granted for token")