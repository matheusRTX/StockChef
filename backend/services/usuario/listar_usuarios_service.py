from backend.models.usuario import Usuario


class ListarUsuariosService:

    @staticmethod
    def execute():
        return Usuario.listar_todos()
