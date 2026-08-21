from flask import Blueprint, request, jsonify, session

from backend.services.prato.criar_prato_service import CriarPratoService
from backend.services.prato.listar_pratos_service import ListarPratosService
from backend.services.prato.buscar_prato_service import BuscarPratoService
from backend.services.prato.atualizar_prato_service import AtualizarPratoService
from backend.services.prato.remover_prato_service import RemoverPratoService

from backend.services.prato_ingrediente.adicionar_ingrediente_service import AdicionarIngredienteService
from backend.services.prato_ingrediente.listar_ingredientes_service import ListarIngredientesService
from backend.services.prato_ingrediente.atualizar_ingrediente_service import AtualizarIngredienteService
from backend.services.prato_ingrediente.remover_ingrediente_service import RemoverIngredienteService

from backend.services.prato.verificar_disponibilidade_service import VerificarDisponibilidadeService
from backend.services.prato.preparar_prato_service import PrepararPratoService

prato_bp = Blueprint('prato', __name__, url_prefix='/api/pratos')


def _prato_para_json(prato):
    return {
        "id_prato": prato.id_prato,
        "id_usuario": prato.id_usuario,
        "nome": prato.nome,
        "descricao": prato.descricao,
        "id_tipo_culinaria": prato.id_tipo_culinaria,
        "tempo_preparo": prato.tempo_preparo,
        "rendimento": prato.rendimento,
        "modo_preparo": prato.modo_preparo,
        "favorito": prato.favorito,
        "ativo": prato.ativo,
        "imagem": prato.imagem,
    }


def _ingrediente_para_json(ingrediente):
    return {
        "id_prato_ingrediente": ingrediente.id_prato_ingrediente,
        "id_prato": ingrediente.id_prato,
        "id_produto": ingrediente.id_produto,
        "quantidade": float(ingrediente.quantidade) if ingrediente.quantidade is not None else None,
        "observacao": ingrediente.observacao,
    }


@prato_bp.before_request
def exigir_login():
    if 'user_id' not in session:
        return jsonify({"erro": "não autenticado"}), 401


@prato_bp.route('', methods=['GET'])
def listar():
    apenas_favoritos = request.args.get('favoritos') == 'true'
    pratos = ListarPratosService.execute(apenas_favoritos=apenas_favoritos)
    return jsonify([_prato_para_json(p) for p in pratos])


@prato_bp.route('', methods=['POST'])
def criar():
    dados = request.get_json(force=True)
    try:
        prato = CriarPratoService.execute(
            id_usuario=session['user_id'],
            nome=dados.get('nome'),
            id_tipo_culinaria=dados.get('id_tipo_culinaria'),
            tempo_preparo=dados.get('tempo_preparo'),
            rendimento=dados.get('rendimento'),
            modo_preparo=dados.get('modo_preparo'),
            descricao=dados.get('descricao'),
            favorito=dados.get('favorito', False),
            imagem=dados.get('imagem'),
            ingredientes=dados.get('ingredientes'),
        )
        return jsonify(_prato_para_json(prato)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@prato_bp.route('/<int:id_prato>', methods=['GET'])
def buscar(id_prato):
    try:
        prato, ingredientes = BuscarPratoService.execute(id_prato)
        resposta = _prato_para_json(prato)
        resposta['ingredientes'] = [_ingrediente_para_json(i) for i in ingredientes]
        return jsonify(resposta)
    except Exception as e:
        return jsonify({"erro": str(e)}), 404


@prato_bp.route('/<int:id_prato>', methods=['PUT'])
def atualizar(id_prato):
    dados = request.get_json(force=True)
    try:
        prato = AtualizarPratoService.execute(id_prato, **dados)
        return jsonify(_prato_para_json(prato))
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@prato_bp.route('/<int:id_prato>', methods=['DELETE'])
def remover(id_prato):
    try:
        RemoverPratoService.execute(id_prato)
        return jsonify({"mensagem": "Prato removido com sucesso."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# ---------------------- Ingredientes do prato ----------------------

@prato_bp.route('/<int:id_prato>/ingredientes', methods=['GET'])
def listar_ingredientes(id_prato):
    ingredientes = ListarIngredientesService.execute(id_prato)
    return jsonify([_ingrediente_para_json(i) for i in ingredientes])


@prato_bp.route('/<int:id_prato>/ingredientes', methods=['POST'])
def adicionar_ingrediente(id_prato):
    dados = request.get_json(force=True)
    try:
        ingrediente = AdicionarIngredienteService.execute(
            id_prato=id_prato,
            id_produto=dados.get('id_produto'),
            quantidade=dados.get('quantidade'),
            observacao=dados.get('observacao'),
        )
        return jsonify(_ingrediente_para_json(ingrediente)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@prato_bp.route('/ingredientes/<int:id_prato_ingrediente>', methods=['PUT'])
def atualizar_ingrediente(id_prato_ingrediente):
    dados = request.get_json(force=True)
    try:
        ingrediente = AtualizarIngredienteService.execute(id_prato_ingrediente, **dados)
        return jsonify(_ingrediente_para_json(ingrediente))
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@prato_bp.route('/ingredientes/<int:id_prato_ingrediente>', methods=['DELETE'])
def remover_ingrediente(id_prato_ingrediente):
    try:
        RemoverIngredienteService.execute(id_prato_ingrediente)
        return jsonify({"mensagem": "Ingrediente removido com sucesso."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# ---------------------- Preparo do prato ----------------------

@prato_bp.route('/<int:id_prato>/disponibilidade', methods=['GET'])
def verificar_disponibilidade(id_prato):
    try:
        resultado = VerificarDisponibilidadeService.execute(id_prato)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@prato_bp.route('/<int:id_prato>/preparar', methods=['POST'])
def preparar(id_prato):
    try:
        movimentacao = PrepararPratoService.execute(id_prato, session['user_id'])
        return jsonify({
            "mensagem": "Prato preparado com sucesso. Ingredientes abatidos do estoque.",
            "id_movimentacao": movimentacao.id_movimentacao,
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
