from backend.models.movimentacao import Movimentacao


class RemoverMovimentacaoService:

    @staticmethod
    def execute(id_movimentacao):
        movimentacao = Movimentacao.buscar_por_id(id_movimentacao)
        if not movimentacao:
            raise Exception("Movimentação não encontrada.")
        Movimentacao.deletar(movimentacao)
        return movimentacao
