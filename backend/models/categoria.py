from backend.models.usuario import db


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(255))

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(nome, descricao=None):
        nova = Categoria(nome=nome, descricao=descricao)
        db.session.add(nova)
        db.session.commit()
        return nova

    @staticmethod
    def buscar_por_id(id_categoria):
        return Categoria.query.get(id_categoria)

    @staticmethod
    def listar_todos():
        return Categoria.query.order_by(Categoria.nome).all()

    @staticmethod
    def atualizar(categoria, **campos):
        for campo, valor in campos.items():
            setattr(categoria, campo, valor)
        db.session.commit()
        return categoria

    @staticmethod
    def deletar(categoria):
        db.session.delete(categoria)
        db.session.commit()
