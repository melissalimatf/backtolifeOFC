from flask import Flask, render_template
from models import db
from routes import user_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user_blueprint)

#rotas a fazer no routes.py aqui só pra buildar o app
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


if __name__ == "__main__":
    app.run(debug=True)
