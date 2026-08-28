# StockChef - Sistema de Controle de Estoque para Restaurantes

Este repositório apresenta o sistema StockChef, com:

- Backend em Flask;
- Persistência com **SQL puro** via driver nativo **PyMySQL** (sem ORM/SQLAlchemy);
- Módulo central de conexão (`backend/database/connection.py`) gerenciando cursores de dicionário (`DictCursor`) e transações;
- Models representados por **Data Classes (`@dataclass`)** puras em Python com o método `from_row()`;
- Repositories (`ProdutoRepository`, `CategoriaRepository`, `UsuarioRepository`, etc.) encapsulando consultas SQL parametrizadas e execução de stored procedures do banco;
- Controllers implementados como classes, responsáveis por receber as requisições HTTP e renderizar as páginas, com o Blueprint atuando como camada de registro das rotas;
- Services organizados por caso de uso (um arquivo por operação, ex.: `CriarProdutoService`, `AtualizarProdutoService`);
- Autenticação por sessão (login e cadastro de usuário);
- Frontend em HTML, CSS e JavaScript, servido diretamente pelo Flask e consumindo a API via `fetch()`;
- Scripts SQL para criação do banco MySQL e carga de dados.

## Estrutura do projeto

```text
StockChef/
├── frontend/
│   ├── html/
│   ├── css/
│   ├── js/
│   └── imagens/
└── backend/
    ├── app.py
    ├── requirements.txt
    ├── config.py
    ├── controllers/
    │   ├── auth_controller.py
    │   ├── categoria_controller.py
    │   ├── unidade_medida_controller.py
    │   ├── produto_controller.py
    │   ├── lote_controller.py
    │   ├── movimentacao_controller.py
    │   ├── tipo_culinaria_controller.py
    │   ├── prato_controller.py
    │   └── estoque_controller.py
    ├── database/
    │   ├── connection.py
    │   ├── dados ficticios/
    │   ├── estrutura do banco/
    │   ├── pesquisas que serao feitas/
    │   ├── procedures/
    │   └── rodar_tudo_de_uma_vez.sql
    ├── models/
    ├── repositories/
    └── services/
        ├── categoria/
        ├── lote/
        ├── movimentacao/
        ├── prato/
        ├── prato_ingrediente/
        ├── produto/
        ├── tipo_culinaria/
        ├── unidade_medida/
        └── usuario/
