from backend.models.prato_ingrediente import PratoIngrediente
from backend.models.prato import Prato
from backend.models.produto import Produto


class AdicionarIngredienteService:
    """Caso de uso: adicionar um ingrediente a um prato existente."""

    @staticmethod
    def execute(id_prato, id_produto, quantidade, observacao=None):
        if not Prato.buscar_por_id(id_prato):
            raise Exception("Prato informado não existe.")
        if not Produto.buscar_por_id(id_produto):
            raise Exception("Produto informado não existe.")

        return PratoIngrediente.criar(id_prato, id_produto, quantidade, observacao)
