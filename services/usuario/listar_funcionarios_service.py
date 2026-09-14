from backend.models.usuario import Usuario


class ListarFuncionariosService:
    """Caso de uso: o Administrador lista todos os funcionários (pendentes,
    aprovados ou recusados) vinculados ao estabelecimento dele."""

    @staticmethod
    def execute(id_estabelecimento):
        return Usuario.listar_funcionarios_do_estabelecimento(id_estabelecimento)
