from flask import request, jsonify, render_template
from . import dynamic_chat
from flask_security import login_required, current_user
from ..models import Token, Endpoint, Role

@dynamic_chat.route('/chat/<role>/<endpoint_url>', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado
def dynamic_chat_route(role, endpoint_url):
    # Buscar el rol correspondiente al valor recibido en la URL
    role_obj = Role.query.filter_by(name=role).first()
    
    if role_obj is None:
        return jsonify(message=f"Role '{role}' not found"), 404
    
    # Verificar si el usuario actual tiene acceso al rol
    if role_obj not in current_user.roles:
        return jsonify(message="Access denied"), 403
    
    # Verificar si existe el endpoint con el rol y el endpoint_url dados
    endpoint = Endpoint.query.filter_by(role_id=role_obj.id, endpoint_url=endpoint_url).first()
    if endpoint is None:
        return jsonify(message=f"Endpoint '{endpoint_url}' not found"), 404

    # Buscar el token asociado con el rol
    token_obj = Token.query.filter_by(role_id=role_obj.id).first()
    print(token_obj)
    if token_obj is None:
        return jsonify(message=f"No token found for role '{role}'"), 404
    
    
    # Renderizar el template y pasar el endpoint dinámico
    api_endpoint = f"/api/{role}/{endpoint_url}"
    return render_template('chatbot.html',  endpoint=endpoint, role=role, endpoint_url=endpoint_url, token=token_obj.token)
