from backend.models.categoria import Categoria


class CriarCategoriaService:
    """Caso de uso: cadastrar uma nova categoria de produto."""

    @staticmethod
    def execute(nome, descricao=None):
        return Categoria.criar(nome, descricao)
