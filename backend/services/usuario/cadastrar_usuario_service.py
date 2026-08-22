from backend.models.usuario import Usuario
from werkzeug.security import generate_password_hash


class CadastrarUsuarioService:
    """Caso de uso: cadastrar um novo usuário no StockChef."""

    @staticmethod
    def execute(nome, email, senha, tipo):
        if Usuario.buscar_por_email(email):
            raise Exception("Este e-mail já está cadastrado no StockChef.")

        senha_hash = generate_password_hash(senha)
        return Usuario.criar(nome, email, senha_hash, tipo)
