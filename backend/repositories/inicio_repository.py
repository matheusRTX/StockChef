from sqlalchemy import text
from backend.models.usuario import db


class InicioRepository:
    """Executa as procedures do banco relacionadas ao módulo Início."""

    @staticmethod
    def get_resumo(id_usuario):
        """
        Executa sp_inicio_total_cadastrados, sp_inicio_total_estoque_baixo
        e sp_inicio_total_vencendo_7_dias para o usuário logado.
        """
        cadastrados = db.session.execute(
            text("CALL sp_inicio_total_cadastrados(:id)"),
            {"id": id_usuario}
        ).mappings().first()

        estoque_baixo = db.session.execute(
            text("CALL sp_inicio_total_estoque_baixo(:id)"),
            {"id": id_usuario}
        ).mappings().first()

        vencendo_7_dias = db.session.execute(
            text("CALL sp_inicio_total_vencendo_7_dias(:id)"),
            {"id": id_usuario}
        ).mappings().first()

        db.session.commit()

        return {
            "total_cadastrados": cadastrados["total_itens_cadastrados"],
            "total_estoque_baixo": estoque_baixo["total_itens_estoque_baixo"],
            "total_vencendo_7_dias": vencendo_7_dias["total_lotes_vencendo_7_dias"],
        }

    @staticmethod
    def get_estoque_baixo(id_usuario, limite=5):
        """
        Executa sp_listar_estoque e filtra apenas os produtos cuja
        quantidade atual está abaixo do mínimo configurado.
        """
        resultado = db.session.execute(
            text("CALL sp_listar_estoque(:id)"),
            {"id": id_usuario}
        ).mappings().all()

        db.session.commit()

        abaixo_do_minimo = [
            {
                "produto": linha["produto"],
                "categoria": linha["categoria"],
                "quantidade": linha["quantidade"],
                "valor_minimo": linha["valor_minimo"],
            }
            for linha in resultado
            if linha["quantidade"] < linha["valor_minimo"]
        ]

        return abaixo_do_minimo[:limite]

    @staticmethod
    def get_vencendo_7_dias(id_usuario):
        """
        Executa sp_inicio_total_vencendo_7_dias_lista e retorna a lista de
        lotes que vencem nos próximos 7 dias (incluindo hoje) para o
        usuário logado.
        """
        resultado = db.session.execute(
            text("CALL sp_inicio_total_vencendo_7_dias_lista(:id)"),
            {"id": id_usuario}
        ).mappings().all()

        db.session.commit()

        return [
            {
                "id_lote": linha["id_lote"],
                "id_produto": linha["id_produto"],
                "produto": linha["produto"],
                "numero_lote": linha["numero_lote"],
                "validade": linha["validade"].isoformat() if linha["validade"] else None,
                "quantidade_atual": float(linha["quantidade_atual"]) if linha["quantidade_atual"] is not None else None,
                "custo_unitario": float(linha["custo_unitario"]) if linha["custo_unitario"] is not None else None,
            }
            for linha in resultado
        ]

