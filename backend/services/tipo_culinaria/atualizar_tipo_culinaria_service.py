from backend.models.tipo_culinaria import TipoCulinaria


class AtualizarTipoCulinariaService:
    """Caso de uso: atualizar os dados de um tipo de culinária existente."""

    @staticmethod
    def execute(id_tipo_culinaria, **campos):
        tipo = TipoCulinaria.buscar_por_id(id_tipo_culinaria)
        if not tipo:
            raise Exception("Tipo de culinária não encontrado.")
        return TipoCulinaria.atualizar(tipo, **campos)
