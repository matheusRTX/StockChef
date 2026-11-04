from backend.models.usuario import Usuario


class ListarUsuariosService:
    """Caso de uso: listar todos os usuários ativos."""

    @staticmethod
    def execute():
        return Usuario.listar_todos()
