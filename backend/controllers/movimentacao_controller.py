from datetime import datetime
from flask import Blueprint, request, jsonify, session

from backend.services.movimentacao.registrar_movimentacao_service import RegistrarMovimentacaoService
from backend.services.movimentacao.listar_movimentacoes_service import ListarMovimentacoesService
from backend.services.movimentacao.buscar_movimentacao_service import BuscarMovimentacaoService
from backend.services.movimentacao.atualizar_movimentacao_service import AtualizarMovimentacaoService
from backend.services.movimentacao.remover_movimentacao_service import RemoverMovimentacaoService

movimentacao_bp = Blueprint('movimentacao', __name__, url_prefix='/api/movimentacoes')


def _movimentacao_para_json(movimentacao):
    return {
        "id_movimentacao": movimentacao.id_movimentacao,
        "id_usuario": movimentacao.id_usuario,
        "tipo": movimentacao.tipo,
        "data_movimentacao": movimentacao.data_movimentacao.isoformat() if movimentacao.data_movimentacao else None,
        "observacao": movimentacao.observacao,
    }


def _item_para_json(item):
    return {
        "id_movimentacao_item": item.id_movimentacao_item,
        "id_produto": item.id_produto,
        "quantidade": float(item.quantidade) if item.quantidade is not None else None,
    }


@movimentacao_bp.before_request
def exigir_login():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401


@movimentacao_bp.route('', methods=['GET'])
def listar():
    movimentacoes = ListarMovimentacoesService.execute()
    return jsonify([_movimentacao_para_json(m) for m in movimentacoes])


@movimentacao_bp.route('', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    try:
        itens = dados.get('itens', [])
        for item in itens:
            if item.get('validade'):
                item['validade'] = datetime.strptime(item['validade'], '%Y-%m-%d').date()

        movimentacao = RegistrarMovimentacaoService.execute(
            id_usuario=session['user_id'],
            tipo=dados.get('tipo'),
            itens=itens,
            observacao=dados.get('observacao'),
        )
        return jsonify(_movimentacao_para_json(movimentacao)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@movimentacao_bp.route('/<int:id_movimentacao>', methods=['GET'])
def buscar(id_movimentacao):
    try:
        movimentacao, itens = BuscarMovimentacaoService.execute(id_movimentacao)
        resposta = _movimentacao_para_json(movimentacao)
        resposta['itens'] = [_item_para_json(i) for i in itens]
        return jsonify(resposta)
    except Exception as e:
        return jsonify({"erro": str(e)}), 404


@movimentacao_bp.route('/<int:id_movimentacao>', methods=['PUT'])
def atualizar(id_movimentacao):
    dados = request.get_json(force=True)
    try:
        movimentacao = AtualizarMovimentacaoService.execute(id_movimentacao, **dados)
        return jsonify(_movimentacao_para_json(movimentacao))
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@movimentacao_bp.route('/<int:id_movimentacao>', methods=['DELETE'])
def remover(id_movimentacao):
    try:
        RemoverMovimentacaoService.execute(id_movimentacao)
        return jsonify({"mensagem": "Movimentação removida com sucesso."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
