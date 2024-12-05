from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    tipo_instituicao = db.Column(db.String(50), nullable=False)
    nome_instituicao = db.Column(db.String(100), nullable=False)
    cpf_cnpj = db.Column(db.String(14), unique=True, nullable=False)
    nome_usuario = db.Column(db.String(100), nullable=True)
    cpf_usuario = db.Column(db.String(11), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value if value else getattr(self, key))

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
