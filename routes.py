from flask import Blueprint, redirect, request, jsonify, render_template, url_for, session
from models import Usuario, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


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

    if not senha:
        return jsonify({"error": "A senha é obrigatória"}), 400

    senha_hash = Usuario.hash_password(senha)

    if tipo_instituicao == 'education':
        if Usuario.query.filter_by(cpf_cnpj=cpf_cnpj).first():
            return jsonify({"error": "Instituição de ensino já cadastrada com este CPF/CNPJ"}), 400

        novo_usuario = Usuario(
            tipo_instituicao=tipo_instituicao,
            nome_instituicao=nome_instituicao,
            cpf_cnpj=cpf_cnpj,
            email=email,
            senha=senha_hash
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
            senha=senha_hash
        )
    else:
        return jsonify({"error": "Tipo de instituição inválido"}), 400

    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('user.perfil'))  # Redireciona para a página de login após o cadastro


# Login
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not usuario.check_password(senha):
        return jsonify({"error": "Credenciais inválidas"}), 401

    session['user_id'] = usuario.id
    return redirect(url_for('user.perfil'))  # Redireciona para o perfil do usuário após login bem-sucedido



# Atualizar usuário
@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.json
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    usuario.update(data)
    db.session.commit()
    return jsonify({"message": "Usuário atualizado com sucesso"}), 200

# Excluir usuário
@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"message": "Usuário excluído com sucesso"}), 200

# Página de login
@user_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

from flask import render_template, session, redirect, url_for

@user_blueprint.route('/perfil')
def perfil():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user.login'))  # Redireciona para login se não estiver logado

    # Busca o usuário no banco de dados
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Passa o usuário para o template
    return render_template('perfil.html', usuario=usuario)

