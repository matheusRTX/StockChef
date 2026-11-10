from backend.models.produto import Produto


class RemoverProdutoService:

    @staticmethod
    def execute(id_produto):
        produto = Produto.buscar_por_id(id_produto)
        if not produto:
            raise Exception("Produto não encontrado.")
        Produto.deletar(produto)
        return produto
