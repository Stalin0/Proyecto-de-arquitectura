import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-llave-secreta-muy-segura'
    DB_HOST = 'localhost'
    DB_NAME = 'cursos'
    DB_USER = 'postgres'
    DB_PASS = '12345'
    DB_PORT = '5432'
