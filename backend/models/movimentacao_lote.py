from backend.models.usuario import db


class MovimentacaoLote(db.Model):
    __tablename__ = 'movimentacao_lotes'

    id_movimentacao_lote = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_movimentacao_item = db.Column(db.Integer, db.ForeignKey('movimentacao_itens.id_movimentacao_item'), nullable=False)
    id_lote = db.Column(db.Integer, db.ForeignKey('lotes.id_lote'), nullable=False)
    quantidade = db.Column(db.Numeric(10, 2), nullable=False)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_movimentacao_item, id_lote, quantidade):
        novo = MovimentacaoLote(
            id_movimentacao_item=id_movimentacao_item,
            id_lote=id_lote,
            quantidade=quantidade,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_movimentacao_lote):
        return MovimentacaoLote.query.get(id_movimentacao_lote)

    @staticmethod
    def listar_todos():
        return MovimentacaoLote.query.all()

    @staticmethod
    def listar_por_item(id_movimentacao_item):
        return MovimentacaoLote.query.filter_by(id_movimentacao_item=id_movimentacao_item).all()

    @staticmethod
    def atualizar(registro, **campos):
        for campo, valor in campos.items():
            setattr(registro, campo, valor)
        db.session.commit()
        return registro

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)
        db.session.commit()
