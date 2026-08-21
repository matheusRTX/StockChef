from backend.models.usuario import Usuario
from werkzeug.security import check_password_hash


class AutenticarUsuarioService:
    """Caso de uso: autenticar (login) um usuário existente."""

    @staticmethod
    def execute(email, senha):
        usuario = Usuario.buscar_por_email(email)
        if usuario and usuario.ativo and check_password_hash(usuario.senha, senha):
            return usuario
        return None
