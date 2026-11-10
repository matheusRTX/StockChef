from backend.models.movimentacao import Movimentacao


class AtualizarMovimentacaoService:

    @staticmethod
    def execute(id_movimentacao, **campos):
        movimentacao = Movimentacao.buscar_por_id(id_movimentacao)
        if not movimentacao:
            raise Exception("Movimentação não encontrada.")
        return Movimentacao.atualizar(movimentacao, **campos)
