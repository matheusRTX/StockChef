from backend.models.produto import Produto


class ListarProdutosService:
    """Caso de uso: listar produtos ativos (opcionalmente por usuário)."""

    @staticmethod
    def execute(id_usuario=None):
        if id_usuario:
            return Produto.listar_por_usuario(id_usuario)
        return Produto.listar_todos()
