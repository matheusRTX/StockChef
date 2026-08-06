# Pith - Sistema de Controle de Estoque para Restaurantes

Este repositório apresenta o sistema Pith, com:

- Backend em Flask, organizado com o padrão *application factory* (`create_app`);
- SQLAlchemy como ORM, com o objeto `db` centralizado em `models/database.py`;
- Model herdando de `db.Model`, com os métodos de persistência (`salvar`, buscas);
- Controllers para receber requisições HTTP e renderizar as páginas;
- Services organizados por caso de uso (um arquivo por operação);
- Autenticação por sessão (login e cadastro de usuário);
- Configuração via variáveis de ambiente (`.env`);
- Frontend em HTML, CSS e JavaScript, servido diretamente pelo Flask;
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
    ├── .env.example
    ├── controllers/
    │   └── auth_controller.py
    ├── models/
    │   ├── database.py
    │   └── usuario.py
    ├── repositories/
    ├── services/
    │   ├── login_usuario_service.py
    │   └── cadastrar_usuario_service.py
    └── database/
        └── create_database.sql
```

## Arquitetura usada no projeto

```text
Frontend (templates em frontend/html)
   ↓
Controller (backend/controllers)
   ↓
Service (backend/services)
   ↓
Model (backend/models)
   ↓
Banco de Dados (MySQL)
```

## Funcionalidades implementadas

Autenticação:

- Cadastrar usuário (tipo Administrador ou Funcionário), via `CadastrarUsuarioService`;
- Fazer login (e-mail e senha, com senha em hash), via `LoginUsuarioService`;
- Encerrar sessão (logout).

Navegação (protegida por login):

- Início;
- Cardápio;
- Compras;
- Pratos;
- QR Code.

## Como executar o projeto

O frontend não roda separado: o próprio Flask serve as páginas HTML e os arquivos estáticos (CSS, JS, imagens). Só é necessário rodar o backend.

1º Crie o banco de dados executando `database/create_database.sql` no seu MySQL.

2º configure sua conexão do mysql no app.py

3º instale as dependencias:
flask_sqlalchemy, pymysql e werkzeug

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
| GET | `/logout` | Encerra a sessão do usuário |

## Observações

- As páginas **Estoque** e **Histórico** ainda não foram criadas; os links do menu para elas estão desativados (`#`) até que os arquivos e rotas correspondentes sejam criados.
- As credenciais do banco de dados agora ficam no arquivo `.env`.
