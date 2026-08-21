from flask import Blueprint, request, jsonify, session

from backend.services.tipo_culinaria.criar_tipo_culinaria_service import CriarTipoCulinariaService
from backend.services.tipo_culinaria.listar_tipos_culinaria_service import ListarTiposCulinariaService
from backend.services.tipo_culinaria.buscar_tipo_culinaria_service import BuscarTipoCulinariaService
from backend.services.tipo_culinaria.atualizar_tipo_culinaria_service import AtualizarTipoCulinariaService
from backend.services.tipo_culinaria.remover_tipo_culinaria_service import RemoverTipoCulinariaService

tipo_culinaria_bp = Blueprint('tipo_culinaria', __name__, url_prefix='/api/tipos-culinaria')


def _tipo_para_json(tipo):
    return {
        "id_tipo_culinaria": tipo.id_tipo_culinaria,
        "nome": tipo.nome,
        "descricao": tipo.descricao,
    }


@tipo_culinaria_bp.before_request
def exigir_login():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401


@tipo_culinaria_bp.route('', methods=['GET'])
def listar():
    tipos = ListarTiposCulinariaService.execute()
    return jsonify([_tipo_para_json(t) for t in tipos])


@tipo_culinaria_bp.route('', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    try:
        tipo = CriarTipoCulinariaService.execute(
            nome=dados.get('nome'),
            descricao=dados.get('descricao'),
        )
        return jsonify(_tipo_para_json(tipo)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@tipo_culinaria_bp.route('/<int:id_tipo_culinaria>', methods=['GET'])
def buscar(id_tipo_culinaria):
    try:
        tipo = BuscarTipoCulinariaService.execute(id_tipo_culinaria)
        return jsonify(_tipo_para_json(tipo))
    except Exception as e:
        return jsonify({"erro": str(e)}), 404


@tipo_culinaria_bp.route('/<int:id_tipo_culinaria>', methods=['PUT'])
def atualizar(id_tipo_culinaria):
    dados = request.get_json(force=True)
    try:
        tipo = AtualizarTipoCulinariaService.execute(id_tipo_culinaria, **dados)
        return jsonify(_tipo_para_json(tipo))
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@tipo_culinaria_bp.route('/<int:id_tipo_culinaria>', methods=['DELETE'])
def remover(id_tipo_culinaria):
    try:
        RemoverTipoCulinariaService.execute(id_tipo_culinaria)
        return jsonify({"mensagem": "Tipo de culinária removido com sucesso."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
