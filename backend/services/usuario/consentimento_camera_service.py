from backend.models.usuario import Usuario


class ConsultarConsentimentoCameraService:
    """Caso de uso: informa se o usuário logado já aceitou o termo da câmera."""

    @staticmethod
    def execute(id_usuario):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado.")
        return bool(usuario.camera_autorizada)


class SalvarConsentimentoCameraService:
    """Caso de uso: grava no banco se o usuário logado aceitou (True) ou
    não (False) o termo da câmera, para não perguntar de novo."""

    @staticmethod
    def execute(id_usuario, autorizada):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado.")
        Usuario.atualizar(usuario, camera_autorizada=bool(autorizada))
        return bool(usuario.camera_autorizada)
