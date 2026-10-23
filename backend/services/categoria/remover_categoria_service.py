from backend.models.categoria import Categoria


class RemoverCategoriaService:
    """Caso de uso: remover uma categoria."""

    @staticmethod
    def execute(id_categoria):
        categoria = Categoria.buscar_por_id(id_categoria)
        if not categoria:
            raise Exception("Categoria não encontrada.")
        Categoria.deletar(categoria)
        return categoria
