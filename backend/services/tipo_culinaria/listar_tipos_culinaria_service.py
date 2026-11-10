from backend.models.tipo_culinaria import TipoCulinaria


class ListarTiposCulinariaService:
    """Caso de uso: listar todos os tipos de culinária."""

    @staticmethod
    def execute():
        return TipoCulinaria.listar_todos()
