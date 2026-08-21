# Pith - Sistema de Controle de Estoque para Restaurantes

Este repositório apresenta o sistema Pith, com:

- Backend em Flask;
- SQLAlchemy como ORM, com o objeto `db` centralizado em `models/usuario.py`;
- Models herdando de `db.Model`, cada uma com seu próprio CRUD (`criar`, `buscar_por_id`, `listar_todos`, `atualizar`, `deletar`, com soft delete);
- Controllers implementados como classes, responsáveis por receber as requisições HTTP e renderizar as páginas, com o Blueprint atuando apenas como camada de registro das rotas;
- Services organizados por caso de uso (um arquivo por operação, ex.: `CriarProdutoService`, `AtualizarProdutoService`);
- Repositories (`EstoqueRepository`, `InicioRepository`) encapsulando chamadas a stored procedures do banco;
- Autenticação por sessão (login e cadastro de usuário);
- Frontend em HTML, CSS e JavaScript, servido diretamente pelo Flask e consumindo a API real via `fetch()`;
- Script SQL para criação do banco MySQL.

## Estrutura do projeto

```text
pith/
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
    ├── models/
    ├── repositories/
    ├── services/
    │   ├── categoria/
    │   ├── lote/
    │   ├── movimentacao/
    │   ├── prato/
    │   ├── prato_ingrediente/
    │   ├── produto/
    │   ├── tipo_culinaria/
    │   ├── unidade_medida/
    │   └── usuario/
    └── database/
        └── rodar_tudo_de_uma_vez.sql
```

## Arquitetura usada no projeto

```text
Frontend (templates em frontend/html, JS consumindo /api/*)
   ↓
Controller (backend/controllers) — classes registradas via Blueprint
   ↓
Service (backend/services) — uma classe por caso de uso
   ↓
Model (backend/models) / Repository (backend/repositories, para stored procedures)
   ↓
Banco de Dados (MySQL)
```

## Funcionalidades implementadas

Autenticação:

- Cadastrar usuário (tipo Administrador ou Funcionário), via `CadastrarUsuarioService`;
- Fazer login (e-mail e senha, com senha em hash), via `AutenticarUsuarioService`;
- Encerrar sessão (logout).

Categorias de produto (CRUD completo via `/api/categorias`):

- Criar, listar, buscar, atualizar e remover categorias.

Unidades de medida (CRUD completo via `/api/unidades-medida`):

- Criar, listar, buscar, atualizar e remover unidades de medida.

Produtos (CRUD completo via `/api/produtos`):

- Criar, listar, buscar, atualizar e remover produtos, com categoria, unidade e estoque mínimo.

Lotes (CRUD completo via `/api/lotes`):

- Criar, listar (com filtro por produto), buscar, atualizar e remover lotes, incluindo controle de validade e quantidade.

Movimentações de estoque (CRUD completo via `/api/movimentacoes`):

- Registrar entrada/saída (com itens), listar, buscar, atualizar e remover movimentações.

Tipos de culinária (CRUD completo via `/api/tipos-culinaria`):

- Criar, listar, buscar, atualizar e remover tipos de culinária.

Pratos e ingredientes (CRUD completo via `/api/pratos`):

- Criar, listar (com filtro de favoritos), buscar, atualizar e remover pratos;
- Adicionar, listar, atualizar e remover ingredientes de um prato;
- Verificar disponibilidade de ingredientes em estoque para um prato;
- Preparar um prato, abatendo automaticamente os ingredientes do estoque.

Estoque (via `/api/estoque/listar`):

- Consulta do estoque detalhado por produto/lote, usando stored procedure.

Dashboard de início (via `/api/inicio/*`):

- Resumo geral, itens com estoque baixo, itens vencendo em 7 dias e últimas movimentações.

Navegação (protegida por login):

- Início, Cardápio, Compras, Pratos, QR Code e Estoque.

## Como executar o projeto

1º Crie o banco de dados executando `rodar_tudo_de_uma_vez.sql` no seu MySQL.

2º configure sua conexão do MySQL (ver `backend/config.py`).

3º instale as dependências:

```bash
pip install -r backend/requirements.txt
```

4° Execute o backend:

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

O servidor já abre o navegador automaticamente na tela de login.

## Rotas da aplicação

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Tela de login (página inicial) |
| GET, POST | `/login` | Autentica o usuário |
| GET, POST | `/cadastro` | Cadastra um novo usuário |
| GET | `/inicio` | Página inicial do sistema (requer login) |
| GET | `/cardapio` | Página de cardápio (requer login) |
| GET | `/compras` | Página de compras (requer login) |
| GET | `/pratos` | Página de pratos (requer login) |
| GET | `/qrcode` | Página de QR Code (requer login) |
| GET | `/estoque` | Página de estoque (requer login) |
| GET | `/logout` | Encerra a sessão do usuário |
| GET/POST/PUT/DELETE | `/api/categorias`, `/api/unidades-medida`, `/api/produtos`, `/api/lotes`, `/api/movimentacoes`, `/api/tipos-culinaria`, `/api/pratos` | CRUD de cada recurso (requer login) |
| GET | `/api/estoque/listar` | Estoque detalhado (requer login) |
| GET | `/api/inicio/resumo`, `/api/inicio/estoque-baixo`, `/api/inicio/vencendo`, `/api/inicio/movimentacoes` | Dados do dashboard de início (requer login) |
