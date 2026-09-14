from backend.models.prato import Prato
from backend.models.prato_ingrediente import PratoIngrediente
from backend.models.produto import Produto
from backend.models.unidade_medida import UnidadeMedida
from backend.models.lote import Lote


class VerificarDisponibilidadeService:
    """
    Caso de uso: verificar se o estoque atual dá conta de todos os
    ingredientes de um prato, comparando a quantidade necessária de cada
    ingrediente com a soma dos lotes disponíveis do produto correspondente.
    """

    @staticmethod
    def execute(id_prato):
        prato = Prato.buscar_por_id(id_prato)
        if not prato:
            raise Exception("Prato não encontrado.")

        ingredientes = PratoIngrediente.listar_por_prato(id_prato)
        if not ingredientes:
            raise Exception("Este prato ainda não possui ingredientes cadastrados.")

        itens = []
        disponivel_geral = True

        for ingrediente in ingredientes:
            produto = Produto.buscar_por_id(ingrediente.id_produto)
            unidade = UnidadeMedida.buscar_por_id(produto.id_unidade) if produto else None

            quantidade_necessaria = float(ingrediente.quantidade)
            quantidade_disponivel = sum(
                float(lote.quantidade_atual) for lote in Lote.listar_por_produto(ingrediente.id_produto)
            )

            suficiente = quantidade_disponivel >= quantidade_necessaria
            if not suficiente:
                disponivel_geral = False

            itens.append({
                "id_produto": ingrediente.id_produto,
                "produto": produto.nome if produto else "Produto removido",
                "unidade": unidade.sigla if unidade else "",
                "quantidade_necessaria": quantidade_necessaria,
                "quantidade_disponivel": quantidade_disponivel,
                "quantidade_faltante": max(0.0, quantidade_necessaria - quantidade_disponivel),
                "suficiente": suficiente,
            })

        return {
            "id_prato": prato.id_prato,
            "nome": prato.nome,
            "disponivel": disponivel_geral,
            "itens": itens,
        }
