from backend.models.categoria import Categoria


class ListarCategoriasService:
    """Caso de uso: listar todas as categorias."""

    @staticmethod
    def execute():
        return Categoria.listar_todos()
