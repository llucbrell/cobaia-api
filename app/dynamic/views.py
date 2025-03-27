from flask import request, jsonify
from . import dynamic
from ..models import Token, Endpoint, Role
from app.ia_tools.tokenizer import TokenizerWrapper
from app.ia_tools.json_validator import JSONValidator
from app.ia_tools.engine import EngineBuilder
from app.ia_tools.pdf_handler import process_pdf
from app.ia_tools.pdf2markdown_handler import pdf_to_markdown_with_structure
from app.ia_tools.pdf2img_handler import save_pdf_pages_as_jpg
import os
import shutil
import subprocess
from werkzeug.utils import secure_filename
from PIL import Image


# Definir las extensiones permitidas
ALLOWED_DOC_EXTENSIONS = {'pdf', 'txt'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Directorio donde se guardarán los archivos subidos
UPLOAD_FOLDER = 'uploads'  # Asegúrate de que este directorio exista o se cree

# Asegúrate de que el directorio de uploads existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def remove_files_from_upload_folder():
    # Borrar todos los archivos en el directorio 'uploads'
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')



# Función de verificación de seguridad común
def security_checks(token_value, role, endpoint_url):
    print(f"Token recibido: {token_value}")
    
    # Verificar si el token está presente en la base de datos
    token = Token.query.filter_by(token=token_value).first()
    
    if token is None:
        print("Token no encontrado o inválido.")
        return None, None, None
    
    print(f"Token válido encontrado: {token.token}")
    
    # Buscar el rol correspondiente al valor recibido en la URL
    role_obj = Role.query.filter_by(name=role).first()
    
    if role_obj is None:
        print(f"Rol '{role}' no encontrado.")
        return token, None, None
    
    print(f"Rol encontrado: {role_obj.name}")
    
    # Verificar si el token tiene acceso al rol
    if token.role_id != role_obj.id:
        print(f"Acceso denegado al rol '{role_obj.name}' para el token.")
        return token, role_obj, None
    
    print(f"Acceso concedido al rol '{role_obj.name}' para el token.")
    
    # Verificar si existe el endpoint con el rol y el endpoint_url dados
    endpoint = Endpoint.query.filter_by(role_id=role_obj.id, endpoint_url=endpoint_url).first()
    
    if endpoint is None:
        print(f"Endpoint '{endpoint_url}' no encontrado para el rol '{role_obj.name}'.")
        return token, role_obj, None
    
    print(f"Endpoint encontrado: {endpoint.endpoint_url} para el rol {role_obj.name}")
    
    return token, role_obj, endpoint

@dynamic.route('/api/documents/img/<role>/<endpoint_url>', methods=['POST'])
def handle_documents_images(role, endpoint_url):
    # Verificaciones de seguridad (token, role, endpoint)
    token_value = request.headers.get('Authorization')
    token, role_obj, endpoint = security_checks(token_value, role, endpoint_url)
    if not token or not role_obj or not endpoint:
        return jsonify(message="Security check failed"), 403

    # Procesamiento de archivos PDF
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files['file']
    
    allow = allowed_file(file.filename, ALLOWED_DOC_EXTENSIONS)
    if not allow:
        return jsonify(message=f"Unsupported file type, only {ALLOWED_DOC_EXTENSIONS}"), 400

    if file:
        # Guardar el archivo temporalmente
        pdf_path = os.path.join(UPLOAD_FOLDER, 'temp.pdf')
        file.save(pdf_path)

        # Convertir el PDF a imágenes
        images = save_pdf_pages_as_jpg(pdf_path)

        print(len(images))
        #print(images[0])

        #remove_files_from_upload_folder()
        # Responder con las imágenes en formato base64
        return jsonify({
            "message": "Images created",
            #"images": images  # Lista de imágenes en base64
        })
    else:
        return jsonify(message="File not found, please mark it as multipart/form named 'file'"), 400

@dynamic.route('/api/documents/md/<role>/<endpoint_url>', methods=['POST'])
def handle_documents_md(role, endpoint_url):
    # Verificaciones de seguridad (token, role, endpoint)
    token_value = request.headers.get('Authorization')
    token, role_obj, endpoint = security_checks(token_value, role, endpoint_url)
    if not token or not role_obj or not endpoint:
        return jsonify(message="Security check failed"), 403

    # Procesamiento de archivos PDF y TXT
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files['file']

    # Obtener los otros parámetros desde request.form
    prompt = request.form.get('prompt')
    validation = request.form.get('validation') == 'true'
    report_markdown = request.form.get('reportMarkdown') == 'true'
    dynamic_prompt_model_memory = request.form.get('dynamicPromptModelMemory') == 'true'
    
    allow = allowed_file(file.filename, ALLOWED_DOC_EXTENSIONS)
    if not allow:
        return jsonify(message=f"Unsupported file type, only {ALLOWED_DOC_EXTENSIONS}"), 400

    if file:
        # Guardar temporalmente el archivo para procesamiento
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Procesar el archivo con Marker y convertirlo a Markdown
        markdown_path = os.path.join(UPLOAD_FOLDER, 'prueba.md')
        
        try:
            # Run the marker command to convert the PDF to Markdown
            subprocess.run(
                ["marker_single", file_path, markdown_path],
                check=True
            )

            # Leer el contenido del archivo Markdown generado
            with open(markdown_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            # Responder con la confirmación de que se guardó el archivo
            return jsonify({
                "message": "Markdown file created",
                "markdown_file": 'prueba.md',
                "text": markdown_content,
            })

        except subprocess.CalledProcessError as e:
            return jsonify(message=f"Error processing PDF: {str(e)}"), 500

    else:
        return jsonify(message="File not found, please mark it as multipart/form named 'file'"), 400

# Endpoint para manejar archivos PDF y TXT
@dynamic.route('/api/documents/txt/<role>/<endpoint_url>', methods=['POST'])
def handle_documents(role, endpoint_url):
    # Verificaciones de seguridad (token, role, endpoint)
    token_value = request.headers.get('Authorization')
    token, role_obj, endpoint = security_checks(token_value, role, endpoint_url)
    if not token or not role_obj or not endpoint:
        return jsonify(message="Security check failed"), 403

    # Procesamiento de archivos PDF y TXT
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400
    file = request.files['file']

    # Obtener los otros parámetros desde request.form
    prompt = request.form.get('prompt')
    validation = request.form.get('validation') == 'true'  # Convertir a booleano
    report_markdown = request.form.get('reportMarkdown') == 'true'
    dynamic_prompt_model_memory = request.form.get('dynamicPromptModelMemory') == 'true'
    allow =allowed_file(file.filename, ALLOWED_DOC_EXTENSIONS)
    if not allow:
        return jsonify(message=f"Unsupported file type, only {ALLOWED_DOC_EXTENSIONS}"), 400
    # Verificar el tipo de archivo
    if file:
        # Procesar el archivo como antes
        print(f"Archivo guardado en {file.filename}")

        # Llamada al motor de procesamiento (simulada)
        # Aquí podrías usar estos parámetros en el procesamiento
        print(f"Prompt: {prompt}")
        print(f"Validation: {validation}")
        print(f"Report Markdown: {report_markdown}")
        print(f"Dynamic Prompt Model Memory: {dynamic_prompt_model_memory}")

        # Procesar el archivo PDF
        text, images = process_pdf(file)
        
        # Respuesta
        return jsonify({
            "message": "Ok",
            "text": text,
            "images": images
        })
    else:
        return jsonify(message="File not found, please mark it as multipart/form named 'file'"), 400



@dynamic.route('/api/image/<role>/<endpoint_url>', methods=['POST'])
def handle_images(role, endpoint_url):
    # Verificaciones de seguridad (token, role, endpoint)
    token_value = request.headers.get('Authorization')
    token, role_obj, endpoint = security_checks(token_value, role, endpoint_url)
    if not token or not role_obj or not endpoint:
        return jsonify(message="Security check failed"), 403

    # Procesamiento de imágenes JPG y PNG
    if 'file' not in request.files:
        return jsonify(message="No file part"), 400

    file = request.files['file']
    # Obtener parámetros adicionales
    new_width = request.form.get('width', type=int)
    new_height = request.form.get('height', type=int)
    document_id = request.form.get('document_id')
    patient_id = request.form.get('patient_id')

    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        # Directorio donde se guardarán las imágenes
        upload_folder = './uploads/images'

        # Crea el directorio si no existe
        os.makedirs(upload_folder, exist_ok=True)

        # Guarda y redimensiona la imagen
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        print(f"Imagen guardada en {file_path}, Document ID: {document_id}, Patient ID: {patient_id}")

        # Redimensionar si se especificaron dimensiones
        # Redimensionar si se especificaron dimensiones
    if new_width and new_height:
        img = Image.open(file_path)
        img = img.resize((new_width, new_height), ImageResampling.LANCZOS)
        img.save(file_path)  # Sobreescribe la imagen original con la redimensionada
        if new_width and new_height:
            img = Image.open(file_path)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save(file_path)  # Sobreescribe la imagen original con la redimensionada

        return jsonify(message="Image uploaded successfully"), 200
    else:
        return jsonify(message="Unsupported image type"), 400

       # Llamada al motor de procesamiento
        #engine = EngineBuilder(error_log_path=f"user-logs/{role}/{endpoint_url}/images")
        #req_data = {"file_path": file_path}
        #resp = engine.run(endpoint, req_data)
        #return resp



@dynamic.route('/api/<role>/<endpoint_url>', methods=['GET', 'POST'])
def dynamic_route(role, endpoint_url):
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

   
    # Aquí puedes manejar la lógica personalizada para este endpoint
    if request.method == 'GET':
        return jsonify(message=f"GET request to {role}/{endpoint_url} to work with FHIR use POST or visit API docs for more information")
    elif request.method == 'POST':
        req_data = request.json
        engine = EngineBuilder(error_log_path=f"user-logs/{role}{endpoint_url}")    
        resp = engine.run(endpoint, req_data)
        #resp['internal_url_info']=f"{role}/{endpoint_url}" 
        return resp
