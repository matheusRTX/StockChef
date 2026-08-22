from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('Administrador', 'Funcionario'), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(nome, email, senha_hash, tipo):
        novo = Usuario(nome=nome, email=email, senha=senha_hash, tipo=tipo)
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_usuario):
        return Usuario.query.get(id_usuario)

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def listar_todos():
        return Usuario.query.filter_by(ativo=True).all()

    @staticmethod
    def atualizar(usuario, **campos):
        for campo, valor in campos.items():
            setattr(usuario, campo, valor)
        db.session.commit()
        return usuario

    @staticmethod
    def deletar(usuario):
        # Soft delete: mantém o registro, apenas desativa
        usuario.ativo = False
        db.session.commit()
