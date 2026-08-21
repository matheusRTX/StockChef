from backend.models.usuario import db


class MovimentacaoItem(db.Model):
    __tablename__ = 'movimentacao_itens'

    id_movimentacao_item = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_movimentacao = db.Column(db.Integer, db.ForeignKey('movimentacoes.id_movimentacao'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)
    quantidade = db.Column(db.Numeric(10, 2), nullable=False)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_movimentacao, id_produto, quantidade):
        novo = MovimentacaoItem(
            id_movimentacao=id_movimentacao,
            id_produto=id_produto,
            quantidade=quantidade,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_movimentacao_item):
        return MovimentacaoItem.query.get(id_movimentacao_item)

    @staticmethod
    def listar_todos():
        return MovimentacaoItem.query.all()

    @staticmethod
    def listar_por_movimentacao(id_movimentacao):
        return MovimentacaoItem.query.filter_by(id_movimentacao=id_movimentacao).all()

    @staticmethod
    def atualizar(item, **campos):
        for campo, valor in campos.items():
            setattr(item, campo, valor)
        db.session.commit()
        return item

    @staticmethod
    def deletar(item):
        db.session.delete(item)
        db.session.commit()
