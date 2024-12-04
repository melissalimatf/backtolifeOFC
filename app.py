from datetime import timedelta
import os
from flask import Flask, render_template
from models import db
from routes import user_blueprint
from flask_jwt_extended import JWTManager  # Importe o JWTManager

# Diretório do banco de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'var', 'app-instance')
DB_PATH = os.path.join(DB_DIR, 'database.db')

# Garante que o diretório do banco de dados exista
os.makedirs(DB_DIR, exist_ok=True)

# Configuração do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'F023401823AJ84123840238482H384B12831230498123'  # Chave secreta do JWT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Tempo de expiração do token

# Inicializa o JWTManager com o Flask
jwt = JWTManager(app)

# Configuração do banco de dados
db.init_app(app)

with app.app_context():
    db.create_all()

# Registra o blueprint para as rotas de usuário
app.register_blueprint(user_blueprint)

# Rotas a fazer no routes.py
@app.route('/') 
def index(): 
    return render_template('index.html') 

@app.route('/instituicoes-reabilitacao') 
def instituicoes_reabilitacao(): 
    return render_template('instituicoes-reabilitacao.html') 

@app.route('/instituicoes-ensino') 
def instituicoes_ensino(): 
    return render_template('instituicoes-ensino.html') 

@app.route('/sobre-nos') 
def sobre_nos(): 
    return render_template('sobre-nos.html') 

@app.route('/suporte') 
def suporte(): 
    return render_template('suporte.html')

# Inicializa a aplicação
if __name__ == "__main__":
    app.run(debug=True)
