from backend.models.usuario import Usuario


class ConsultarConsentimentoCameraService:

    @staticmethod
    def execute(id_usuario):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado.")
        return bool(usuario.camera_autorizada)


class SalvarConsentimentoCameraService:

    @staticmethod
    def execute(id_usuario, autorizada):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado.")
        Usuario.atualizar(usuario, camera_autorizada=bool(autorizada))
        return bool(usuario.camera_autorizada)
