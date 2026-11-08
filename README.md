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
Controller (backend/controllers) — recebe a requisição, confere o login, devolve JSON
   ↓                                   ↓
Service (backend/services)         Repository (backend/repositories)
 casos de uso e regras              consultas ao banco via procedures
   ↓                                   ↓
Model (backend/models)                 |
 classes SQLAlchemy (db.Model)         |
   ↓                                   ↓
Banco de Dados (MySQL) ←───────────────┘
```

- **Models:** cada classe herda `db.Model`, com `criar`, `buscar_por_id`, `listar_todos`, `atualizar` e `deletar` (soft delete quando aplicável).
- **Controllers:** classes que recebem a requisição HTTP e devolvem a resposta; o Blueprint só registra as rotas.
- **Services:** um caso de uso por arquivo (ex.: `CriarProdutoService`, `PrepararPratoService`), com as regras da aplicação.
- **Repositories:** executam as consultas de leitura do estoque, do histórico e da tela de Início (`CALL sp_...`), sempre parametrizadas.
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

## Funcionalidades Implementadas

Todas as funcionalidades abaixo estão disponíveis de ponta a ponta, da tela ao banco de dados. As operações de escrita seguem **Tela → API Flask → Controller → Service → Model → Banco de Dados**; as consultas de estoque, histórico e alertas passam pelo **Repository**.

1. Cadastrar usuário (Administrador ou Funcionário)
2. Fazer login
3. Listar funcionários do estabelecimento
4. Aprovar cadastro de funcionário
5. Atualizar funcionário
6. Inativar funcionário
7. Cadastrar produto
8. Remover produto
9. Registrar movimentação de entrada/saída de estoque
10. Cadastrar categoria de produto
11. Cadastrar tipo de culinária
12. Cadastrar prato com seus ingredientes
13. Listar pratos do cardápio
14. Remover prato
15. Verificar disponibilidade dos ingredientes de um prato no estoque
16. Preparar prato, abatendo automaticamente os ingredientes do estoque
17. Cadastrar fornecedor
18. Listar fornecedores
19. Atualizar fornecedor
20. Remover fornecedor

**Além das 20 acima, o sistema também implementa:**

21. Ler QR Code / código de barras pela câmera para localizar o produto
22. Baixar o estoque pelo lote que vence primeiro (FEFO) nas saídas e no preparo de pratos
23. Consultar o estoque detalhado, por produto e por lote
24. Consultar o histórico de movimentações, com filtros por período e por tipo
25. Alertar produtos com estoque abaixo do mínimo
26. Alertar lotes que vencem nos próximos 7 dias
27. Gerar a lista de compras (produtos abaixo do mínimo, agrupados por categoria)
28. Compartilhar a lista de compras com o fornecedor por WhatsApp ou Gmail
29. Sugerir pratos com IA a partir do estoque, priorizando o que vence primeiro
30. Exibir o termo de consentimento da câmera e registrar o aceite do usuário

## Bônus

- **Integração de IA como serviço:** a sugestão de pratos (`SugerirPratosService`) envia o estoque real ao Google Gemini e recebe de volta de 3 a 5 pratos em JSON, com modo de preparo e ingredientes marcados como disponíveis ou em falta.
- **Termo de consentimento com decisão registrada:** antes de usar a câmera para ler QR Code, o usuário vê o termo e escolhe Aceitar ou Recusar. O aceite é gravado no banco, por usuário, no campo `camera_autorizada`, e consultado nas próximas vezes pela API `/api/camera-consentimento`, de modo que o termo não é exibido de novo. Se o usuário recusa, a câmera não é aberta e o termo volta a ser apresentado na próxima tentativa.

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
