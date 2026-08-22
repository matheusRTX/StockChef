from backend.models.usuario import db


class TipoCulinaria(db.Model):
    __tablename__ = 'tipos_culinaria'

    id_tipo_culinaria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(nome, descricao=None):
        novo = TipoCulinaria(nome=nome, descricao=descricao)
        db.session.add(novo)
        db.session.commit()
        return novo

    @staticmethod
    def buscar_por_id(id_tipo_culinaria):
        return TipoCulinaria.query.get(id_tipo_culinaria)

    @staticmethod
    def listar_todos():
        return TipoCulinaria.query.order_by(TipoCulinaria.nome).all()

    @staticmethod
    def atualizar(tipo_culinaria, **campos):
        for campo, valor in campos.items():
            setattr(tipo_culinaria, campo, valor)
        db.session.commit()
        return tipo_culinaria

    @staticmethod
    def deletar(tipo_culinaria):
        db.session.delete(tipo_culinaria)
        db.session.commit()
