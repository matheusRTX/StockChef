from backend.models.produto import Produto


class ListarProdutosService:

    @staticmethod
    def execute(id_usuario=None):
        if id_usuario:
            return Produto.listar_por_usuario(id_usuario)
        return Produto.listar_todos()
