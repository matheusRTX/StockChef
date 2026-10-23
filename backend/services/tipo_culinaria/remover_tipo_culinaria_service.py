from backend.models.tipo_culinaria import TipoCulinaria


class RemoverTipoCulinariaService:
    """Caso de uso: remover um tipo de culinária."""

    @staticmethod
    def execute(id_tipo_culinaria):
        tipo = TipoCulinaria.buscar_por_id(id_tipo_culinaria)
        if not tipo:
            raise Exception("Tipo de culinária não encontrado.")
        TipoCulinaria.deletar(tipo)
        return tipo
