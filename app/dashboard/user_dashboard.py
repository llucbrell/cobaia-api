from flask import Blueprint, render_template, redirect, url_for, request, jsonify 
from flask_security import login_required, current_user
from app.models import Endpoint, Role
from app import db
import genson

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Obtener todos los roles del usuario actual
    user_roles = [role.id for role in current_user.roles]
    
    # Depuración: Imprimir los roles del usuario
    print(f"User Roles: {user_roles}")
    
    # Obtener todos los endpoints asociados a cualquiera de los roles del usuario
    # La consulta asegura que también se obtienen los roles asociados
    endpoints_with_roles = db.session.query(Endpoint, Role).outerjoin(Role).filter(Endpoint.role_id.in_(user_roles)).all()
    
    # Depuración: Imprimir los endpoints obtenidos con los roles asociados
    print(f"Endpoints with Roles: {endpoints_with_roles}")
    
    # Verificar si hay endpoints disponibles
    if not endpoints_with_roles:
        message = "No endpoints available. Create one to get started."
    else:
        message = None
    
    # Pasar tanto los endpoints como los roles al template
    return render_template('dashboard.html', name=current_user.name, endpoints=endpoints_with_roles, message=message)


@dashboard_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_endpoint():
    if request.method == 'POST':
        model_name = request.form.get('model_name')
        schema = request.form.get('schema')
        target_url = request.form.get('target_url')
        endpoint_url = request.form.get('endpoint_url')
        role_id = request.form.get('role_id')  # Capturamos el rol seleccionado
        
        # Crear el nuevo endpoint con todos los datos
        new_endpoint = Endpoint(model_name=model_name, schema=schema, target_url=target_url, endpoint_url=endpoint_url, role_id=role_id)
        
        db.session.add(new_endpoint)
        db.session.commit()
        
        return redirect(url_for('dashboard.index'))
    
    # Pasar los roles del usuario al formulario para que pueda seleccionar uno
    roles = current_user.roles
    return render_template('create_endpoint.html', roles=roles)

@dashboard_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_endpoint(id):
    endpoint = Endpoint.query.get_or_404(id)
    
    if request.method == 'POST':
        endpoint.model_name = request.form.get('model_name')
        endpoint.schema = request.form.get('schema')
        endpoint.target_url = request.form.get('target_url')
        endpoint.endpoint_url = request.form.get('endpoint_url')
        endpoint.role_id = request.form.get('role_id')  # Actualizamos el role_id seleccionado
        
        db.session.commit()
        return redirect(url_for('dashboard.index'))
    
    # Pasar los roles del usuario al formulario para que pueda seleccionar uno
    roles = current_user.roles
    return render_template('edit_endpoint.html', endpoint=endpoint, roles=roles)

@dashboard_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_endpoint(id):
    endpoint = Endpoint.query.get_or_404(id)
    db.session.delete(endpoint)
    db.session.commit()
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/update_model_name/<int:endpoint_id>', methods=['POST'])
@login_required
def update_model_name(endpoint_id):
    endpoint = Endpoint.query.get_or_404(endpoint_id)
    model_name = request.json.get('model_name')
    
    if model_name:
        endpoint.model_name = model_name
        db.session.commit()
        return jsonify({"message": "Model name updated successfully"}), 200
    return jsonify({"message": "Model name not provided"}), 400

@dashboard_bp.route('/update_model_context_window/<int:endpoint_id>', methods=['POST'])
@login_required
def update_model_context_window(endpoint_id):
    endpoint = Endpoint.query.get_or_404(endpoint_id)
    model_context = request.json.get('model_context_window')
    
    if model_context:
        endpoint.model_context_window = model_context
        db.session.commit()
        return jsonify({"message": "Model context window updated successfully"}), 200
    return jsonify({"message": "Model context window not provided"}), 400

@dashboard_bp.route('/update_additional_prompt/<int:endpoint_id>', methods=['POST'])
@login_required
def update_additional_prompt(endpoint_id):
    data = request.get_json()
    endpoint = Endpoint.query.get_or_404(endpoint_id)
    endpoint.additional_prompt = data.get('additional_prompt', '')
    db.session.commit()
    return jsonify(message="Prompt updated successfully")


@dashboard_bp.route('/update_schema/<int:endpoint_id>', methods=['POST'])
@login_required
def update_schema(endpoint_id):
    endpoint = Endpoint.query.get_or_404(endpoint_id)
    schema = request.json.get('schema')
    
    if schema:
        endpoint.schema = schema
        db.session.commit()
        return jsonify({"message": "Schema updated successfully"}), 200
    return jsonify({"message": "Schema not provided"}), 400

@dashboard_bp.route('/generate_schema_with_genson', methods=['POST'])
@login_required
def generate_schema_with_genson():
    data = request.get_json()
    schema_builder = genson.SchemaBuilder()
    schema_builder.add_object(data)
    generated_schema = schema_builder.to_schema()
    return jsonify(generated_schema)