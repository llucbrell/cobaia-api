from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint


# Inicializa la base de datos y las extensiones
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos y las extensiones
    db.init_app(app)

    # Importar los modelos aquí para que sean conocidos por SQLAlchemy
    from app.models import User, Role  # Importación después de inicializar `db`
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    # Registrar los blueprints existentes
    from app.routes import main
    app.register_blueprint(main)

    # Registrar el blueprint de autenticación (auth)
    from app.auth import auth
    app.register_blueprint(auth)

    # Registrar el blueprint de la doc de la api
    #from app.api_docs import api_docs
    #app.register_blueprint(api_docs)

    # Configuración de Swagger-UI
    SWAGGER_URL = '/api'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
        'app_name': "Cobaia API docs",
        'favicon32': "/static/images/cobaia.png",  # Cambia el logotipo
        'favicon16': "/static/images/cobaia.png",
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

 
    # Registrar el blueprint dinámico (dynamic)
    from app.dynamic import dynamic
    app.register_blueprint(dynamic)
    from app.dynamic_chat import dynamic_chat
    app.register_blueprint(dynamic_chat)
    from app.model_logs import dynamic_logs
    app.register_blueprint(dynamic_logs)
    from app.model_logs import dynamic_api_logs
    app.register_blueprint(dynamic_api_logs)

    # Registrar el blueprint del dashboard (dashboard)
    from app.dashboard.user_dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # Configurar el panel de administración
    from app.admin import setup_admin
    setup_admin(app)

    return app
