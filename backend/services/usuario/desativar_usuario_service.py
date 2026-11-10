from backend.models.usuario import Usuario


class DesativarUsuarioService:

    @staticmethod
    def execute(id_usuario):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado.")
        Usuario.deletar(usuario)
        return usuario
