from flask import Blueprint, request, jsonify, session

from backend.services.tipo_culinaria.criar_tipo_culinaria_service import CriarTipoCulinariaService
from backend.services.tipo_culinaria.listar_tipos_culinaria_service import ListarTiposCulinariaService
from backend.services.tipo_culinaria.buscar_tipo_culinaria_service import BuscarTipoCulinariaService
from backend.services.tipo_culinaria.atualizar_tipo_culinaria_service import AtualizarTipoCulinariaService
from backend.services.tipo_culinaria.remover_tipo_culinaria_service import RemoverTipoCulinariaService

tipo_culinaria_bp = Blueprint('tipo_culinaria', __name__, url_prefix='/api/tipos-culinaria')


class TipoCulinariaController:
    """Controller responsável pelas rotas de Tipo de Culinária."""

    @staticmethod
    def _tipo_para_json(tipo):
        return {
            "id_tipo_culinaria": tipo.id_tipo_culinaria,
            "nome": tipo.nome,
            "descricao": tipo.descricao,
        }

    @staticmethod
    def exigir_login():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

    @staticmethod
    def listar():
        tipos = ListarTiposCulinariaService.execute()
        return jsonify([TipoCulinariaController._tipo_para_json(t) for t in tipos])

    @staticmethod
    def criar():
        dados = request.get_json(force=True)
        try:
            tipo = CriarTipoCulinariaService.execute(
                nome=dados.get('nome'),
                descricao=dados.get('descricao'),
            )
            return jsonify(TipoCulinariaController._tipo_para_json(tipo)), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def buscar(id_tipo_culinaria):
        try:
            tipo = BuscarTipoCulinariaService.execute(id_tipo_culinaria)
            return jsonify(TipoCulinariaController._tipo_para_json(tipo))
        except Exception as e:
            return jsonify({"erro": str(e)}), 404

    @staticmethod
    def atualizar(id_tipo_culinaria):
        dados = request.get_json(force=True)
        try:
            tipo = AtualizarTipoCulinariaService.execute(id_tipo_culinaria, **dados)
            return jsonify(TipoCulinariaController._tipo_para_json(tipo))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def remover(id_tipo_culinaria):
        try:
            RemoverTipoCulinariaService.execute(id_tipo_culinaria)
            return jsonify({"mensagem": "Tipo de culinária removido com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


# ---------------------- Registro das rotas ----------------------

tipo_culinaria_bp.before_request(TipoCulinariaController.exigir_login)

tipo_culinaria_bp.add_url_rule('', view_func=TipoCulinariaController.listar, methods=['GET'])
tipo_culinaria_bp.add_url_rule('', view_func=TipoCulinariaController.criar, methods=['POST'])
tipo_culinaria_bp.add_url_rule('/<int:id_tipo_culinaria>', view_func=TipoCulinariaController.buscar, methods=['GET'])
tipo_culinaria_bp.add_url_rule('/<int:id_tipo_culinaria>', view_func=TipoCulinariaController.atualizar, methods=['PUT'])
tipo_culinaria_bp.add_url_rule('/<int:id_tipo_culinaria>', view_func=TipoCulinariaController.remover, methods=['DELETE'])
