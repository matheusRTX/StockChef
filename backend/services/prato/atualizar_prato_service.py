from backend.models.prato import Prato


class AtualizarPratoService:
    """Caso de uso: atualizar os dados de um prato existente."""

    @staticmethod
    def execute(id_prato, **campos):
        prato = Prato.buscar_por_id(id_prato)
        if not prato:
            raise Exception("Prato não encontrado.")
        return Prato.atualizar(prato, **campos)
