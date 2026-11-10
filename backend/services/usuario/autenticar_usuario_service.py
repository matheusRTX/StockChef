from backend.models.usuario import Usuario
from werkzeug.security import check_password_hash


class ContaNaoAprovadaException(Exception):
    """Levantada quando a senha está correta, mas a conta do Funcionario
    ainda não foi aprovada (ou foi recusada) pelo Administrador do
    estabelecimento."""
    pass


class AutenticarUsuarioService:
    """Caso de uso: autenticar (login) um usuário existente.

    Regras:
    - E-mail/senha inválidos ou conta desativada -> retorna None
      (credenciais inválidas).
    - Funcionario com status diferente de 'Aprovado' -> levanta
      ContaNaoAprovadaException (a senha está certa, mas o acesso ainda
      não é permitido).
    """

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
