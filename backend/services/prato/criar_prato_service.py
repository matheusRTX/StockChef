from backend.models.prato import Prato
from backend.models.tipo_culinaria import TipoCulinaria
from backend.models.prato_ingrediente import PratoIngrediente
from backend.models.produto import Produto


class CriarPratoService:
    """
    Caso de uso: cadastrar um novo prato, opcionalmente já com sua lista
    de ingredientes.

    `ingredientes` é uma lista de dicts:
    [{"id_produto": 1, "quantidade": 2, "observacao": "picado"}, ...]
    """

    @staticmethod
    def execute(id_usuario, nome, id_tipo_culinaria, tempo_preparo, rendimento,
                modo_preparo, descricao=None, favorito=False, imagem=None,
                ingredientes=None):
        if not TipoCulinaria.buscar_por_id(id_tipo_culinaria):
            raise Exception("Tipo de culinária informado não existe.")

        prato = Prato.criar(
            id_usuario=id_usuario,
            nome=nome,
            id_tipo_culinaria=id_tipo_culinaria,
            tempo_preparo=tempo_preparo,
            rendimento=rendimento,
            modo_preparo=modo_preparo,
            descricao=descricao,
            favorito=favorito,
            imagem=imagem,
        )

        for ingrediente in (ingredientes or []):
            id_produto = ingrediente.get('id_produto')
            if not Produto.buscar_por_id(id_produto):
                raise Exception(f"Produto {id_produto} não existe.")
            PratoIngrediente.criar(
                id_prato=prato.id_prato,
                id_produto=id_produto,
                quantidade=ingrediente.get('quantidade'),
                observacao=ingrediente.get('observacao'),
            )

        return prato
