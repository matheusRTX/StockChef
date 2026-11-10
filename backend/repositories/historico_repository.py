from sqlalchemy import text
from backend.models.usuario import db

MAPA_FILTRO_DATA = {
    'hoje': 0,
    'semana': 1,
    'todos': 2,
}

MAPA_FILTRO_TIPO = {
    'entrada': 0,
    'saida': 1,
    'todos': 2,
}


class HistoricoRepository:

    @staticmethod
    def get_resumo(id_usuario):
        entradas = db.session.execute(
            text("CALL sp_historico_total_entradas(:id)"),
            {"id": id_usuario}
        ).mappings().first()

        saidas = db.session.execute(
            text("CALL sp_historico_total_saidas(:id)"),
            {"id": id_usuario}
        ).mappings().first()

        db.session.commit()

        return {
            "total_entradas": float(entradas["total_acumulado_entradas"]) if entradas else 0,
            "total_saidas": float(saidas["total_acumulado_saidas"]) if saidas else 0,
        }

    @staticmethod
    def listar_movimentacoes(id_usuario, filtro_data='todos', filtro_tipo='todos'):
        codigo_data = MAPA_FILTRO_DATA.get(filtro_data, 2)
        codigo_tipo = MAPA_FILTRO_TIPO.get(filtro_tipo, 2)

        resultado = db.session.execute(
            text("CALL sp_historico_listar_movimentacoes(:id, :data, :tipo)"),
            {"id": id_usuario, "data": codigo_data, "tipo": codigo_tipo}
        ).mappings().all()

        db.session.commit()

        return [
            {
                "produto": linha["nome_produto"],
                "categoria": linha["categoria"],
                "tipo": linha["tipo_movimentacao"],
                "unidade": linha["unidade"],
                "quantidade": float(linha["quantidade_movimentada"]) if linha["quantidade_movimentada"] is not None else 0,
                "data_registro": linha["data_registro"].isoformat() if linha["data_registro"] else None,
            }
            for linha in resultado
        ]
