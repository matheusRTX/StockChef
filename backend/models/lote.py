from datetime import datetime
from backend.models.usuario import db


class Lote(db.Model):
    __tablename__ = 'lotes'

    id_lote = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)
    numero_lote = db.Column(db.String(60))
    validade = db.Column(db.Date, nullable=False)
    quantidade_inicial = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_atual = db.Column(db.Numeric(10, 2), nullable=False)
    custo_unitario = db.Column(db.Numeric(10, 2))
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    observacao = db.Column(db.Text)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_produto, validade, quantidade_inicial, numero_lote=None,
              custo_unitario=None, observacao=None):
        novo = Lote(
            id_produto=id_produto,
            numero_lote=numero_lote,
            validade=validade,
            quantidade_inicial=quantidade_inicial,
            quantidade_atual=quantidade_inicial,
            custo_unitario=custo_unitario,
            observacao=observacao,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_lote):
        return Lote.query.get(id_lote)

    @staticmethod
    def listar_todos():
        return Lote.query.order_by(Lote.validade).all()

    @staticmethod
    def listar_por_produto(id_produto):
        return Lote.query.filter_by(id_produto=id_produto).order_by(Lote.validade).all()

    @staticmethod
    def atualizar(lote, **campos):
        for campo, valor in campos.items():
            setattr(lote, campo, valor)
        db.session.commit()
        return lote

    @staticmethod
    def deletar(lote):
        db.session.delete(lote)
        db.session.commit()
