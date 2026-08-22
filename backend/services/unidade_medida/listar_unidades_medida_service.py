from backend.models.unidade_medida import UnidadeMedida


class ListarUnidadesMedidaService:
    """Caso de uso: listar todas as unidades de medida."""

    @staticmethod
    def execute():
        return UnidadeMedida.listar_todos()
