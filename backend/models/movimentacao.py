from datetime import datetime
from backend.models.usuario import db


class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'

    id_movimentacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo = db.Column(db.Enum('Entrada', 'Saida', 'Ajuste'), nullable=False)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    observacao = db.Column(db.Text)

    # ---------------------- CRUD ----------------------

    @staticmethod
    def criar(id_usuario, tipo, observacao=None):
        nova = Movimentacao(id_usuario=id_usuario, tipo=tipo, observacao=observacao)
        db.session.add(nova)
        db.session.commit()
        return nova

    @staticmethod
    def buscar_por_id(id_movimentacao):
        return Movimentacao.query.get(id_movimentacao)

    @staticmethod
    def listar_todos():
        return Movimentacao.query.order_by(Movimentacao.data_movimentacao.desc()).all()

    @staticmethod
    def listar_por_usuario(id_usuario):
        return Movimentacao.query.filter_by(id_usuario=id_usuario).order_by(Movimentacao.data_movimentacao.desc()).all()

    @staticmethod
    def atualizar(movimentacao, **campos):
        for campo, valor in campos.items():
            setattr(movimentacao, campo, valor)
        db.session.commit()
        return movimentacao

    @staticmethod
    def deletar(movimentacao):
        db.session.delete(movimentacao)
        db.session.commit()
