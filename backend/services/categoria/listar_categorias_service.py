from backend.models.categoria import Categoria


class ListarCategoriasService:

    @staticmethod
    def execute():
        return Categoria.listar_todos()
