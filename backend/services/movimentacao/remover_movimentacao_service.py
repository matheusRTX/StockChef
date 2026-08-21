from backend.models.movimentacao import Movimentacao


class RemoverMovimentacaoService:
    """Caso de uso: remover uma movimentação (e seus itens, via CASCADE)."""

    @staticmethod
    def execute(id_movimentacao):
        movimentacao = Movimentacao.buscar_por_id(id_movimentacao)
        if not movimentacao:
            raise Exception("Movimentação não encontrada.")
        Movimentacao.deletar(movimentacao)
        return movimentacao
