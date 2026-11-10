from backend.models.prato import Prato
from backend.models.prato_ingrediente import PratoIngrediente


class BuscarPratoService:

    @staticmethod
    def execute(id_prato):
        prato = Prato.buscar_por_id(id_prato)
        if not prato:
            raise Exception("Prato não encontrado.")
        ingredientes = PratoIngrediente.listar_por_prato(id_prato)
        return prato, ingredientes
