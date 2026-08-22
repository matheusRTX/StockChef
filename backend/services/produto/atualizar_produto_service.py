from backend.models.produto import Produto


class AtualizarProdutoService:
    """Caso de uso: atualizar os dados de um produto existente."""

    @staticmethod
    def execute(id_produto, **campos):
        produto = Produto.buscar_por_id(id_produto)
        if not produto:
            raise Exception("Produto não encontrado.")
        return Produto.atualizar(produto, **campos)
