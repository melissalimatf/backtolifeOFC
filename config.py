# config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'F023401823AJ84123840238482H384B12831230498123'  # Altere para um valor seguro no ambiente de produção
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.getcwd(), "var", "app-instance", "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
