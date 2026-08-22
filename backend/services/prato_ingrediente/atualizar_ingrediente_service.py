from backend.models.prato_ingrediente import PratoIngrediente


class AtualizarIngredienteService:
    """Caso de uso: atualizar a quantidade/observação de um ingrediente."""

    @staticmethod
    def execute(id_prato_ingrediente, **campos):
        ingrediente = PratoIngrediente.buscar_por_id(id_prato_ingrediente)
        if not ingrediente:
            raise Exception("Ingrediente não encontrado.")
        return PratoIngrediente.atualizar(ingrediente, **campos)
