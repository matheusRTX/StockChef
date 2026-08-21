from datetime import datetime
from backend.models.usuario import db


class Prato(db.Model):
    __tablename__ = 'pratos'

    id_prato = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    id_tipo_culinaria = db.Column(db.Integer, db.ForeignKey('tipos_culinaria.id_tipo_culinaria'), nullable=False)
    tempo_preparo = db.Column(db.Integer, nullable=False)
    rendimento = db.Column(db.Integer, nullable=False)
    modo_preparo = db.Column(db.Text, nullable=False)
    favorito = db.Column(db.Boolean, nullable=False, default=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    imagem = db.Column(db.String(255))
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_usuario, nome, id_tipo_culinaria, tempo_preparo, rendimento,
              modo_preparo, descricao=None, favorito=False, imagem=None):
        novo = Prato(
            id_usuario=id_usuario,
            nome=nome,
            descricao=descricao,
            id_tipo_culinaria=id_tipo_culinaria,
            tempo_preparo=tempo_preparo,
            rendimento=rendimento,
            modo_preparo=modo_preparo,
            favorito=favorito,
            imagem=imagem,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_prato):
        return Prato.query.get(id_prato)

    @staticmethod
    def listar_todos():
        return Prato.query.filter_by(ativo=True).order_by(Prato.nome).all()

    @staticmethod
    def listar_por_usuario(id_usuario):
        return Prato.query.filter_by(id_usuario=id_usuario, ativo=True).order_by(Prato.nome).all()

    @staticmethod
    def listar_favoritos():
        return Prato.query.filter_by(ativo=True, favorito=True).order_by(Prato.nome).all()

    @staticmethod
    def atualizar(prato, **campos):
        for campo, valor in campos.items():
            setattr(prato, campo, valor)
        db.session.commit()
        return prato

    @staticmethod
    def deletar(prato):
        # Soft delete: mantém histórico de ingredientes e sugestões
        prato.ativo = False
        db.session.commit()
