from datetime import datetime
from backend.models.usuario import db


class Produto(db.Model):
    __tablename__ = 'produtos'

    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    codigo_barras = db.Column(db.String(100))
    qr_code = db.Column(db.String(255))
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    id_unidade = db.Column(db.Integer, db.ForeignKey('unidades_medida.id_unidade'), nullable=False)
    estoque_minimo = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    imagem = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    atualizado_em = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_usuario, nome, id_categoria, id_unidade, descricao=None,
              codigo_barras=None, qr_code=None, estoque_minimo=0, imagem=None):
        novo = Produto(
            id_usuario=id_usuario,
            nome=nome,
            descricao=descricao,
            codigo_barras=codigo_barras,
            qr_code=qr_code,
            id_categoria=id_categoria,
            id_unidade=id_unidade,
            estoque_minimo=estoque_minimo,
            imagem=imagem,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_produto):
        return Produto.query.get(id_produto)

    @staticmethod
    def listar_todos():
        return Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()

    @staticmethod
    def listar_por_usuario(id_usuario):
        return Produto.query.filter_by(id_usuario=id_usuario, ativo=True).order_by(Produto.nome).all()

    @staticmethod
    def atualizar(produto, **campos):
        for campo, valor in campos.items():
            setattr(produto, campo, valor)
        db.session.commit()
        return produto

    @staticmethod
    def deletar(produto):
        # Soft delete: mantém o histórico (lotes, movimentações, pratos)
        produto.ativo = False
        db.session.commit()
