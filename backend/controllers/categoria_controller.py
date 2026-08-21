from flask import Blueprint, request, jsonify, session

from backend.services.categoria.criar_categoria_service import CriarCategoriaService
from backend.services.categoria.listar_categorias_service import ListarCategoriasService
from backend.services.categoria.buscar_categoria_service import BuscarCategoriaService
from backend.services.categoria.atualizar_categoria_service import AtualizarCategoriaService
from backend.services.categoria.remover_categoria_service import RemoverCategoriaService

categoria_bp = Blueprint('categoria', __name__, url_prefix='/api/categorias')


def _categoria_para_json(categoria):
    return {
        "id_categoria": categoria.id_categoria,
        "nome": categoria.nome,
        "descricao": categoria.descricao,
    }


@categoria_bp.before_request
def exigir_login():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401


@categoria_bp.route('', methods=['GET'])
def listar():
    categorias = ListarCategoriasService.execute()
    return jsonify([_categoria_para_json(c) for c in categorias])


@categoria_bp.route('', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    try:
        categoria = CriarCategoriaService.execute(
            nome=dados.get('nome'),
            descricao=dados.get('descricao'),
        )
        return jsonify(_categoria_para_json(categoria)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@categoria_bp.route('/<int:id_categoria>', methods=['GET'])
def buscar(id_categoria):
    try:
        categoria = BuscarCategoriaService.execute(id_categoria)
        return jsonify(_categoria_para_json(categoria))
    except Exception as e:
        return jsonify({"erro": str(e)}), 404


@categoria_bp.route('/<int:id_categoria>', methods=['PUT'])
def atualizar(id_categoria):
    dados = request.get_json(force=True)
    try:
        categoria = AtualizarCategoriaService.execute(id_categoria, **dados)
        return jsonify(_categoria_para_json(categoria))
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@categoria_bp.route('/<int:id_categoria>', methods=['DELETE'])
def remover(id_categoria):
    try:
        RemoverCategoriaService.execute(id_categoria)
        return jsonify({"mensagem": "Categoria removida com sucesso."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
