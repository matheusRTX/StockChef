import random
import string

from backend.models.usuario import Usuario
from werkzeug.security import generate_password_hash


class CadastrarUsuarioService:
    """Caso de uso: cadastrar um novo usuário no StockChef.

    - Administrador: recebe automaticamente um `codigo_estabelecimento`
      único e entra com status 'Aprovado' (não depende de aprovação de
      ninguém).
    - Funcionario: precisa informar o `codigo_estabelecimento` do
      estabelecimento ao qual quer se vincular. O cadastro entra com
      status 'Pendente' e só passa a ser 'Aprovado' quando o
      Administrador daquele estabelecimento aprovar.
    """

    TAMANHO_CODIGO = 6
    CARACTERES_CODIGO = string.ascii_uppercase + string.digits

    @staticmethod
    def execute(nome, email, senha, tipo, codigo_estabelecimento=None):
        if not nome or not nome.strip():
            raise Exception("Informe o nome completo.")
        if not email or not email.strip():
            raise Exception("Informe o e-mail.")
        if not senha:
            raise Exception("Informe a senha.")
        if tipo not in ('Administrador', 'Funcionario'):
            raise Exception("Tipo de usuário inválido.")

        if Usuario.buscar_por_email(email):
            raise Exception("Este e-mail já está cadastrado no StockChef.")

        senha_hash = generate_password_hash(senha)

        if tipo == 'Administrador':
            codigo_gerado = CadastrarUsuarioService._gerar_codigo_estabelecimento()
            return Usuario.criar(
                nome=nome.strip(),
                email=email.strip(),
                senha_hash=senha_hash,
                tipo=tipo,
                codigo_estabelecimento=codigo_gerado,
                id_estabelecimento=None,
                status='Aprovado',
            )

        # Funcionario: precisa vincular a um estabelecimento existente.
        codigo_estabelecimento = (codigo_estabelecimento or '').strip().upper()
        if not codigo_estabelecimento:
            raise Exception("Informe o código do estabelecimento fornecido pelo seu administrador.")

        administrador = Usuario.buscar_por_codigo_estabelecimento(codigo_estabelecimento)
        if not administrador:
            raise Exception("Código de estabelecimento inválido. Confira com o seu administrador.")

        return Usuario.criar(
            nome=nome.strip(),
            email=email.strip(),
            senha_hash=senha_hash,
            tipo=tipo,
            codigo_estabelecimento=None,
            id_estabelecimento=administrador.id_usuario,
            status='Pendente',
        )

    @staticmethod
    def _gerar_codigo_estabelecimento():
        for _ in range(20):
            codigo = ''.join(
                random.choices(CadastrarUsuarioService.CARACTERES_CODIGO,
                                k=CadastrarUsuarioService.TAMANHO_CODIGO)
            )
            if not Usuario.buscar_por_codigo_estabelecimento(codigo):
                return codigo
        raise Exception("Não foi possível gerar um código de estabelecimento único. Tente novamente.")
