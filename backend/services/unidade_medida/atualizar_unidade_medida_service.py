from backend.models.unidade_medida import UnidadeMedida


class AtualizarUnidadeMedidaService:
    """Caso de uso: atualizar os dados de uma unidade de medida existente."""

    @staticmethod
    def execute(id_unidade, **campos):
        unidade = UnidadeMedida.buscar_por_id(id_unidade)
        if not unidade:
            raise Exception("Unidade de medida não encontrada.")
        return UnidadeMedida.atualizar(unidade, **campos)
