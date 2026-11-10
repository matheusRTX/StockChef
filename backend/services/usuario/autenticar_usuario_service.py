from backend.models.usuario import Usuario
from werkzeug.security import check_password_hash


class ContaNaoAprovadaException(Exception):
    pass


class AutenticarUsuarioService:

    @staticmethod
    def execute(email, senha):
        usuario = Usuario.buscar_por_email(email)
        if not usuario or not usuario.ativo or not check_password_hash(usuario.senha, senha):
            return None

        if usuario.tipo == 'Funcionario' and usuario.status != 'Aprovado':
            raise ContaNaoAprovadaException(
                "Sua senha está correta, mas o seu cadastro ainda está "
                f"'{usuario.status}'. Aguarde a aprovação do administrador "
                "do seu estabelecimento para acessar o sistema."
            )

        return usuario
