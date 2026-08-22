from backend.models.prato import Prato


class ListarPratosService:
    """Caso de uso: listar pratos ativos (todos, por usuário ou favoritos)."""

    @staticmethod
    def execute(id_usuario=None, apenas_favoritos=False):
        if apenas_favoritos:
            return Prato.listar_favoritos()
        if id_usuario:
            return Prato.listar_por_usuario(id_usuario)
        return Prato.listar_todos()
