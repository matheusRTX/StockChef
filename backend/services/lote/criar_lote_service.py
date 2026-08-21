from backend.models.lote import Lote
from backend.models.produto import Produto


class CriarLoteService:
    """Caso de uso: cadastrar um novo lote de um produto."""

    @staticmethod
    def execute(id_produto, validade, quantidade_inicial, numero_lote=None,
                custo_unitario=None, observacao=None):
        if not Produto.buscar_por_id(id_produto):
            raise Exception("Produto informado não existe.")

        return Lote.criar(
            id_produto=id_produto,
            validade=validade,
            quantidade_inicial=quantidade_inicial,
            numero_lote=numero_lote,
            custo_unitario=custo_unitario,
            observacao=observacao,
        )
