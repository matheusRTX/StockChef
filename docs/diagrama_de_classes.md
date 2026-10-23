# Diagrama de Classes do Domínio

Diagrama das classes implementadas em `backend/models/` e seus relacionamentos.
Ele é coerente com as Models do backend e com o banco (`backend/database/estrutura do banco/create_database.sql`).

Arquivos desta pasta:

- `diagrama_de_classes.png` — imagem pronta para visualização;
- `diagrama_de_classes.svg` — versão vetorial;
- `diagrama_de_classes.mmd` — código-fonte em Mermaid (o bloco abaixo é o mesmo, e o GitHub o renderiza automaticamente).

![Diagrama de classes](diagrama_de_classes.png)

## Como ler o diagrama

| Conceito | Onde aparece |
|---|---|
| **Herança** | Todas as 12 Models herdam de `db.Model` (SQLAlchemy). Está indicado pelo estereótipo `«db.Model»` em cada classe. |
| **Composição** (◆) | `Movimentacao` → `MovimentacaoItem` → `MovimentacaoLote`, e `Prato` → `PratoIngrediente`. A parte não faz sentido sem o todo. |
| **Agregação** (◇) | `Usuario` (Administrador) → `Usuario` (Funcionários, auto-relacionamento por `id_estabelecimento`) e `Produto` → `Lote`. |
| **Associação** (→) | Chaves estrangeiras entre as demais classes (ex.: `Categoria` → `Produto`, `TipoCulinaria` → `Prato`). |
| **Muitos-para-muitos** | `Fornecedor` ↔ `Categoria`, pela tabela associativa `fornecedor_categoria` (sem Model própria; o acesso fica em `Fornecedor.definir_categoria()` e `Fornecedor.buscar_categoria()`). |

Observações:

- O diagrama representa apenas o **domínio** (Models). Controllers, Services e Repositories não entram aqui.
- Os métodos listados são os de persistência de cada Model (`criar`, `buscar_por_id`, `listar_todos`, `atualizar`, `deletar` e consultas específicas).
- `Usuario`, `Produto`, `Prato` e `Fornecedor` fazem *soft delete* (campo `ativo`).

## Código-fonte (Mermaid)

```mermaid
classDiagram
    direction TB

    note "Herança: todas as classes herdam de db.Model (SQLAlchemy), indicado pelo estereótipo db.Model."

    class Usuario {
        <<db.Model>>
        +int id_usuario
        +str nome
        +str email
        +str senha
        +str tipo
        +bool ativo
        +str codigo_estabelecimento
        +int id_estabelecimento
        +str status
        +criar()
        +buscar_por_id()
        +buscar_por_email()
        +buscar_por_codigo_estabelecimento()
        +listar_todos()
        +listar_funcionarios_do_estabelecimento()
        +atualizar()
        +deletar()
    }

    class Categoria {
        <<db.Model>>
        +int id_categoria
        +str nome
        +str descricao
        +criar()
        +buscar_por_id()
        +listar_todos()
        +atualizar()
        +deletar()
    }

    class UnidadeMedida {
        <<db.Model>>
        +int id_unidade
        +str sigla
        +str descricao
        +criar()
        +buscar_por_id()
        +listar_todos()
        +atualizar()
        +deletar()
    }

    class Produto {
        <<db.Model>>
        +int id_produto
        +int id_usuario
        +str nome
        +str descricao
        +str codigo_barras
        +str qr_code
        +int id_categoria
        +int id_unidade
        +Decimal estoque_minimo
        +str imagem
        +bool ativo
        +criar()
        +buscar_por_id()
        +listar_todos()
        +listar_por_usuario()
        +atualizar()
        +deletar()
    }

    class Lote {
        <<db.Model>>
        +int id_lote
        +int id_produto
        +str numero_lote
        +date validade
        +Decimal quantidade_inicial
        +Decimal quantidade_atual
        +Decimal custo_unitario
        +datetime data_entrada
        +str observacao
        +criar()
        +buscar_por_id()
        +listar_todos()
        +listar_por_produto()
        +atualizar()
        +deletar()
    }

    class Movimentacao {
        <<db.Model>>
        +int id_movimentacao
        +int id_usuario
        +str tipo
        +datetime data_movimentacao
        +str observacao
        +criar()
        +buscar_por_id()
        +listar_todos()
        +listar_por_usuario()
        +atualizar()
        +deletar()
    }

    class MovimentacaoItem {
        <<db.Model>>
        +int id_movimentacao_item
        +int id_movimentacao
        +int id_produto
        +Decimal quantidade
        +criar()
        +buscar_por_id()
        +listar_todos()
        +listar_por_movimentacao()
        +atualizar()
        +deletar()
    }

    class MovimentacaoLote {
        <<db.Model>>
        +int id_movimentacao_lote
        +int id_movimentacao_item
        +int id_lote
        +Decimal quantidade
        +criar()
        +buscar_por_id()
        +listar_todos()
        +listar_por_item()
        +atualizar()
        +deletar()
    }

    class TipoCulinaria {
        <<db.Model>>
        +int id_tipo_culinaria
        +str nome
        +str descricao
        +criar()
        +buscar_por_id()
        +listar_todos()
        +atualizar()
        +deletar()
    }

    class Prato {
        <<db.Model>>
        +int id_prato
        +int id_usuario
        +str nome
        +str descricao
        +int id_tipo_culinaria
        +int tempo_preparo
        +int rendimento
        +str modo_preparo
        +bool favorito
        +bool ativo
        +str imagem
        +criar()
        +buscar_por_id()
        +listar_todos()
        +listar_por_usuario()
        +listar_favoritos()
        +atualizar()
        +deletar()
    }

    class PratoIngrediente {
        <<db.Model>>
        +int id_prato_ingrediente
        +int id_prato
        +int id_produto
        +Decimal quantidade
        +str observacao
        +criar()
        +buscar_por_id()
        +listar_todos()
        +listar_por_prato()
        +atualizar()
        +deletar()
    }

    class Fornecedor {
        <<db.Model>>
        +int id_fornecedor
        +int id_usuario
        +str nome
        +str telefone
        +str email
        +str endereco
        +str contato
        +bool ativo
        +str observacao
        +criar()
        +buscar_por_id()
        +listar_por_usuario()
        +atualizar()
        +deletar()
        +definir_categoria()
        +buscar_categoria()
    }

    %% Agregação (o "todo" não é dono do ciclo de vida da parte)
    Usuario "1" o-- "0..*" Usuario : funcionários (id_estabelecimento)
    Produto "1" o-- "0..*" Lote : possui lotes

    %% Composição (a parte não existe sem o todo)
    Movimentacao "1" *-- "1..*" MovimentacaoItem : itens
    MovimentacaoItem "1" *-- "0..*" MovimentacaoLote : lotes afetados
    Prato "1" *-- "1..*" PratoIngrediente : ingredientes

    %% Associações
    Usuario "1" --> "0..*" Produto : cadastra
    Usuario "1" --> "0..*" Fornecedor : cadastra
    Usuario "1" --> "0..*" Prato : cadastra
    Usuario "1" --> "0..*" Movimentacao : registra
    Categoria "1" --> "0..*" Produto : classifica
    UnidadeMedida "1" --> "0..*" Produto : mede
    MovimentacaoItem "0..*" --> "1" Produto : refere-se a
    MovimentacaoLote "0..*" --> "1" Lote : abate / soma
    PratoIngrediente "0..*" --> "1" Produto : usa
    TipoCulinaria "1" --> "0..*" Prato : classifica
    Fornecedor "0..*" -- "0..*" Categoria : fornecedor_categoria
```
