# Pith / StockChef - Sistema de Controle de Estoque para Restaurantes

O StockChef ajuda restaurantes a reduzir o desperdício de alimentos e a perda de tempo no controle do estoque: controla lotes e validades, avisa antes de vencer ou acabar, monta a lista de compras, baixa os ingredientes quando um prato é preparado e sugere pratos com IA a partir do que há em estoque.

## Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Backend | Python, Flask |
| ORM | SQLAlchemy (Flask-SQLAlchemy) |
| Banco de dados | MySQL (com stored procedures), driver PyMySQL |
| Segurança | Werkzeug (hash de senhas), autenticação por sessão |
| IA | Google Gemini, via biblioteca `google-generativeai` |
| Frontend | HTML, CSS e JavaScript puro, consumindo a API com `fetch()` |
| Leitura de QR Code | html5-qrcode (carregada por CDN) |

## Arquitetura

```text
Frontend (frontend/html, css, js)  — consome /api/* com fetch()
   ↓ requisição HTTP (JSON)
Controller   (backend/controllers)   — recebe a requisição, confere o login, devolve JSON
   ↓
Service      (backend/services)      — um caso de uso por arquivo, com as regras da aplicação
   ↓
Model        (backend/models)        — classes SQLAlchemy (db.Model) com o CRUD de cada tabela
Repository   (backend/repositories)  — consultas ao banco via procedures (estoque, histórico, início)
   ↓
Banco de Dados (MySQL)
```

- **Models:** cada classe herda `db.Model`, com `criar`, `buscar_por_id`, `listar_todos`, `atualizar` e `deletar` (soft delete quando aplicável).
- **Controllers:** classes que recebem a requisição HTTP e devolvem a resposta; o Blueprint só registra as rotas.
- **Repositories:** concentram as consultas SQL (`CALL sp_...`), sempre parametrizadas.
- **Frontend e API separados:** o frontend só conversa com a API por requisições; não acessa o banco.

## Estrutura do projeto

```text
pith/
├── app.py
├── requirements.txt
├── docs/
│   └── diagrama_de_classes.png
├── frontend/
│   ├── html/
│   ├── css/
│   ├── js/
│   └── imagens/
└── backend/
    ├── config.py
    ├── controllers/
    ├── services/         (uma pasta por recurso, um arquivo por caso de uso)
    ├── models/
    ├── repositories/
    └── database/
        ├── rodar_tudo_de_uma_vez.sql
        └── procedures/
```

## Diagrama de classes

O diagrama de classes do domínio está em [`docs/diagrama_de_classes.png`](docs/diagrama_de_classes.png).

## Casos de uso implementados

Todos funcionam de ponta a ponta: **Tela → API Flask → Controller → Service → Model/Repository → Banco de Dados**.

**Acesso e usuários**
1. Cadastrar usuário (Administrador ou Funcionário)
2. Fazer login e logout
3. Aprovar cadastro de funcionário (feito pelo Administrador)
4. Listar, atualizar e inativar funcionários

**Estoque**
5. Cadastrar e remover produtos e categorias
6. Registrar entrada de estoque (cria o lote ou soma em lote de mesma validade)
7. Registrar saída de estoque (baixa pelo lote que vence primeiro, FEFO)
8. Ler QR Code / código de barras pela câmera para localizar o produto
9. Consultar o estoque detalhado, por produto e por lote
10. Consultar o histórico de movimentações, com filtros por período e por tipo

**Alertas**
11. Alertar produtos com estoque abaixo do mínimo
12. Alertar lotes que vencem nos próximos 7 dias
13. Exibir o resumo da tela de Início (itens cadastrados, estoque baixo e vencendo)

**Cardápio**
14. Cadastrar tipo de culinária
15. Cadastrar prato com seus ingredientes
16. Listar e remover pratos
17. Verificar a disponibilidade dos ingredientes de um prato no estoque
18. Preparar prato, abatendo automaticamente os ingredientes do estoque

**Compras e fornecedores**
19. Gerar a lista de compras (produtos abaixo do mínimo, agrupados por categoria)
20. Compartilhar a lista de compras com o fornecedor por WhatsApp ou Gmail
21. Cadastrar, listar, atualizar e remover fornecedores

**Inteligência artificial**
22. Sugerir pratos com IA a partir do estoque, priorizando o que vence primeiro

**Consentimento**
23. Exibir o termo de consentimento da câmera e registrar a decisão do usuário

## Bônus

- **Integração de IA como serviço:** a sugestão de pratos (`SugerirPratosService`) envia o estoque real ao Google Gemini e recebe de volta de 3 a 5 pratos em JSON, com modo de preparo e ingredientes marcados como disponíveis ou em falta.
- **Termo de consentimento com decisão registrada:** antes de usar a câmera para ler QR Code, o usuário vê o termo. A decisão (aceitou ou recusou) é gravada no banco, por usuário, no campo `camera_autorizada`, e consultada nas próximas vezes pela API `/api/camera-consentimento`.

## Como executar o projeto

1º Crie o banco de dados executando `backend/database/rodar_tudo_de_uma_vez.sql` no seu MySQL.

2º Abra `backend/config.py` e configure o acesso ao MySQL (`SQLALCHEMY_DATABASE_URI`, no formato `mysql+pymysql://USUARIO:SENHA@localhost:3306/stockchef`) e a chave da IA (`GEMINI_API_KEY`, que também pode ser definida como variável de ambiente).

3º Instale as dependências:

```bash
pip install -r requirements.txt
```

4º Execute o backend:

```bash
python app.py
```

A aplicação ficará disponível em `http://127.0.0.1:5000`, e o navegador abre sozinho na tela de login.
