from backend.models.unidade_medida import UnidadeMedida


class ListarUnidadesMedidaService:

    @staticmethod
    def execute():
        return UnidadeMedida.listar_todos()
