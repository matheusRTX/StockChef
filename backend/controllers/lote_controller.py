from datetime import datetime
from flask import Blueprint, request, jsonify, session

from backend.services.lote.criar_lote_service import CriarLoteService
from backend.services.lote.listar_lotes_service import ListarLotesService
from backend.services.lote.buscar_lote_service import BuscarLoteService
from backend.services.lote.atualizar_lote_service import AtualizarLoteService
from backend.services.lote.remover_lote_service import RemoverLoteService

lote_bp = Blueprint('lote', __name__, url_prefix='/api/lotes')


class LoteController:
    """Controller responsável pelas rotas de Lote."""

    @staticmethod
    def _lote_para_json(lote):
        return {
            "id_lote": lote.id_lote,
            "id_produto": lote.id_produto,
            "numero_lote": lote.numero_lote,
            "validade": lote.validade.isoformat() if lote.validade else None,
            "quantidade_inicial": float(lote.quantidade_inicial) if lote.quantidade_inicial is not None else None,
            "quantidade_atual": float(lote.quantidade_atual) if lote.quantidade_atual is not None else None,
            "custo_unitario": float(lote.custo_unitario) if lote.custo_unitario is not None else None,
            "data_entrada": lote.data_entrada.isoformat() if lote.data_entrada else None,
            "observacao": lote.observacao,
        }

    @staticmethod
    def exigir_login():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

    @staticmethod
    def listar():
        id_produto = request.args.get('id_produto', type=int)
        lotes = ListarLotesService.execute(id_produto=id_produto)
        return jsonify([LoteController._lote_para_json(l) for l in lotes])

    @staticmethod
    def criar():
        dados = request.get_json(force=True)
        try:
            validade = datetime.strptime(dados.get('validade'), '%Y-%m-%d').date()
            lote = CriarLoteService.execute(
                id_produto=dados.get('id_produto'),
                validade=validade,
                quantidade_inicial=dados.get('quantidade_inicial'),
                numero_lote=dados.get('numero_lote'),
                custo_unitario=dados.get('custo_unitario'),
                observacao=dados.get('observacao'),
            )
            return jsonify(LoteController._lote_para_json(lote)), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def buscar(id_lote):
        try:
            lote = BuscarLoteService.execute(id_lote)
            return jsonify(LoteController._lote_para_json(lote))
        except Exception as e:
            return jsonify({"erro": str(e)}), 404

    @staticmethod
    def atualizar(id_lote):
        dados = request.get_json(force=True)
        if 'validade' in dados and dados['validade']:
            dados['validade'] = datetime.strptime(dados['validade'], '%Y-%m-%d').date()
        try:
            lote = AtualizarLoteService.execute(id_lote, **dados)
            return jsonify(LoteController._lote_para_json(lote))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def remover(id_lote):
        try:
            RemoverLoteService.execute(id_lote)
            return jsonify({"mensagem": "Lote removido com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


# ---------------------- Registro das rotas ----------------------

lote_bp.before_request(LoteController.exigir_login)

lote_bp.add_url_rule('', view_func=LoteController.listar, methods=['GET'])
lote_bp.add_url_rule('', view_func=LoteController.criar, methods=['POST'])
lote_bp.add_url_rule('/<int:id_lote>', view_func=LoteController.buscar, methods=['GET'])
lote_bp.add_url_rule('/<int:id_lote>', view_func=LoteController.atualizar, methods=['PUT'])
lote_bp.add_url_rule('/<int:id_lote>', view_func=LoteController.remover, methods=['DELETE'])
