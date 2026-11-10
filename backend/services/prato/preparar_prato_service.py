from backend.models.prato import Prato
from backend.models.prato_ingrediente import PratoIngrediente
from backend.services.prato.verificar_disponibilidade_service import VerificarDisponibilidadeService
from backend.services.movimentacao.registrar_movimentacao_service import RegistrarMovimentacaoService


class PrepararPratoService:

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
