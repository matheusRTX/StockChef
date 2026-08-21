from backend.models.usuario import db


class PratoIngrediente(db.Model):
    __tablename__ = 'prato_ingredientes'

    id_prato_ingrediente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_prato = db.Column(db.Integer, db.ForeignKey('pratos.id_prato'), nullable=False)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)
    quantidade = db.Column(db.Numeric(10, 2), nullable=False)
    observacao = db.Column(db.String(255))

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_prato, id_produto, quantidade, observacao=None):
        novo = PratoIngrediente(
            id_prato=id_prato,
            id_produto=id_produto,
            quantidade=quantidade,
            observacao=observacao,
        )
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_prato_ingrediente):
        return PratoIngrediente.query.get(id_prato_ingrediente)

    @staticmethod
    def listar_todos():
        return PratoIngrediente.query.all()

    @staticmethod
    def listar_por_prato(id_prato):
        return PratoIngrediente.query.filter_by(id_prato=id_prato).all()

    @staticmethod
    def atualizar(ingrediente, **campos):
        for campo, valor in campos.items():
            setattr(ingrediente, campo, valor)
        db.session.commit()
        return ingrediente

    @staticmethod
    def deletar(ingrediente):
        db.session.delete(ingrediente)
        db.session.commit()
