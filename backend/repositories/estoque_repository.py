from sqlalchemy import text
from backend.models.usuario import db


class EstoqueRepository:
    """Executa a procedure de estoque detalhado e agrupa os lotes por produto."""

    @staticmethod
    def listar_estoque(id_usuario):
        """
        Executa sp_listar_estoque_detalhado (uma linha por lote) e agrupa
        o resultado em uma lista de produtos, cada um com sua lista de lotes.
        """
        resultado = db.session.execute(
            text("CALL sp_listar_estoque_detalhado(:id)"),
            {"id": id_usuario}
        ).mappings().all()

        db.session.commit()

        produtos_por_id = {}
        ordem = []

        for linha in resultado:
            id_produto = linha["id_produto"]

            if id_produto not in produtos_por_id:
                produtos_por_id[id_produto] = {
                    "id_produto": id_produto,
                    "produto": linha["produto"],
                    "categoria": linha["categoria"],
                    "unidade": linha["unidade"],
                    "valor_minimo": float(linha["valor_minimo"]) if linha["valor_minimo"] is not None else 0,
                    "quantidade_total": 0,
                    "lotes": [],
                }
                ordem.append(id_produto)

            # Produtos sem nenhum lote vêm com id_lote NULL (LEFT JOIN)
            if linha["id_lote"] is not None:
                quantidade = float(linha["quantidade_atual"]) if linha["quantidade_atual"] is not None else 0
                produtos_por_id[id_produto]["quantidade_total"] += quantidade
                produtos_por_id[id_produto]["lotes"].append({
                    "id_lote": linha["id_lote"],
                    "numero_lote": linha["numero_lote"],
                    "quantidade_atual": quantidade,
                    "validade": linha["validade"].isoformat() if linha["validade"] else None,
                })

        return [produtos_por_id[id_produto] for id_produto in ordem]
