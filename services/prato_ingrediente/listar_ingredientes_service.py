from backend.models.prato_ingrediente import PratoIngrediente


class ListarIngredientesService:
    """Caso de uso: listar os ingredientes de um prato."""

    @staticmethod
    def execute(id_prato):
        return PratoIngrediente.listar_por_prato(id_prato)
