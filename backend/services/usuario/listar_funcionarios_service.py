from backend.models.usuario import Usuario


class ListarFuncionariosService:

    @staticmethod
    def execute(id_estabelecimento):
        return Usuario.listar_funcionarios_do_estabelecimento(id_estabelecimento)
