import os
import json
from flask import request, jsonify, Response
from . import dynamic_api_logs
from ..models import Token, Endpoint, Role

@dynamic_api_logs.route('/logs/api/<role>/<endpoint_url>', methods=['GET'])
def dynamic_api_logs_route(role, endpoint_url):
   # Obtener el token desde el encabezado de la solicitud
    token_value = request.headers.get('Authorization')
    print(f"Token recibido: {token_value}")
    
    # Verificar si el token está presente en la base de datos
    token = Token.query.filter_by(token=token_value).first()
    
    if token is None:
        print("Token no encontrado o inválido.")
        return jsonify(message="Invalid or missing token"), 401
    
    print(f"Token válido encontrado: {token.token}")
    
    # Buscar el rol correspondiente al valor recibido en la URL
    role_obj = Role.query.filter_by(name=role).first()
    
    if role_obj is None:
        print(f"Rol '{role}' no encontrado.")
        return jsonify(message=f"Role '{role}' not found"), 404
    
    print(f"Rol encontrado: {role_obj.name}")
    
    # Verificar si el token tiene acceso al rol
    if token.role_id != role_obj.id:
        print(f"Acceso denegado al rol '{role_obj.name}' para el token.")
        return jsonify(message="Access denied"), 403
    
    print(f"Acceso concedido al rol '{role_obj.name}' para el token.")
    
    # Verificar si existe el endpoint con el rol y el endpoint_url dados
    endpoint = Endpoint.query.filter_by(role_id=role_obj.id, endpoint_url=endpoint_url).first()
    
    if endpoint is None:
        print(f"Endpoint '{endpoint_url}' no encontrado para el rol '{role_obj.name}'.")
        return jsonify(message=f"Endpoint '{endpoint_url}' not found"), 404
    
    print(f"Endpoint encontrado: {endpoint.endpoint_url} para el rol {role_obj.name}")
    
    # Construir la ruta del archivo de log
    log_dir = os.path.join(os.getcwd(), 'user-logs', role)
    log_file_path = os.path.join(log_dir, f"{endpoint_url}.log")
    
    # Verificar si el archivo existe
    if not os.path.exists(log_file_path):
        return jsonify(message=f"Log file for {role}/{endpoint_url} not found"), 404
    
    try:
        # Leer el contenido del archivo con la codificación utf-8
        with open(log_file_path, 'r', encoding='utf-8') as log_file:
            log_content = log_file.read()
        
        # Serializar manualmente el JSON asegurando la codificación utf-8
        response_data = json.dumps({
            "role": role,
            "endpoint_url": endpoint_url,
            "log_content": log_content
        }, ensure_ascii=False)  # ensure_ascii=False is crucial for preserving special characters

        # Devolver la respuesta JSON con la cabecera correcta
        return Response(response_data, content_type="application/json; charset=utf-8")
    
    except Exception as e:
        return jsonify(message="An error occurred while reading the log file", error=str(e)), 500 