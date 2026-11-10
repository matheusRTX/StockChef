from backend.models.categoria import Categoria


class BuscarCategoriaService:

    @staticmethod
    def execute(id_categoria):
        categoria = Categoria.buscar_por_id(id_categoria)
        if not categoria:
            raise Exception("Categoria não encontrada.")
        return categoria
