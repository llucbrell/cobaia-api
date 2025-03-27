from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask import redirect, url_for, request
from wtforms_alchemy import ModelForm
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from flask_admin.menu import MenuLink
from .models import User, Role, Token, Endpoint
from . import db

# Usar WTForms-Alchemy para generar automáticamente el formulario de Token
class TokenForm(ModelForm):
    class Meta:
        model = Token  # Asocia el formulario con el modelo Token

# Vista personalizada para proteger el acceso
class SecureModelView(ModelView):
    def is_accessible(self):
        # Verifica si el usuario está autenticado y tiene el rol de 'admin'
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # Redirige a la página de inicio de sesión si el usuario no tiene acceso
        if not current_user.is_authenticated:
            return redirect(url_for('security.login', next=request.url))  # Redirige a login con la URL original
        return redirect(url_for('dashboard.index'))  # Si está autenticado pero no es admin, redirige al dashboard

# Vista personalizada para la página principal del admin
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login', next=request.url))  # Redirige a login con la URL original
        return redirect(url_for('dashboard.index'))  # Si está autenticado pero no es admin, redirige al dashboard

# Vista personalizada para gestionar usuarios
class UserModelView(SecureModelView):
    form_excluded_columns = ['fs_uniquifier']
    column_list = ['id', 'name', 'email', 'active', 'roles']
    # Formateador personalizado para mostrar nombres de roles
    column_formatters = {
        'roles': lambda view, context, model, name: ', '.join([role.name for role in model.roles])
    }
     # Personalizar el formulario para mostrar nombres de roles en lugar de objetos en el campo de selección
    form_args = {
        'roles': {
            'query_factory': lambda: Role.query.all(),
            'get_label': 'name'  # Mostrar los nombres de los roles en lugar de los objetos
        }
    }

class RoleModelView(SecureModelView):
    column_list = ['id', 'name', 'tokens', 'endpoints']

    # Formateador personalizado para mostrar los nombres de los usuarios asociados al rol
    column_formatters = {
        'tokens': lambda view, context, model, name: ', '.join([token.token for token in model.tokens]),
        'endpoints': lambda view, context, model, name: ', '.join([endpoint.model_name for endpoint in model.endpoints])
    }

    # Personalizar el formulario para seleccionar usuarios, tokens y endpoints relacionados
    form_args = {
        'users': {
            'query_factory': lambda: User.query.all(),
            'get_label': 'name'  # Mostrar los nombres de los usuarios en lugar de los objetos
        },
        'tokens': {
            'query_factory': lambda: Token.query.all(),
            'get_label': 'token'  # Mostrar los tokens en lugar de los objetos
        },
        'endpoints': {
            'query_factory': lambda: Endpoint.query.all(),
            'get_label': 'model_name'  # Mostrar los nombres de los endpoints en lugar de los objetos
        }
    }

# Vista personalizada para gestionar Tokens y su relación con Roles
class TokenModelView(SecureModelView):
    form = TokenForm  # Utiliza el formulario generado automáticamente
    column_list = ['id', 'token', 'role.name']

# Vista personalizada para gestionar Endpoints
class EndpointModelView(SecureModelView):
    column_list = ['id', 'model_name', 'target_url', 'role.name']

    # Formateador personalizado para mostrar el nombre del rol asociado al endpoint
    column_formatters = {
        'role.name': lambda view, context, model, name: model.role.name if model.role else ''
    }

    # Personalizar el formulario para mostrar nombres de roles en lugar de objetos en el campo de selección
    form_args = {
        'role': {
            'query_factory': lambda: Role.query.all(),
            'get_label': 'name'  # Mostrar los nombres de los roles en lugar de los objetos
        }
    }



def setup_admin(app):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())

    # Añadir vistas de modelos con protección de login
    admin.add_view(UserModelView(User, db.session))
    #admin.add_view(SecureModelView(Role, db.session))
    admin.add_view(TokenModelView(Token, db.session))
    admin.add_view(RoleModelView(Role, db.session, endpoint="admin_role"))
    admin.add_view(EndpointModelView(Endpoint, db.session))

    # Añadir enlace de logout
    admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
