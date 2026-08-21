from backend.models.prato import Prato


class RemoverPratoService:
    """Caso de uso: remover (soft delete) um prato do cardápio."""

    @staticmethod
    def execute(id_prato):
        prato = Prato.buscar_por_id(id_prato)
        if not prato:
            raise Exception("Prato não encontrado.")
        Prato.deletar(prato)
        return prato
