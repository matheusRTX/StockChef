from backend.models.lote import Lote


class RemoverLoteService:
    """Caso de uso: remover um lote do estoque."""

    @staticmethod
    def execute(id_lote):
        lote = Lote.buscar_por_id(id_lote)
        if not lote:
            raise Exception("Lote não encontrado.")
        Lote.deletar(lote)
        return lote
