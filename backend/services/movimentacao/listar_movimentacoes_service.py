from backend.models.movimentacao import Movimentacao


class ListarMovimentacoesService:

    @staticmethod
    def execute(id_usuario=None):
        if id_usuario:
            return Movimentacao.listar_por_usuario(id_usuario)
        return Movimentacao.listar_todos()
