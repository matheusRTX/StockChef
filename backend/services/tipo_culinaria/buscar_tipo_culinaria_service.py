from backend.models.tipo_culinaria import TipoCulinaria


class BuscarTipoCulinariaService:
    """Caso de uso: buscar um tipo de culinária pelo id."""

    @staticmethod
    def execute(id_tipo_culinaria):
        tipo = TipoCulinaria.buscar_por_id(id_tipo_culinaria)
        if not tipo:
            raise Exception("Tipo de culinária não encontrado.")
        return tipo
