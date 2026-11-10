from backend.models.categoria import Categoria


class CriarCategoriaService:

    @staticmethod
    def execute(nome, descricao=None):
        return Categoria.criar(nome, descricao)
