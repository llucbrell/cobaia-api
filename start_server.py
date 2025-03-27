from app import create_app, db
from flask_security.utils import hash_password

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crear todas las tablas en la base de datos
        db.create_all()

        # Crear un usuario administrador si no existe
        user_datastore = app.extensions['security'].datastore
        
        # Verifica si el rol 'admin' existe
        admin_role = user_datastore.find_role('admin')
        if not admin_role:
            admin_role = user_datastore.create_role(name='admin')
    
        # Verifica si el rol 'user' existe
        user_role = user_datastore.find_role('user')
        if not user_role:
            user_role = user_datastore.create_role(name='user')
        
        # Crea un usuario administrador y asigna el rol 'admin'
        if not user_datastore.find_user(email='admin@example.com'):
            user_datastore.create_user(
                email='admin@example.com',
                password=hash_password('admin'),
                name='Admin',  # Proporciona un valor para el campo 'name'
                roles=[admin_role]
            )

         # Crea un usuario regular y asigna el rol 'user'
        if not user_datastore.find_user(email='user@example.com'):
            user_datastore.create_user(
                email='user@example.com',
                password=hash_password('user'),
                name='User',  # Proporciona un valor para el campo 'name'
                roles=[user_role]
            )

        # Guardar cambios en la base de datos
        db.session.commit()

    # Ejecutar la aplicación
    app.run(debug=True)
