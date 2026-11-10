from backend.models.lote import Lote


class BuscarLoteService:

    @staticmethod
    def execute(id_lote):
        lote = Lote.buscar_por_id(id_lote)
        if not lote:
            raise Exception("Lote não encontrado.")
        return lote
