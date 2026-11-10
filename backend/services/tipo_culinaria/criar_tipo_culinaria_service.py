from backend.models.tipo_culinaria import TipoCulinaria


class CriarTipoCulinariaService:

    @staticmethod
    def execute(nome, descricao=None):
        return TipoCulinaria.criar(nome, descricao)
