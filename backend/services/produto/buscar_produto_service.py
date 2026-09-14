from backend.models.produto import Produto


class BuscarProdutoService:
    """Caso de uso: buscar um produto específico pelo id."""

    @staticmethod
    def execute(id_produto):
        produto = Produto.buscar_por_id(id_produto)
        if not produto:
            raise Exception("Produto não encontrado.")
        return produto
