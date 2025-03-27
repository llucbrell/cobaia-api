import uuid
from . import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy.event import listens_for

# Relación muchos a muchos entre usuarios y roles
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    tokens = db.relationship('Token', backref='role', lazy=True)
    endpoints = db.relationship('Endpoint', backref='role', lazy=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))  # Automáticamente genera un UUID
    name = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Endpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endpoint_url = db.Column(db.String(255), nullable=False)  # Nuevo campo endpoint_url
    endpoint_description = db.Column(db.Text, nullable=True)
    schema = db.Column(db.Text, nullable=False)
    model_name = db.Column(db.String(255), nullable=False)
    model_context_window = db.Column(db.BigInteger, nullable=True)
    target_url = db.Column(db.String(255), nullable=False)
    request = db.Column(db.Text, nullable=True)
    additional_prompt = db.Column(db.Text, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

# Escucha el evento de inserción para el modelo User para asegurarse de que el fs_uniquifier esté presente
@listens_for(User, 'before_insert')
def generate_fs_uniquifier(mapper, connect, target):
    if not target.fs_uniquifier:
        target.fs_uniquifier = str(uuid.uuid4())
