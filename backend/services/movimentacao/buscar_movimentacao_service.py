from backend.models.movimentacao import Movimentacao
from backend.models.movimentacao_item import MovimentacaoItem


class BuscarMovimentacaoService:
    """Caso de uso: buscar uma movimentação e seus itens pelo id."""

    @staticmethod
    def execute(id_movimentacao):
        movimentacao = Movimentacao.buscar_por_id(id_movimentacao)
        if not movimentacao:
            raise Exception("Movimentação não encontrada.")
        itens = MovimentacaoItem.listar_por_movimentacao(id_movimentacao)
        return movimentacao, itens
