from backend.models.prato import Prato
from backend.models.prato_ingrediente import PratoIngrediente
from backend.services.prato.verificar_disponibilidade_service import VerificarDisponibilidadeService
from backend.services.movimentacao.registrar_movimentacao_service import RegistrarMovimentacaoService


class PrepararPratoService:
    """
    Caso de uso: preparar um prato, abatendo do estoque a quantidade de
    cada ingrediente. A baixa é feita dando prioridade aos lotes que
    vencem primeiro (FEFO), reaproveitando a mesma lógica usada pelas
    movimentações de saída manuais.
    """

    @staticmethod
    def execute(id_prato, id_usuario):
        prato = Prato.buscar_por_id(id_prato)
        if not prato:
            raise Exception("Prato não encontrado.")

        disponibilidade = VerificarDisponibilidadeService.execute(id_prato)
        if not disponibilidade["disponivel"]:
            raise Exception("Estoque insuficiente para preparar este prato.")

        ingredientes = PratoIngrediente.listar_por_prato(id_prato)
        itens = [
            {"id_produto": ingrediente.id_produto, "quantidade": float(ingrediente.quantidade)}
            for ingrediente in ingredientes
        ]

        movimentacao = RegistrarMovimentacaoService.execute(
            id_usuario=id_usuario,
            tipo='Saida',
            itens=itens,
            observacao=f"Preparo do prato: {prato.nome}",
        )

        return movimentacao
