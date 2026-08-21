from flask import Blueprint, request, jsonify, session

from backend.services.produto.criar_produto_service import CriarProdutoService
from backend.services.produto.listar_produtos_service import ListarProdutosService
from backend.services.produto.buscar_produto_service import BuscarProdutoService
from backend.services.produto.atualizar_produto_service import AtualizarProdutoService
from backend.services.produto.remover_produto_service import RemoverProdutoService

produto_bp = Blueprint('produto', __name__, url_prefix='/api/produtos')


def _produto_para_json(produto):
    return {
        "id_produto": produto.id_produto,
        "id_usuario": produto.id_usuario,
        "nome": produto.nome,
        "descricao": produto.descricao,
        "codigo_barras": produto.codigo_barras,
        "qr_code": produto.qr_code,
        "id_categoria": produto.id_categoria,
        "id_unidade": produto.id_unidade,
        "estoque_minimo": float(produto.estoque_minimo) if produto.estoque_minimo is not None else None,
        "imagem": produto.imagem,
        "ativo": produto.ativo,
    }


@produto_bp.before_request
def exigir_login():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401


@produto_bp.route('', methods=['GET'])
def listar():
    produtos = ListarProdutosService.execute()
    return jsonify([_produto_para_json(p) for p in produtos])


@produto_bp.route('', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    try:
        produto = CriarProdutoService.execute(
            id_usuario=session['user_id'],
            nome=dados.get('nome'),
            id_categoria=dados.get('id_categoria'),
            id_unidade=dados.get('id_unidade'),
            descricao=dados.get('descricao'),
            codigo_barras=dados.get('codigo_barras'),
            qr_code=dados.get('qr_code'),
            estoque_minimo=dados.get('estoque_minimo', 0),
            imagem=dados.get('imagem'),
        )
        return jsonify(_produto_para_json(produto)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@produto_bp.route('/<int:id_produto>', methods=['GET'])
def buscar(id_produto):
    try:
        produto = BuscarProdutoService.execute(id_produto)
        return jsonify(_produto_para_json(produto))
    except Exception as e:
        return jsonify({"erro": str(e)}), 404


@produto_bp.route('/<int:id_produto>', methods=['PUT'])
def atualizar(id_produto):
    dados = request.get_json(force=True)
    try:
        produto = AtualizarProdutoService.execute(id_produto, **dados)
        return jsonify(_produto_para_json(produto))
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@produto_bp.route('/<int:id_produto>', methods=['DELETE'])
def remover(id_produto):
    try:
        RemoverProdutoService.execute(id_produto)
        return jsonify({"mensagem": "Produto removido com sucesso."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
