from backend.models.categoria import Categoria


class AtualizarCategoriaService:

    @staticmethod
    def execute(id_categoria, **campos):
        categoria = Categoria.buscar_por_id(id_categoria)
        if not categoria:
            raise Exception("Categoria não encontrada.")
        return Categoria.atualizar(categoria, **campos)
