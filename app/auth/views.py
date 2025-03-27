from flask import render_template
from flask_security import login_required
from . import auth


#@auth.route('/dashboard')
#@login_required  # Protege esta ruta, solo accesible para usuarios autenticados
#def dashboard():
#    return render_template('dashboard.html', message="Bienvenido al panel de usuario protegido.")

#@auth.route('/admin')
#@login_required  # Protege esta ruta, solo accesible para usuarios autenticados
#def admin():
#    return render_template('dashboard.html', message="Bienvenido al panel de usuario protegido.")




@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('security.login'))
