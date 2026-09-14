from backend.models.fornecedor import Fornecedor


class RemoverFornecedorService:
    """Caso de uso: remover um fornecedor."""

    @staticmethod
    def execute(id_fornecedor, id_usuario):
        fornecedor = Fornecedor.buscar_por_id(id_fornecedor)
        if not fornecedor or fornecedor.id_usuario != id_usuario:
            raise Exception("Fornecedor não encontrado.")
        Fornecedor.deletar(fornecedor)
        return fornecedor
