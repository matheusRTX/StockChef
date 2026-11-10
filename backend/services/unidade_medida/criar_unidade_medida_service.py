from backend.models.unidade_medida import UnidadeMedida


class CriarUnidadeMedidaService:

    @staticmethod
    def execute(sigla, descricao):
        return UnidadeMedida.criar(sigla, descricao)
