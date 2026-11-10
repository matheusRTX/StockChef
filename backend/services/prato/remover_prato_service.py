from backend.models.prato import Prato


class RemoverPratoService:

    @staticmethod
    def execute(id_prato):
        prato = Prato.buscar_por_id(id_prato)
        if not prato:
            raise Exception("Prato não encontrado.")
        Prato.deletar(prato)
        return prato
