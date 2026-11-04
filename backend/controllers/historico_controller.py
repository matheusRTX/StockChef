from flask import Blueprint, jsonify, session, request

from backend.repositories.historico_repository import HistoricoRepository

historico_api_bp = Blueprint('historico_api', __name__, url_prefix='/api/historico')


class HistoricoController:
    """Controller responsável pela consulta de histórico de movimentações."""

    @staticmethod
    def exigir_login():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

    @staticmethod
    def resumo():
        dados = HistoricoRepository.get_resumo(session['id_estabelecimento'])
        return jsonify(dados)

    @staticmethod
    def listar():
        filtro_data = request.args.get('data', 'todos')
        filtro_tipo = request.args.get('tipo', 'todos')

        dados = HistoricoRepository.listar_movimentacoes(
            session['id_estabelecimento'], filtro_data, filtro_tipo
        )
        return jsonify(dados)


# ---------------------- Registro das rotas ----------------------

historico_api_bp.before_request(HistoricoController.exigir_login)

historico_api_bp.add_url_rule('/resumo', view_func=HistoricoController.resumo, methods=['GET'])
historico_api_bp.add_url_rule('/listar', view_func=HistoricoController.listar, methods=['GET'])
