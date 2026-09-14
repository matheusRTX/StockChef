from backend.models.fornecedor import Fornecedor


class CriarFornecedorService:
    """Caso de uso: cadastrar um novo fornecedor."""

    @staticmethod
    def execute(id_usuario, nome, telefone=None, email=None, id_categoria=None):
        if not nome or not nome.strip():
            raise Exception("Informe o nome do fornecedor.")

        fornecedor = Fornecedor.criar(
            id_usuario=id_usuario,
            nome=nome.strip(),
            telefone=telefone,
            email=email,
        )

        if id_categoria:
            Fornecedor.definir_categoria(fornecedor.id_fornecedor, id_categoria)

        categoria = Fornecedor.buscar_categoria(fornecedor.id_fornecedor)
        return fornecedor, categoria
