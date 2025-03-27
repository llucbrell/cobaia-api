import os
from flask import request, jsonify, render_template
from . import dynamic_logs
from flask_security import login_required, current_user
from ..models import Token, Endpoint, Role

@dynamic_logs.route('/logs/chat/<role>/<endpoint_url>', methods=['GET'])
@login_required  # Asegura que el usuario esté autenticado
def dynamic_chat_logs_route(role, endpoint_url):
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
    
    # Construir la ruta del archivo de log
    log_dir = os.path.join(os.getcwd(), 'user-logs', role)
    log_file_path = os.path.join(log_dir, f"{endpoint_url}.log")
    
    # Verificar si el archivo existe
    if not os.path.exists(log_file_path):
        return jsonify(message=f"Log file for {role}/{endpoint_url} not found"), 404
    
    # Leer el contenido del archivo con la codificación utf-8
    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_content = log_file.read()
    
    # Renderizar el HTML con el contenido del log en un textarea
    return render_template('log_viewer.html', log_content=log_content, role=role, endpoint_url=endpoint_url)
