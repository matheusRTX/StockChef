from flask import Blueprint, request, jsonify, session

from backend.services.fornecedor.criar_fornecedor_service import CriarFornecedorService
from backend.services.fornecedor.listar_fornecedores_service import ListarFornecedoresService
from backend.services.fornecedor.atualizar_fornecedor_service import AtualizarFornecedorService
from backend.services.fornecedor.remover_fornecedor_service import RemoverFornecedorService

fornecedor_bp = Blueprint('fornecedor', __name__, url_prefix='/api/fornecedores')


class FornecedorController:
    """Controller responsável pelas rotas de Fornecedor."""

    @staticmethod
    def _fornecedor_para_json(fornecedor, categoria=None):
        return {
            "id_fornecedor": fornecedor.id_fornecedor,
            "nome": fornecedor.nome,
            "telefone": fornecedor.telefone,
            "email": fornecedor.email,
            "id_categoria": categoria['id_categoria'] if categoria else None,
            "categoria": categoria['nome'] if categoria else None,
        }

    @staticmethod
    def exigir_login():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

    @staticmethod
    def listar():
        fornecedores = ListarFornecedoresService.execute(session['id_estabelecimento'])
        return jsonify([
            FornecedorController._fornecedor_para_json(f, categoria)
            for f, categoria in fornecedores
        ])

    @staticmethod
    def criar():
        dados = request.get_json(force=True)
        try:
            fornecedor, categoria = CriarFornecedorService.execute(
                id_usuario=session['id_estabelecimento'],
                nome=dados.get('nome'),
                telefone=dados.get('telefone'),
                email=dados.get('email'),
                id_categoria=dados.get('id_categoria'),
            )
            return jsonify(FornecedorController._fornecedor_para_json(fornecedor, categoria)), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def atualizar(id_fornecedor):
        dados = request.get_json(force=True)
        try:
            fornecedor, categoria = AtualizarFornecedorService.execute(
                id_fornecedor=id_fornecedor,
                id_usuario=session['id_estabelecimento'],
                nome=dados.get('nome'),
                telefone=dados.get('telefone'),
                email=dados.get('email'),
                id_categoria=dados.get('id_categoria'),
            )
            return jsonify(FornecedorController._fornecedor_para_json(fornecedor, categoria))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def remover(id_fornecedor):
        try:
            RemoverFornecedorService.execute(id_fornecedor, session['id_estabelecimento'])
            return jsonify({"mensagem": "Fornecedor removido com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


# ---------------------- Registro das rotas ----------------------

fornecedor_bp.before_request(FornecedorController.exigir_login)

fornecedor_bp.add_url_rule('', view_func=FornecedorController.listar, methods=['GET'])
fornecedor_bp.add_url_rule('', view_func=FornecedorController.criar, methods=['POST'])
fornecedor_bp.add_url_rule('/<int:id_fornecedor>', view_func=FornecedorController.atualizar, methods=['PUT'])
fornecedor_bp.add_url_rule('/<int:id_fornecedor>', view_func=FornecedorController.remover, methods=['DELETE'])
