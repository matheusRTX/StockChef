from backend.models.tipo_culinaria import TipoCulinaria


class CriarTipoCulinariaService:
    """Caso de uso: cadastrar um novo tipo de culinária."""

    @staticmethod
    def execute(nome, descricao=None):
        return TipoCulinaria.criar(nome, descricao)
