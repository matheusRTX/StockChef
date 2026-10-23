from backend.models.fornecedor import Fornecedor


class AtualizarFornecedorService:
    """Caso de uso: atualizar os dados de um fornecedor existente."""

    @staticmethod
    def execute(id_fornecedor, id_usuario, nome=None, telefone=None, email=None, id_categoria=None):
        fornecedor = Fornecedor.buscar_por_id(id_fornecedor)
        if not fornecedor or fornecedor.id_usuario != id_usuario:
            raise Exception("Fornecedor não encontrado.")

        campos = {}
        if nome is not None:
            if not nome.strip():
                raise Exception("Informe o nome do fornecedor.")
            campos['nome'] = nome.strip()
        if telefone is not None:
            campos['telefone'] = telefone
        if email is not None:
            campos['email'] = email

        Fornecedor.atualizar(fornecedor, **campos)
        Fornecedor.definir_categoria(fornecedor.id_fornecedor, id_categoria)

        categoria = Fornecedor.buscar_categoria(fornecedor.id_fornecedor)
        return fornecedor, categoria
