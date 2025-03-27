from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask import redirect, url_for, request

class AdminModelView(ModelView):
    def is_accessible(self):
        # Solo permitir acceso si el usuario está autenticado y tiene el rol 'admin'
        return current_user.is_authenticated and current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        # Redirigir a la página de login si el usuario no tiene acceso
        return redirect(url_for('security.login', next=request.url))
