from flask import Blueprint, request, jsonify, session

from backend.services.unidade_medida.criar_unidade_medida_service import CriarUnidadeMedidaService
from backend.services.unidade_medida.listar_unidades_medida_service import ListarUnidadesMedidaService
from backend.services.unidade_medida.buscar_unidade_medida_service import BuscarUnidadeMedidaService
from backend.services.unidade_medida.atualizar_unidade_medida_service import AtualizarUnidadeMedidaService
from backend.services.unidade_medida.remover_unidade_medida_service import RemoverUnidadeMedidaService

unidade_medida_bp = Blueprint('unidade_medida', __name__, url_prefix='/api/unidades-medida')


class UnidadeMedidaController:
    """Controller responsável pelas rotas de Unidade de Medida."""

    @staticmethod
    def _unidade_para_json(unidade):
        return {
            "id_unidade": unidade.id_unidade,
            "sigla": unidade.sigla,
            "descricao": unidade.descricao,
        }

    @staticmethod
    def exigir_login():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

    @staticmethod
    def listar():
        unidades = ListarUnidadesMedidaService.execute()
        return jsonify([UnidadeMedidaController._unidade_para_json(u) for u in unidades])

    @staticmethod
    def criar():
        dados = request.get_json(force=True)
        try:
            unidade = CriarUnidadeMedidaService.execute(
                sigla=dados.get('sigla'),
                descricao=dados.get('descricao'),
            )
            return jsonify(UnidadeMedidaController._unidade_para_json(unidade)), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def buscar(id_unidade):
        try:
            unidade = BuscarUnidadeMedidaService.execute(id_unidade)
            return jsonify(UnidadeMedidaController._unidade_para_json(unidade))
        except Exception as e:
            return jsonify({"erro": str(e)}), 404

    @staticmethod
    def atualizar(id_unidade):
        dados = request.get_json(force=True)
        try:
            unidade = AtualizarUnidadeMedidaService.execute(id_unidade, **dados)
            return jsonify(UnidadeMedidaController._unidade_para_json(unidade))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def remover(id_unidade):
        try:
            RemoverUnidadeMedidaService.execute(id_unidade)
            return jsonify({"mensagem": "Unidade de medida removida com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


# ---------------------- Registro das rotas ----------------------

unidade_medida_bp.before_request(UnidadeMedidaController.exigir_login)

unidade_medida_bp.add_url_rule('', view_func=UnidadeMedidaController.listar, methods=['GET'])
unidade_medida_bp.add_url_rule('', view_func=UnidadeMedidaController.criar, methods=['POST'])
unidade_medida_bp.add_url_rule('/<int:id_unidade>', view_func=UnidadeMedidaController.buscar, methods=['GET'])
unidade_medida_bp.add_url_rule('/<int:id_unidade>', view_func=UnidadeMedidaController.atualizar, methods=['PUT'])
unidade_medida_bp.add_url_rule('/<int:id_unidade>', view_func=UnidadeMedidaController.remover, methods=['DELETE'])
