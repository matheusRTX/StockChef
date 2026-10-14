# Pith / StockChef - Sistema de Controle de Estoque para Restaurantes

Este repositório apresenta o sistema Pith (StockChef), com:

- Backend em Flask;
- SQLAlchemy como ORM, com o objeto `db` centralizado em `models/usuario.py`;
- Models herdando de `db.Model`, cada uma com seu próprio CRUD (`criar`, `buscar_por_id`, `listar_todos`, `atualizar`, `deletar`, com soft delete quando aplicável);
- Controllers implementados como classes, responsáveis por receber as requisições HTTP e devolver a resposta, com o Blueprint atuando apenas como camada de registro das rotas;
- Services organizados por caso de uso (um arquivo por operação, ex.: `CriarProdutoService`, `PrepararPratoService`);
- Senhas do banco e demais segredos lidos de variáveis de ambiente (`.env`), fora do repositório;
- Autenticação por sessão, com perfis Administrador e Funcionário (o Funcionário precisa ser aprovado pelo Administrador do estabelecimento);
- Frontend em HTML, CSS e JavaScript, servido pelo Flask e consumindo a API via `fetch()`;
- Script SQL para criação do banco MySQL.

## Estrutura do projeto

```text
pith/
├── app.py
├── requirements.txt
├── .env.example
├── docs/
│   ├── diagrama_de_classes.md
│   ├── diagrama_de_classes.png
│   ├── diagrama_de_classes.svg
│   └── diagrama_de_classes.mmd
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
Model (backend/models)
   ↓
Banco de Dados (MySQL)
```

## Diagrama de classes

O diagrama de classes do domínio (Models, atributos, relacionamentos, herança, composição e agregação) está em:

- [`docs/diagrama_de_classes.md`](docs/diagrama_de_classes.md) (explicação + diagrama em Mermaid);
- [`docs/diagrama_de_classes.png`](docs/diagrama_de_classes.png) (imagem) e [`docs/diagrama_de_classes.svg`](docs/diagrama_de_classes.svg) (vetorial).

## Funcionalidades Implementadas

Todas as funcionalidades abaixo estão disponíveis de ponta a ponta:
**Tela → API Flask → Controller → Service → Model → Banco de Dados**.

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

## Como executar o projeto

1º Crie o banco de dados executando `backend/database/rodar_tudo_de_uma_vez.sql` no seu MySQL.

2º Crie o arquivo `.env` na raiz do projeto, copiando o modelo `.env.example`, e preencha os valores de acesso ao MySQL:

```bash
cp .env.example .env
```

O arquivo `.env` está no `.gitignore` e **não deve ser enviado ao repositório**.

3º Instale as dependências:

```bash
pip install -r requirements.txt
```

4º Execute o backend:

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

O servidor já abre o navegador automaticamente na tela de login.
