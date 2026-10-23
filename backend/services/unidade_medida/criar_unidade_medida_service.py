from backend.models.unidade_medida import UnidadeMedida


class CriarUnidadeMedidaService:
    """Caso de uso: cadastrar uma nova unidade de medida."""

    @staticmethod
    def execute(sigla, descricao):
        return UnidadeMedida.criar(sigla, descricao)
