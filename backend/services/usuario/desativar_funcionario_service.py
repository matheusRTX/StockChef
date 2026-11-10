from backend.models.usuario import Usuario


class DesativarFuncionarioService:
    """Caso de uso: o Administrador inativa (soft delete) um Funcionario
    do seu próprio estabelecimento."""

    @staticmethod
    def execute(id_estabelecimento, id_usuario_funcionario):
        funcionario = Usuario.buscar_por_id(id_usuario_funcionario)

        if not funcionario or funcionario.tipo != 'Funcionario':
            raise Exception("Funcionário não encontrado.")
        if funcionario.id_estabelecimento != id_estabelecimento:
            raise Exception("Este funcionário não pertence ao seu estabelecimento.")

        Usuario.deletar(funcionario)
        return funcionario
