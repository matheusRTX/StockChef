from backend.models.usuario import Usuario
from werkzeug.security import generate_password_hash


class AtualizarUsuarioService:
    """Caso de uso: atualizar os dados de um usuário existente."""

    @staticmethod
    def execute(id_usuario, **campos):
        usuario = Usuario.buscar_por_id(id_usuario)
        if not usuario:
            raise Exception("Usuário não encontrado.")

        novo_email = campos.get('email')
        if novo_email and novo_email != usuario.email and Usuario.buscar_por_email(novo_email):
            raise Exception("Este e-mail já está cadastrado no StockChef.")

        if 'senha' in campos and campos['senha']:
            campos['senha'] = generate_password_hash(campos['senha'])
        else:
            campos.pop('senha', None)

        return Usuario.atualizar(usuario, **campos)
