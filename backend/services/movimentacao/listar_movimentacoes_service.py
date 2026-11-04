from backend.models.movimentacao import Movimentacao


class ListarMovimentacoesService:
    """Caso de uso: listar movimentações (opcionalmente por usuário)."""

    @staticmethod
    def execute(id_usuario=None):
        if id_usuario:
            return Movimentacao.listar_por_usuario(id_usuario)
        return Movimentacao.listar_todos()
