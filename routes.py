from flask import Blueprint, Flask, app, request, jsonify, render_template, redirect, url_for
from models import Usuario, db

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
        if tipo_instituicao == 'education':
            # Apenas 1 usuário por CPF/CNPJ
            if Usuario.query.filter_by(cpf_cnpj=cpf_cnpj).first():
                return jsonify({"error": "Instituição de ensino já cadastrada com este CPF/CNPJ"}), 400
            
            novo_usuario = Usuario(
                tipo_instituicao=tipo_instituicao,
                nome_instituicao=nome_instituicao,
                cpf_cnpj=cpf_cnpj,
                email=email,
                senha=senha
            )

            

        elif tipo_instituicao == 'rehab':
            # Várias casas de reabilitação podem ser cadastradas, mas o CPF do usuário deve ser único
            if Usuario.query.filter_by(cpf_usuario=cpf_usuario).first():
                return jsonify({"error": "CPF do usuário já cadastrado"}), 400

            novo_usuario = Usuario(
                tipo_instituicao=tipo_instituicao,
                nome_instituicao=nome_instituicao,
                cpf_cnpj=cpf_cnpj,
                nome_usuario=nome_usuario,
                cpf_usuario=cpf_usuario,
                email=email,
                senha=senha
            )

            
        else:
            return jsonify({"error": "Tipo de instituição inválido"}), 400

        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"message": "Cadastro realizado com sucesso"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Atualizar usuário
@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
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
    usuario.senha = data.get('senha', usuario.senha)

    try:
        db.session.commit()
        return jsonify({"message": "Usuário atualizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Excluir usuário
@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
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


# Login
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email, senha=senha).first()
    
    if usuario:
        # Login bem-sucedido retorna JSON
        return jsonify({
            "message": "Login realizado com sucesso",
            "user": usuario.to_dict()
        }), 200

    # Login falhou
    return jsonify({"error": "Credenciais inválidas"}), 401


# Rota para exibir o login.html
@user_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Rota para exibir o perfil do usuário TESTE
@user_blueprint.route('/perfil', methods=['GET'])
def perfil():
    return render_template('perfil.html')


