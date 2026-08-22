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


class PratoController:
    """Controller responsável pelas rotas de Prato, seus ingredientes e preparo."""

    @staticmethod
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

    @staticmethod
    def _ingrediente_para_json(ingrediente):
        return {
            "id_prato_ingrediente": ingrediente.id_prato_ingrediente,
            "id_prato": ingrediente.id_prato,
            "id_produto": ingrediente.id_produto,
            "quantidade": float(ingrediente.quantidade) if ingrediente.quantidade is not None else None,
            "observacao": ingrediente.observacao,
        }

    @staticmethod
    def exigir_login():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

    # ---------------------- Prato ----------------------

    @staticmethod
    def listar():
        apenas_favoritos = request.args.get('favoritos') == 'true'
        pratos = ListarPratosService.execute(apenas_favoritos=apenas_favoritos)
        return jsonify([PratoController._prato_para_json(p) for p in pratos])

    @staticmethod
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
            return jsonify(PratoController._prato_para_json(prato)), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def buscar(id_prato):
        try:
            prato, ingredientes = BuscarPratoService.execute(id_prato)
            resposta = PratoController._prato_para_json(prato)
            resposta['ingredientes'] = [PratoController._ingrediente_para_json(i) for i in ingredientes]
            return jsonify(resposta)
        except Exception as e:
            return jsonify({"erro": str(e)}), 404

    @staticmethod
    def atualizar(id_prato):
        dados = request.get_json(force=True)
        try:
            prato = AtualizarPratoService.execute(id_prato, **dados)
            return jsonify(PratoController._prato_para_json(prato))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def remover(id_prato):
        try:
            RemoverPratoService.execute(id_prato)
            return jsonify({"mensagem": "Prato removido com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    # ---------------------- Ingredientes do prato ----------------------

    @staticmethod
    def listar_ingredientes(id_prato):
        ingredientes = ListarIngredientesService.execute(id_prato)
        return jsonify([PratoController._ingrediente_para_json(i) for i in ingredientes])

    @staticmethod
    def adicionar_ingrediente(id_prato):
        dados = request.get_json(force=True)
        try:
            ingrediente = AdicionarIngredienteService.execute(
                id_prato=id_prato,
                id_produto=dados.get('id_produto'),
                quantidade=dados.get('quantidade'),
                observacao=dados.get('observacao'),
            )
            return jsonify(PratoController._ingrediente_para_json(ingrediente)), 201
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def atualizar_ingrediente(id_prato_ingrediente):
        dados = request.get_json(force=True)
        try:
            ingrediente = AtualizarIngredienteService.execute(id_prato_ingrediente, **dados)
            return jsonify(PratoController._ingrediente_para_json(ingrediente))
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def remover_ingrediente(id_prato_ingrediente):
        try:
            RemoverIngredienteService.execute(id_prato_ingrediente)
            return jsonify({"mensagem": "Ingrediente removido com sucesso."})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    # ---------------------- Preparo do prato ----------------------

    @staticmethod
    def verificar_disponibilidade(id_prato):
        try:
            resultado = VerificarDisponibilidadeService.execute(id_prato)
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"erro": str(e)}), 400

    @staticmethod
    def preparar(id_prato):
        try:
            movimentacao = PrepararPratoService.execute(id_prato, session['user_id'])
            return jsonify({
                "mensagem": "Prato preparado com sucesso. Ingredientes abatidos do estoque.",
                "id_movimentacao": movimentacao.id_movimentacao,
            })
        except Exception as e:
            return jsonify({"erro": str(e)}), 400


# ---------------------- Registro das rotas ----------------------

prato_bp.before_request(PratoController.exigir_login)

prato_bp.add_url_rule('', view_func=PratoController.listar, methods=['GET'])
prato_bp.add_url_rule('', view_func=PratoController.criar, methods=['POST'])
prato_bp.add_url_rule('/<int:id_prato>', view_func=PratoController.buscar, methods=['GET'])
prato_bp.add_url_rule('/<int:id_prato>', view_func=PratoController.atualizar, methods=['PUT'])
prato_bp.add_url_rule('/<int:id_prato>', view_func=PratoController.remover, methods=['DELETE'])

prato_bp.add_url_rule('/<int:id_prato>/ingredientes', view_func=PratoController.listar_ingredientes, methods=['GET'])
prato_bp.add_url_rule('/<int:id_prato>/ingredientes', view_func=PratoController.adicionar_ingrediente, methods=['POST'])
prato_bp.add_url_rule('/ingredientes/<int:id_prato_ingrediente>', view_func=PratoController.atualizar_ingrediente, methods=['PUT'])
prato_bp.add_url_rule('/ingredientes/<int:id_prato_ingrediente>', view_func=PratoController.remover_ingrediente, methods=['DELETE'])

prato_bp.add_url_rule('/<int:id_prato>/disponibilidade', view_func=PratoController.verificar_disponibilidade, methods=['GET'])
prato_bp.add_url_rule('/<int:id_prato>/preparar', view_func=PratoController.preparar, methods=['POST'])
