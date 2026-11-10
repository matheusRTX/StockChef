from backend.models.tipo_culinaria import TipoCulinaria


class ListarTiposCulinariaService:

    @staticmethod
    def execute():
        return TipoCulinaria.listar_todos()
