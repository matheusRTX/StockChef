from backend.models.lote import Lote


class AtualizarLoteService:
    """Caso de uso: atualizar os dados de um lote existente."""

    @staticmethod
    def execute(id_lote, **campos):
        lote = Lote.buscar_por_id(id_lote)
        if not lote:
            raise Exception("Lote não encontrado.")
        return Lote.atualizar(lote, **campos)
