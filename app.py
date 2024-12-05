from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from models import db
from routes import user_blueprint
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa JWT e Banco de Dados
jwt = JWTManager(app)
db.init_app(app)

# Cria o banco de dados
DB_DIR = os.path.dirname(Config.SQLALCHEMY_DATABASE_URI.split('///')[1])
os.makedirs(DB_DIR, exist_ok=True)
with app.app_context():
    db.create_all()

# Registra as rotas
app.register_blueprint(user_blueprint)

# Rotas para o Frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sou-reabilitacao')
def instituicoes_reabilitacao():
    return render_template('sou-reabilitacao.html')

@app.route('/sou-instituicao')
def instituicoes_ensino():
    return render_template('sou-instituicao.html')

@app.route('/sobre-nos')
def sobre_nos():
    return render_template('sobre-nos.html')

@app.route('/suporte')
def suporte():
    return render_template('suporte.html')

@app.route('/cursos-disponiveis')
def cursos_disponiveis():
    return render_template('todos-cursos.html')


@app.route('/meus-cursos')
def meus_cursos():
    return render_template('meus-cursos.html')

@app.route('/curso-andamento')
def curso_andamento():
    return render_template('curso-andamento.html')

@app.route('/curso-andamento-disponivel')
def curso_andamento_disponivel():
    return render_template('curso-andamento-desbloqueado.html')

# Inicializa a aplicação
if __name__ == "__main__":
    app.run(debug=True)
