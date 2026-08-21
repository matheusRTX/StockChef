from flask import Blueprint, jsonify, session

from backend.repositories.estoque_repository import EstoqueRepository

estoque_api_bp = Blueprint('estoque_api', __name__, url_prefix='/api/estoque')


@estoque_api_bp.route('/listar')
def listar():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401
    dados = EstoqueRepository.listar_estoque(session['user_id'])
    return jsonify(dados)
