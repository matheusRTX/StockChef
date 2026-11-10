from backend.models.lote import Lote


class ListarLotesService:

    @staticmethod
    def execute(id_produto=None):
        if id_produto:
            return Lote.listar_por_produto(id_produto)
        return Lote.listar_todos()
