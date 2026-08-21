from backend.models.movimentacao import Movimentacao
from backend.models.movimentacao_item import MovimentacaoItem
from backend.models.movimentacao_lote import MovimentacaoLote
from backend.models.produto import Produto
from backend.models.lote import Lote


class RegistrarMovimentacaoService:
    """
    Caso de uso: registrar uma movimentação de estoque (Entrada, Saída ou
    Ajuste) junto com os itens/produtos envolvidos.

    `itens` é uma lista de dicts:
        [{"id_produto": 1, "quantidade": 2.5, "validade": date(...)}, ...]

    - Entrada: cria um lote novo com a validade informada. Se já existir um
      lote do mesmo produto com essa mesma validade, apenas soma a
      quantidade nele (não cria um lote duplicado).
    - Saída: quando a validade é informada, procura o lote daquele produto
      com exatamente essa validade e abate a quantidade dele. Quando a
      validade não é informada, abate seguindo FEFO (o lote que vence
      primeiro é consumido primeiro).
    """

    @staticmethod
    def execute(id_usuario, tipo, itens, observacao=None):
        if not itens:
            raise Exception("Informe ao menos um item para a movimentação.")

        movimentacao = Movimentacao.criar(id_usuario, tipo, observacao)

        for item in itens:
            id_produto = item.get('id_produto')
            quantidade = item.get('quantidade')
            validade = item.get('validade')

            if not id_produto:
                raise Exception("Informe o produto do item.")
            if quantidade is None or float(quantidade) <= 0:
                raise Exception("Informe uma quantidade válida.")
            if not Produto.buscar_por_id(id_produto):
                raise Exception(f"Produto {id_produto} não existe.")

            movimentacao_item = MovimentacaoItem.criar(movimentacao.id_movimentacao, id_produto, quantidade)

            if tipo == 'Entrada':
                RegistrarMovimentacaoService._registrar_entrada(movimentacao_item, id_produto, quantidade, validade)
            elif tipo == 'Saida':
                RegistrarMovimentacaoService._abater_estoque(movimentacao_item, id_produto, quantidade, validade)

        return movimentacao

    @staticmethod
    def _registrar_entrada(movimentacao_item, id_produto, quantidade, validade):
        if not validade:
            raise Exception("Informe a data de validade do lote de entrada.")

        quantidade = float(quantidade)
        lote_existente = Lote.query.filter_by(id_produto=id_produto, validade=validade).first()

        if lote_existente:
            # Já existe um lote desse produto com a mesma validade: só soma a quantidade.
            nova_quantidade_atual = float(lote_existente.quantidade_atual) + quantidade
            nova_quantidade_inicial = float(lote_existente.quantidade_inicial) + quantidade
            lote_afetado = Lote.atualizar(
                lote_existente,
                quantidade_atual=nova_quantidade_atual,
                quantidade_inicial=nova_quantidade_inicial,
            )
        else:
            # Não existe lote com essa validade ainda: cria um novo.
            lote_afetado = Lote.criar(
                id_produto=id_produto,
                validade=validade,
                quantidade_inicial=quantidade,
            )

        MovimentacaoLote.criar(movimentacao_item.id_movimentacao_item, lote_afetado.id_lote, quantidade)

    @staticmethod
    def _abater_estoque(movimentacao_item, id_produto, quantidade_a_baixar, validade=None):
        restante = float(quantidade_a_baixar)

        if validade:
            lote = Lote.query.filter_by(id_produto=id_produto, validade=validade).first()
            if not lote:
                raise Exception("Não existe lote desse produto com a validade informada.")
            if float(lote.quantidade_atual) < restante:
                raise Exception("Quantidade em estoque insuficiente nesse lote para dar baixa.")

            Lote.atualizar(lote, quantidade_atual=float(lote.quantidade_atual) - restante)
            MovimentacaoLote.criar(movimentacao_item.id_movimentacao_item, lote.id_lote, restante)
            return

        # Sem validade informada: abate seguindo FEFO (lote que vence primeiro sai primeiro).
        lotes = sorted(Lote.listar_por_produto(id_produto), key=lambda lote: lote.validade)

        for lote in lotes:
            if restante <= 0:
                break
            disponivel = float(lote.quantidade_atual)
            if disponivel <= 0:
                continue
            baixa = min(disponivel, restante)
            Lote.atualizar(lote, quantidade_atual=disponivel - baixa)
            MovimentacaoLote.criar(movimentacao_item.id_movimentacao_item, lote.id_lote, baixa)
            restante -= baixa

        if restante > 0:
            raise Exception("Quantidade em estoque insuficiente para esse produto.")
