from backend.models.usuario import Usuario
from werkzeug.security import generate_password_hash

CAMPOS_PERMITIDOS = {'nome', 'email', 'senha', 'status', 'ativo'}
STATUS_VALIDOS = {'Pendente', 'Aprovado', 'Recusado'}


class AtualizarFuncionarioService:
    """Caso de uso: o Administrador edita os dados de um Funcionario do
    seu próprio estabelecimento (nome, e-mail, senha, status, ativo)."""

    @staticmethod
    def execute(id_estabelecimento, id_usuario_funcionario, **campos):
        funcionario = Usuario.buscar_por_id(id_usuario_funcionario)

        if not funcionario or funcionario.tipo != 'Funcionario':
            raise Exception("Funcionário não encontrado.")
        if funcionario.id_estabelecimento != id_estabelecimento:
            raise Exception("Este funcionário não pertence ao seu estabelecimento.")

        dados = {k: v for k, v in campos.items() if k in CAMPOS_PERMITIDOS and v not in (None, '')}

        if 'email' in dados and dados['email'] != funcionario.email:
            existente = Usuario.buscar_por_email(dados['email'])
            if existente and existente.id_usuario != funcionario.id_usuario:
                raise Exception("Este e-mail já está cadastrado no StockChef.")

        if 'senha' in dados:
            dados['senha'] = generate_password_hash(dados['senha'])

        if 'status' in dados and dados['status'] not in STATUS_VALIDOS:
            raise Exception("Status informado é inválido.")

        return Usuario.atualizar(funcionario, **dados)
