class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///security.db'
    SECURITY_PASSWORD_SALT = 'saltsecretkey'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_FLASH_MESSAGES = True
    SECURITY_LOGIN_URL = '/login'
    SECURITY_LOGOUT_URL = '/logout'
    SECURITY_POST_LOGIN_VIEW = '/admin'
    SECURITY_POST_LOGOUT_VIEW = '/login'


