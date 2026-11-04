from flask import Blueprint, request, jsonify, session

from backend.services.categoria.criar_categoria_service import CriarCategoriaService
from backend.services.categoria.listar_categorias_service import ListarCategoriasService
from backend.services.categoria.buscar_categoria_service import BuscarCategoriaService
from backend.services.categoria.atualizar_categoria_service import AtualizarCategoriaService
from backend.services.categoria.remover_categoria_service import RemoverCategoriaService

categoria_bp = Blueprint('categoria', __name__, url_prefix='/api/categorias')


class CategoriaController:
    """Controller responsável pelas rotas de Categoria."""

    @staticmethod
    def _categoria_para_json(categoria):
        return {
            "id_categoria": categoria.id_categoria,
            "nome": categoria.nome,
            "descricao": categoria.descricao,
        }

    @staticmethod
    def exigir_login():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

    @staticmethod
    def listar():
        categorias = ListarCategoriasService.execute()
        return jsonify([CategoriaController._categoria_para_json(c) for c in categorias])

    @staticmethod
    def criar():
        dados = request.get_json(force=True)
        try:
            categoria = CriarCategoriaService.execute(
                nome=dados.get('nome'),
                descricao=dados.get('descricao'),
            )
            return jsonify(CategoriaController._categoria_para_json(categoria)), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def buscar(id_categoria):
        try:
            categoria = BuscarCategoriaService.execute(id_categoria)
            return jsonify(CategoriaController._categoria_para_json(categoria))
        except Exception as e:
            return jsonify({"erro": str(e)}), 404

    @staticmethod
    def atualizar(id_categoria):
        dados = request.get_json(force=True)
        try:
            categoria = AtualizarCategoriaService.execute(id_categoria, **dados)
            return jsonify(CategoriaController._categoria_para_json(categoria))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def remover(id_categoria):
        try:
            RemoverCategoriaService.execute(id_categoria)
            return jsonify({"mensagem": "Categoria removida com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


# ---------------------- Registro das rotas ----------------------

categoria_bp.before_request(CategoriaController.exigir_login)

categoria_bp.add_url_rule('', view_func=CategoriaController.listar, methods=['GET'])
categoria_bp.add_url_rule('', view_func=CategoriaController.criar, methods=['POST'])
categoria_bp.add_url_rule('/<int:id_categoria>', view_func=CategoriaController.buscar, methods=['GET'])
categoria_bp.add_url_rule('/<int:id_categoria>', view_func=CategoriaController.atualizar, methods=['PUT'])
categoria_bp.add_url_rule('/<int:id_categoria>', view_func=CategoriaController.remover, methods=['DELETE'])
