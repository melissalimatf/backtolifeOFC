from flask import Blueprint, request, jsonify, render_template
from models import Usuario, db
import bcrypt
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Configurações do JWT
SECRET_KEY = "F023401823AJ84123840238482H384B12831230498123"  # Substitua por uma chave secreta segura
ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Tempo de expiração do token

user_blueprint = Blueprint('user', __name__)

# Registro de usuários
@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.form

    tipo_instituicao = data.get('clientType')
    nome_instituicao = data.get('nome_instituicao')
    cpf_cnpj = data.get('cpf_cnpj')
    nome_usuario = data.get('nome_usuario')
    cpf_usuario = data.get('cpf_usuario')
    email = data.get('email')
    senha = data.get('senha')

    try:
        if not senha:
            return jsonify({"error": "A senha é obrigatória"}), 400

        # Criptografa a senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        if tipo_instituicao == 'education':
            if Usuario.query.filter_by(cpf_cnpj=cpf_cnpj).first():
                return jsonify({"error": "Instituição de ensino já cadastrada com este CPF/CNPJ"}), 400

            novo_usuario = Usuario(
                tipo_instituicao=tipo_instituicao,
                nome_instituicao=nome_instituicao,
                cpf_cnpj=cpf_cnpj,
                email=email,
                senha=senha_hash.decode('utf-8')
            )

        elif tipo_instituicao == 'rehab':
            if Usuario.query.filter_by(cpf_usuario=cpf_usuario).first():
                return jsonify({"error": "CPF do usuário já cadastrado"}), 400

            novo_usuario = Usuario(
                tipo_instituicao=tipo_instituicao,
                nome_instituicao=nome_instituicao,
                cpf_cnpj=cpf_cnpj,
                nome_usuario=nome_usuario,
                cpf_usuario=cpf_usuario,
                email=email,
                senha=senha_hash.decode('utf-8')
            )

        else:
            return jsonify({"error": "Tipo de instituição inválido"}), 400

        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"message": "Cadastro realizado com sucesso"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Login
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Verifica a senha
    if not bcrypt.checkpw(senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        return jsonify({"error": "Credenciais inválidas"}), 401

    # Gera o token JWT usando Flask-JWT-Extended
    access_token = create_access_token(identity=usuario.id, expires_delta=ACCESS_TOKEN_EXPIRES)

    return jsonify({
        "message": "Login realizado com sucesso",
        "access_token": access_token,
        "user": usuario.to_dict()
    }), 200


# Atualizar usuário (Exemplo com autorização)
@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()  # Protege a rota, só pode ser acessada com um token válido
def update_user(user_id):
    data = request.json
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    usuario.nome_instituicao = data.get('nome_instituicao', usuario.nome_instituicao)
    usuario.cpf_cnpj = data.get('cpf_cnpj', usuario.cpf_cnpj)
    usuario.nome_usuario = data.get('nome_usuario', usuario.nome_usuario)
    usuario.cpf_usuario = data.get('cpf_usuario', usuario.cpf_usuario)
    usuario.email = data.get('email', usuario.email)
    senha = data.get('senha')

    if senha:
        usuario.senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Excluir usuário (Exemplo com autorização)
@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()  # Protege a rota, só pode ser acessada com um token válido
def delete_user(user_id):
    usuario = Usuario.query.get(user_id)

    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    try:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuário excluído com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Rota para exibir o login.html
@user_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


# Rota para exibir o perfil do usuário (Exemplo com autorização)
@user_blueprint.route('/perfil', methods=['GET'])
@jwt_required()  # Protege a rota, só pode ser acessada com um token válido
def perfil():
    current_user_id = get_jwt_identity()  # Pega a identidade do usuário no token JWT
    usuario = Usuario.query.get(current_user_id)

    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return render_template('perfil.html', user=usuario)
