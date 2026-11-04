from backend.models.usuario import db


class UnidadeMedida(db.Model):
    __tablename__ = 'unidades_medida'

    id_unidade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sigla = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(60), nullable=False)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(sigla, descricao):
        nova = UnidadeMedida(sigla=sigla, descricao=descricao)
        db.session.add(nova)
        db.session.commit()
        return nova

    @staticmethod
    def buscar_por_id(id_unidade):
        return UnidadeMedida.query.get(id_unidade)

    @staticmethod
    def listar_todos():
        return UnidadeMedida.query.order_by(UnidadeMedida.descricao).all()

    @staticmethod
    def atualizar(unidade, **campos):
        for campo, valor in campos.items():
            setattr(unidade, campo, valor)
        db.session.commit()
        return unidade

    @staticmethod
    def deletar(unidade):
        db.session.delete(unidade)
        db.session.commit()
