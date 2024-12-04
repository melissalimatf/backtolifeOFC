from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    tipo_instituicao = db.Column(db.String(50), nullable=False)  # 'rehab' ou 'education'
    nome_instituicao = db.Column(db.String(100), nullable=False)
    cpf_cnpj = db.Column(db.String(14), unique=True, nullable=False)  # CPF ou CNPJ
    nome_usuario = db.Column(db.String(100), nullable=True)  # Apenas para casas de reabilitação
    cpf_usuario = db.Column(db.String(11), unique=True, nullable=True)  # CPF do usuário
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)  # Senha não encriptada conforme solicitado

    def to_dict(self):
        return {
            "id": self.id,
            "tipo_instituicao": self.tipo_instituicao,
            "nome_instituicao": self.nome_instituicao,
            "cpf_cnpj": self.cpf_cnpj,
            "nome_usuario": self.nome_usuario,
            "cpf_usuario": self.cpf_usuario,
            "email": self.email
        }
