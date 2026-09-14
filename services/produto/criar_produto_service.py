from backend.models.produto import Produto
from backend.models.categoria import Categoria
from backend.models.unidade_medida import UnidadeMedida


class CriarProdutoService:
    """Caso de uso: cadastrar um novo produto no estoque."""

    @staticmethod
    def execute(id_usuario, nome, id_categoria, id_unidade, descricao=None,
                codigo_barras=None, qr_code=None, estoque_minimo=0, imagem=None):
        if not Categoria.buscar_por_id(id_categoria):
            raise Exception("Categoria informada não existe.")
        if not UnidadeMedida.buscar_por_id(id_unidade):
            raise Exception("Unidade de medida informada não existe.")

        return Produto.criar(
            id_usuario=id_usuario,
            nome=nome,
            id_categoria=id_categoria,
            id_unidade=id_unidade,
            descricao=descricao,
            codigo_barras=codigo_barras,
            qr_code=qr_code,
            estoque_minimo=estoque_minimo,
            imagem=imagem,
        )
