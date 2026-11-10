from backend.models.movimentacao import Movimentacao


class AtualizarMovimentacaoService:
    """Caso de uso: atualizar dados (ex: observação) de uma movimentação."""

    @staticmethod
    def execute(id_movimentacao, **campos):
        movimentacao = Movimentacao.buscar_por_id(id_movimentacao)
        if not movimentacao:
            raise Exception("Movimentação não encontrada.")
        return Movimentacao.atualizar(movimentacao, **campos)
