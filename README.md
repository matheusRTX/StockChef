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

## Funcionalidades Implementadas

Usuários / Autenticação:

1. Cadastrar usuário (Administrador ou Funcionário), via `CadastrarUsuarioService`;
2. Fazer login (e-mail e senha, com senha em hash), via `AutenticarUsuarioService`;
3. Encerrar sessão (logout);
4. Listar usuários, via `ListarUsuariosService`;
5. Atualizar usuário, via `AtualizarUsuarioService`;
6. Desativar usuário, via `DesativarUsuarioService`.

Categorias de produto (`/api/categorias`):

7. Criar categoria;
8. Listar categorias;
9. Buscar categoria por ID;
10. Atualizar categoria;
11. Remover categoria.

Unidades de medida (`/api/unidades-medida`):

12. Criar unidade de medida;
13. Listar unidades de medida;
14. Buscar unidade de medida por ID;
15. Atualizar unidade de medida;
16. Remover unidade de medida.

Produtos (`/api/produtos`):

17. Criar produto (com categoria, unidade e estoque mínimo);
18. Listar produtos;
19. Buscar produto por ID;
20. Atualizar produto;
21. Remover produto.

Lotes (`/api/lotes`):

22. Criar lote de produto (com controle de validade e quantidade);
23. Listar lotes (com filtro por produto);
24. Buscar lote por ID;
25. Atualizar lote;
26. Remover lote.

Movimentações de estoque (`/api/movimentacoes`):

27. Registrar movimentação de entrada/saída (com itens);
28. Listar movimentações;
29. Buscar movimentação por ID;
30. Atualizar movimentação;
31. Remover movimentação.

Tipos de culinária (`/api/tipos-culinaria`):

32. Criar tipo de culinária;
33. Listar tipos de culinária;
34. Buscar tipo de culinária por ID;
35. Atualizar tipo de culinária;
36. Remover tipo de culinária.

Pratos e ingredientes (`/api/pratos`):

37. Criar prato;
38. Listar pratos (com filtro de favoritos);
39. Buscar prato por ID;
40. Atualizar prato;
41. Remover prato;
42. Adicionar ingrediente a um prato;
43. Listar ingredientes de um prato;
44. Atualizar ingrediente de um prato;
45. Remover ingrediente de um prato;
46. Verificar disponibilidade de ingredientes em estoque para um prato;
47. Preparar um prato, abatendo automaticamente os ingredientes do estoque.

Estoque (`/api/estoque/listar`):

48. Consultar estoque detalhado por produto/lote, usando stored procedure.

Dashboard de início (`/api/inicio/*`):

49. Consultar resumo geral do estoque;
50. Consultar itens com estoque baixo;
51. Consultar itens vencendo em 7 dias;
52. Consultar últimas movimentações.

Navegação (protegida por login):

53. Acessar as páginas Início, Cardápio, Compras, Pratos, QR Code e Estoque.

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
