from backend.models.prato_ingrediente import PratoIngrediente


class RemoverIngredienteService:
    """Caso de uso: remover um ingrediente de um prato."""

    @staticmethod
    def execute(id_prato_ingrediente):
        ingrediente = PratoIngrediente.buscar_por_id(id_prato_ingrediente)
        if not ingrediente:
            raise Exception("Ingrediente não encontrado.")
        PratoIngrediente.deletar(ingrediente)
        return ingrediente
