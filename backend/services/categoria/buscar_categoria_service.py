from backend.models.categoria import Categoria


class BuscarCategoriaService:
    """Caso de uso: buscar uma categoria específica pelo id."""

    @staticmethod
    def execute(id_categoria):
        categoria = Categoria.buscar_por_id(id_categoria)
        if not categoria:
            raise Exception("Categoria não encontrada.")
        return categoria
