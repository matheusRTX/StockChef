from backend.models.unidade_medida import UnidadeMedida


class RemoverUnidadeMedidaService:
    """Caso de uso: remover uma unidade de medida."""

    @staticmethod
    def execute(id_unidade):
        unidade = UnidadeMedida.buscar_por_id(id_unidade)
        if not unidade:
            raise Exception("Unidade de medida não encontrada.")
        UnidadeMedida.deletar(unidade)
        return unidade
