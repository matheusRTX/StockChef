from backend.models.fornecedor import Fornecedor


class ListarFornecedoresService:

    @staticmethod
    def execute(id_usuario):
        fornecedores = Fornecedor.listar_por_usuario(id_usuario)
        return [(f, Fornecedor.buscar_categoria(f.id_fornecedor)) for f in fornecedores]
