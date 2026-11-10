from flask import Blueprint, request, jsonify, session

from backend.repositories.estoque_repository import EstoqueRepository
from backend.services.prato.listar_pratos_service import ListarPratosService
from backend.services.prato_ingrediente.listar_ingredientes_service import ListarIngredientesService
from backend.models.produto import Produto
from backend.models.unidade_medida import UnidadeMedida
from backend.services.ia.sugerir_pratos_service import SugerirPratosService

ia_bp = Blueprint('ia', __name__, url_prefix='/api/ia')


class IaController:

    @staticmethod
    def sugerir_pratos():
        if 'user_id' not in session:
            return jsonify({"erro": "não autenticado"}), 401

        dados = request.get_json(force=True) or {}
        usar_cardapio = dados.get("usar_cardapio", True)
        tipo_culinaria = dados.get("tipo_culinaria") or None

        id_usuario = session['id_estabelecimento']

        estoque = EstoqueRepository.listar_estoque(id_usuario)

        cardapio = None
        if usar_cardapio:
            pratos = ListarPratosService.execute(id_usuario=id_usuario, apenas_favoritos=False)
            cardapio = []
            for prato in pratos:
                ingredientes_raw = ListarIngredientesService.execute(prato.id_prato)
                ingredientes = []
                for ing in ingredientes_raw:
                    produto = Produto.buscar_por_id(ing.id_produto)
                    ingredientes.append({
                        "nome": produto.nome if produto else str(ing.id_produto),
                        "quantidade": float(ing.quantidade),
                        "unidade": UnidadeMedida.buscar_por_id(produto.id_unidade).sigla if produto else "",
                    })
                cardapio.append({
                    "nome": prato.nome,
                    "descricao": prato.descricao,
                    "favorito": prato.favorito,
                    "tempo_preparo": prato.tempo_preparo,
                    "rendimento": prato.rendimento,
                    "modo_preparo": prato.modo_preparo,
                    "ingredientes": ingredientes,
                })

        try:
            pratos_sugeridos = SugerirPratosService.execute(estoque, cardapio, tipo_culinaria)
            return jsonify({"pratos": pratos_sugeridos})
        except Exception as e:
            return jsonify({"erro": str(e)}), 500


ia_bp.add_url_rule('/sugerir-pratos', view_func=IaController.sugerir_pratos, methods=['POST'])
