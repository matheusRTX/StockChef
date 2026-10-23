import json
import re
import google.generativeai as genai
from flask import current_app


ESQUEMA_JSON = """
{
  "pratos": [
    {
      "nome": "string",
      "descricao": "string",
      "motivo": "string (por que foi priorizado)",
      "tempo_preparo": 30,
      "porcoes": 4,
      "modo_preparo": ["passo 1", "passo 2"],
      "ingredientes": [
        {"nome": "string", "quantidade": 0.5, "unidade": "kg", "disponivel": true (tem no estoque) ou false (falta no estoque)}
      ]
    }
  ]
}
"""


class SugerirPratosService:

    @staticmethod
    def execute(estoque: list, cardapio: list | None, tipo_culinaria: str | None) -> list:
        genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-3.5-flash-lite")

        estoque_txt = SugerirPratosService._formatar_estoque(estoque)
        prompt = SugerirPratosService._montar_prompt(estoque_txt, cardapio, tipo_culinaria)

        resposta = model.generate_content(prompt)
        texto = resposta.text

        # Extrai o JSON da resposta (remove markdown ```json se vier)
        match = re.search(r'\{.*\}', texto, re.DOTALL)
        if not match:
            raise ValueError("A IA não retornou um JSON válido.")

        return json.loads(match.group())["pratos"]

    @staticmethod
    def _formatar_estoque(estoque: list) -> str:
        linhas = []
        for item in estoque:
            lotes_txt = ", ".join(
                f"{l['quantidade_atual']} {item['unidade']} (vence {l['validade']})"
                for l in item.get("lotes", [])
            ) or "sem lotes"
            linhas.append(
                f"- {item['produto']} | categoria: {item['categoria']} | "
                f"total: {item['quantidade_total']} {item['unidade']} | lotes: [{lotes_txt}]"
            )
        return "\n".join(linhas)

    @staticmethod
    def _montar_prompt(estoque_txt: str, cardapio: list | None, tipo_culinaria: str | None) -> str:
        partes = [
            "Você é um chef de cozinha especialista. Sugira de 3 a 5 pratos com base no estoque abaixo.",
            "PRIORIZE ingredientes com validade mais próxima para evitar desperdício.",
            "Use APENAS as unidades do estoque para cada ingrediente.",
            f"Responda SOMENTE com um JSON válido seguindo exatamente este esquema:{ESQUEMA_JSON}",
            "Unidades permitidas para 'unidade': kg, g, l, ml, unidade, pacote, caixa, lata, garrafa.",
            "Para o campo modo_preparo, escreva de 8 a 15 passos detalhados, cada passo sendo uma string separada no array.",
            "Cada passo deve ser claro e completo: inclua temperaturas, tempos de cozimento, técnicas (ex: refogar, dourar, temperar), texturas esperadas e dicas visuais para o cozinheiro saber quando está no ponto certo.",
            "Exemplo de passo bem detalhado: 'Aqueça 2 colheres de azeite em fogo médio-alto até começar a brilhar levemente. Adicione a cebola picada e refogue por 3 a 4 minutos, mexendo sempre, até ficar translúcida e levemente dourada nas bordas.'",
        ]

        if tipo_culinaria:
            partes.append(f"Tipo de culinária desejado: {tipo_culinaria}.")

        partes.append(f"\nESTOQUE DISPONÍVEL:\n{estoque_txt}")

        if cardapio:
            cardapio_txt = SugerirPratosService._formatar_cardapio(cardapio)
            partes += [
                "\nRESTRIÇÃO OBRIGATÓRIA: sugira APENAS pratos que existem no cardápio abaixo.",
                "Pratos marcados como favorito=verdadeiro SEMPRE devem aparecer, mesmo com ingredientes faltando (marque disponivel=falso).",
                "Copie nome, descricao, modo_preparo, tempo_preparo e porcoes exatamente como estão no cardápio.",
                f"\nCARDÁPIO:\n{cardapio_txt}",
            ]

        return "\n".join(partes)

    @staticmethod
    def _formatar_cardapio(cardapio: list) -> str:
        linhas = []
        for p in cardapio:
            ings = ", ".join(
                f"{i['nome']} {i['quantidade']} {i['unidade']}"
                for i in p.get("ingredientes", [])
            )
            linhas.append(
                f"- {p['nome']} | favorito: {'sim' if p.get('favorito') else 'nao'} | "
                f"tempo: {p.get('tempo_preparo')} min | porções: {p.get('rendimento')} | "
                f"ingredientes: [{ings}] | preparo: {p.get('modo_preparo', '')[:200]}"
            )
        return "\n".join(linhas)
