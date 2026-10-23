from backend.models.unidade_medida import UnidadeMedida


class BuscarUnidadeMedidaService:
    """Caso de uso: buscar uma unidade de medida específica pelo id."""

    @staticmethod
    def execute(id_unidade):
        unidade = UnidadeMedida.buscar_por_id(id_unidade)
        if not unidade:
            raise Exception("Unidade de medida não encontrada.")
        return unidade
