from backend.models.produto import Produto


class RemoverProdutoService:
    """Caso de uso: remover (soft delete) um produto do estoque."""

    @staticmethod
    def execute(id_produto):
        produto = Produto.buscar_por_id(id_produto)
        if not produto:
            raise Exception("Produto não encontrado.")
        Produto.deletar(produto)
        return produto
