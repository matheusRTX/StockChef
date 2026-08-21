from backend.models.lote import Lote


class ListarLotesService:
    """Caso de uso: listar lotes (opcionalmente filtrando por produto)."""

    @staticmethod
    def execute(id_produto=None):
        if id_produto:
            return Lote.listar_por_produto(id_produto)
        return Lote.listar_todos()
