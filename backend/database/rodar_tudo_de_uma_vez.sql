DROP DATABASE IF EXISTS stockchef;
CREATE DATABASE stockchef;
USE stockchef;

/*==========================================================
USUÁRIOS
==========================================================*/
CREATE TABLE usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('Administrador','Funcionario') NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (id_usuario)
) ENGINE=InnoDB;


/*==========================================================
CATEGORIAS
==========================================================*/
CREATE TABLE categorias (
    id_categoria INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(80) NOT NULL,
    descricao VARCHAR(255),
    PRIMARY KEY (id_categoria)
) ENGINE=InnoDB;

/*==========================================================
UNIDADES DE MEDIDA
==========================================================*/
CREATE TABLE unidades_medida (
    id_unidade INT NOT NULL AUTO_INCREMENT,
    sigla VARCHAR(10) NOT NULL,
    descricao VARCHAR(60) NOT NULL,
    PRIMARY KEY (id_unidade)
) ENGINE=InnoDB;

/*==========================================================
PRODUTOS
==========================================================*/
CREATE TABLE produtos (
    id_produto INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL, -- ADICIONE ESTA LINHA AQUI
    nome VARCHAR(120) NOT NULL,
    descricao TEXT,
    codigo_barras VARCHAR(100),
    qr_code VARCHAR(255),
    id_categoria INT NOT NULL,
    id_unidade INT NOT NULL,
    estoque_minimo DECIMAL(10,2) NOT NULL DEFAULT 0,
    imagem VARCHAR(255),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id_produto)
) ENGINE=InnoDB;

/*==========================================================
LOTES
==========================================================*/
CREATE TABLE lotes (
    id_lote INT NOT NULL AUTO_INCREMENT,
    id_produto INT NOT NULL,
    numero_lote VARCHAR(60),
    validade DATE NOT NULL,
    quantidade_inicial DECIMAL(10,2) NOT NULL,
    quantidade_atual DECIMAL(10,2) NOT NULL,
    custo_unitario DECIMAL(10,2),
    data_entrada DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    PRIMARY KEY (id_lote)
) ENGINE=InnoDB;

/*==========================================================
MOVIMENTAÇÕES
==========================================================*/
CREATE TABLE movimentacoes (
    id_movimentacao INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    tipo ENUM('Entrada','Saida','Ajuste') NOT NULL,
    data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    PRIMARY KEY (id_movimentacao)
) ENGINE=InnoDB;

/*==========================================================
ITENS DA MOVIMENTAÇÃO
==========================================================*/
CREATE TABLE movimentacao_itens (
    id_movimentacao_item INT NOT NULL AUTO_INCREMENT,
    id_movimentacao INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_movimentacao_item)
) ENGINE=InnoDB;

/*==========================================================
LOTES UTILIZADOS NA MOVIMENTAÇÃO
==========================================================*/
CREATE TABLE movimentacao_lotes (
    id_movimentacao_lote INT NOT NULL AUTO_INCREMENT,
    id_movimentacao_item INT NOT NULL,
    id_lote INT NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_movimentacao_lote)
) ENGINE=InnoDB;

/*==========================================================
TIPOS DE CULINÁRIA
==========================================================*/
CREATE TABLE tipos_culinaria (
    id_tipo_culinaria INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255),
    PRIMARY KEY (id_tipo_culinaria)
) ENGINE=InnoDB;

/*==========================================================
PRATOS
==========================================================*/
CREATE TABLE pratos (
    id_prato INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL, -- ADICIONE ESTA LINHA AQUI
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    id_tipo_culinaria INT NOT NULL,
    tempo_preparo INT NOT NULL,
    rendimento INT NOT NULL,
    modo_preparo LONGTEXT NOT NULL,
    favorito BOOLEAN NOT NULL DEFAULT FALSE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    imagem VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id_prato)
) ENGINE=InnoDB;

/*==========================================================
INGREDIENTES DOS PRATOS
==========================================================*/
CREATE TABLE prato_ingredientes (
    id_prato_ingrediente INT NOT NULL AUTO_INCREMENT,
    id_prato INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    observacao VARCHAR(255),
    PRIMARY KEY (id_prato_ingrediente)
) ENGINE=InnoDB;

/*==========================================================
FORNECEDORES
==========================================================*/
CREATE TABLE fornecedores (
    id_fornecedor INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL, -- Coluna adicionada para vincular ao Administrador da Empresa
    nome VARCHAR(150) NOT NULL,
    telefone VARCHAR(25),
    email VARCHAR(150),
    endereco VARCHAR(255),
    contato VARCHAR(100),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    observacao TEXT,
    PRIMARY KEY (id_fornecedor),
    -- Criação do vínculo com a tabela de usuários
    CONSTRAINT fk_fornecedores_usuario 
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

/*==========================================================
FORNECEDOR x PRODUTO (Tabela Associativa)
==========================================================*/
CREATE TABLE fornecedor_produto (
    id_fornecedor INT NOT NULL,
    id_produto INT NOT NULL,
    preco DECIMAL(10,2),
    prazo_entrega INT,
    PRIMARY KEY (id_fornecedor, id_produto)
) ENGINE=InnoDB;

/*==========================================================
FORNECEDOR x CATEGORIA (Tabela Associativa)
==========================================================*/
CREATE TABLE fornecedor_categoria (
    id_fornecedor INT NOT NULL,
    id_categoria INT NOT NULL,
    PRIMARY KEY (id_fornecedor, id_categoria)
) ENGINE=InnoDB;

/*==========================================================
LISTAS DE COMPRAS
==========================================================*/
CREATE TABLE listas_compras (
    id_lista_compras INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Aberta','Enviada','Finalizada','Cancelada') DEFAULT 'Aberta',
    observacao TEXT,
    PRIMARY KEY (id_lista_compras)
) ENGINE=InnoDB;

/*==========================================================
ITENS DA LISTA DE COMPRAS
==========================================================*/
CREATE TABLE lista_compras_itens (
    id_lista_compras_item INT NOT NULL AUTO_INCREMENT,
    id_lista_compras INT NOT NULL,
    id_produto INT NOT NULL,
    id_fornecedor INT,
    quantidade DECIMAL(10,2) NOT NULL,
    motivo ENUM('Estoque Baixo','Produto Zerado','Produto Vencido','Compra Manual') NOT NULL,
    comprado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id_lista_compras_item)
) ENGINE=InnoDB;

/*==========================================================
CONFIGURAÇÕES DO SISTEMA
==========================================================*/
CREATE TABLE configuracoes (
    id_configuracao INT NOT NULL AUTO_INCREMENT,
    nome_empresa VARCHAR(150),
    email_empresa VARCHAR(150),
    telefone VARCHAR(25),
    endereco VARCHAR(255),
    logo VARCHAR(255),
    api_whatsapp VARCHAR(255),
    api_email VARCHAR(255),
    PRIMARY KEY (id_configuracao)
) ENGINE=InnoDB;

/*==========================================================
CONFIGURAÇÕES DA IA
==========================================================*/
CREATE TABLE configuracoes_ia (
    id_configuracao_ia INT NOT NULL AUTO_INCREMENT,
    considerar_validade BOOLEAN DEFAULT TRUE,
    considerar_estoque BOOLEAN DEFAULT TRUE,
    considerar_cardapio BOOLEAN DEFAULT TRUE,
    considerar_culinaria BOOLEAN DEFAULT TRUE,
    dias_alerta_validade INT DEFAULT 7,
    peso_validade INT DEFAULT 10,
    peso_estoque INT DEFAULT 5,
    peso_favoritos INT DEFAULT 3,
    PRIMARY KEY (id_configuracao_ia)
) ENGINE=InnoDB;

/*==========================================================
HISTÓRICO DAS SUGESTÕES DA IA
==========================================================*/
CREATE TABLE historico_sugestoes (
    id_historico_sugestao INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_prato INT NOT NULL,
    tipo ENUM('Cardapio','Culinaria','Estoque','Validade') NOT NULL,
    pontuacao DECIMAL(10,2),
    motivo TEXT,
    data_sugestao DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_historico_sugestao)
) ENGINE=InnoDB;

/*==========================================================
HISTÓRICO DE ENVIOS
==========================================================*/
CREATE TABLE historico_envios (
    id_historico_envio INT NOT NULL AUTO_INCREMENT,
    id_lista_compras INT NOT NULL,
    id_fornecedor INT NOT NULL,
    tipo ENUM('WhatsApp','Email') NOT NULL,
    status ENUM('Sucesso','Erro') NOT NULL,
    resposta TEXT,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_historico_envio)
) ENGINE=InnoDB;



/* PRODUTOS */
ALTER TABLE produtos
ADD CONSTRAINT fk_produto_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE produtos
ADD CONSTRAINT fk_produto_unidade
FOREIGN KEY (id_unidade) REFERENCES unidades_medida(id_unidade)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* LOTES */
ALTER TABLE lotes
ADD CONSTRAINT fk_lote_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE CASCADE;

/* MOVIMENTAÇÕES */
ALTER TABLE movimentacoes
ADD CONSTRAINT fk_movimentacao_usuario
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* MOVIMENTAÇÃO ITENS */
ALTER TABLE movimentacao_itens
ADD CONSTRAINT fk_mov_item_movimentacao
FOREIGN KEY (id_movimentacao) REFERENCES movimentacoes(id_movimentacao)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE movimentacao_itens
ADD CONSTRAINT fk_mov_item_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* MOVIMENTAÇÃO LOTES */
ALTER TABLE movimentacao_lotes
ADD CONSTRAINT fk_mov_lote_item
FOREIGN KEY (id_movimentacao_item) REFERENCES movimentacao_itens(id_movimentacao_item)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE movimentacao_lotes
ADD CONSTRAINT fk_mov_lote_lote
FOREIGN KEY (id_lote) REFERENCES lotes(id_lote)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* PRATOS */
ALTER TABLE pratos
ADD CONSTRAINT fk_prato_culinaria
FOREIGN KEY (id_tipo_culinaria) REFERENCES tipos_culinaria(id_tipo_culinaria)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* PRATO INGREDIENTES */
ALTER TABLE prato_ingredientes
ADD CONSTRAINT fk_prato_ingrediente_prato
FOREIGN KEY (id_prato) REFERENCES pratos(id_prato)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE prato_ingredientes
ADD CONSTRAINT fk_prato_ingrediente_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* FORNECEDOR PRODUTO */
ALTER TABLE fornecedor_produto
ADD CONSTRAINT fk_fornecedor_produto_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE fornecedor_produto
ADD CONSTRAINT fk_fornecedor_produto_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE CASCADE;

/* FORNECEDOR CATEGORIA */
ALTER TABLE fornecedor_categoria
ADD CONSTRAINT fk_fornecedor_categoria_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE fornecedor_categoria
ADD CONSTRAINT fk_fornecedor_categoria_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
ON UPDATE CASCADE ON DELETE CASCADE;

/* LISTAS DE COMPRAS */
ALTER TABLE listas_compras
ADD CONSTRAINT fk_lista_usuario
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* LISTA DE COMPRAS ITENS */
ALTER TABLE lista_compras_itens
ADD CONSTRAINT fk_lista_item_lista
FOREIGN KEY (id_lista_compras) REFERENCES listas_compras(id_lista_compras)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE lista_compras_itens
ADD CONSTRAINT fk_lista_item_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE lista_compras_itens
ADD CONSTRAINT fk_lista_item_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE SET NULL;

/* HISTÓRICO DE SUGESTÕES */
ALTER TABLE historico_sugestoes
ADD CONSTRAINT fk_hist_usuario
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE historico_sugestoes
ADD CONSTRAINT fk_hist_prato
FOREIGN KEY (id_prato) REFERENCES pratos(id_prato)
ON UPDATE CASCADE ON DELETE CASCADE;

/* HISTÓRICO DE ENVIOS */
ALTER TABLE historico_envios
ADD CONSTRAINT fk_envio_lista
FOREIGN KEY (id_lista_compras) REFERENCES listas_compras(id_lista_compras)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE historico_envios
ADD CONSTRAINT fk_envio_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE CASCADE;


USE stockchef;

-- Limpar dados anteriores para evitar conflitos de chaves estrangeiras
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE movimentacao_lotes;
TRUNCATE TABLE movimentacao_itens;
TRUNCATE TABLE movimentacoes;
TRUNCATE TABLE prato_ingredientes;
TRUNCATE TABLE pratos;
TRUNCATE TABLE lotes;
TRUNCATE TABLE produtos;
TRUNCATE TABLE usuarios;
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- 1. USUÁRIOS
-- =============================================================================
INSERT INTO usuarios (id_usuario, nome, email, senha, tipo, ativo) VALUES
(1, 'Carlos Oliveira', 'matheusmoreiradinizz@gmail.com', 'scrypt:32768:8:1$GpR3BPBcEGRmwikO$2f0f2eacd96ddc57f7d77a2e3c4cf0482733f2331983cde278945bdc705b74362130f9cb17f27e738136cac3147ff1ba3947ab29a973a1153c8985218b937e60', 'Administrador', TRUE);



-- =============================================================================
-- CATEGORIAS
-- =============================================================================
INSERT INTO categorias (id_categoria, nome, descricao) VALUES
(1, 'Carnes', 'Carnes bovinas, suínas, aves, peixes e frutos do mar.'),
(2, 'Laticínios', 'Leites, queijos, manteiga, creme de leite e derivados.'),
(3, 'Hortifrúti', 'Frutas, verduras, legumes e vegetais frescos.'),
(4, 'Mercearia', 'Produtos industrializados, enlatados, molhos, temperos e alimentos não perecíveis.');


-- =============================================================================
-- UNIDADES DE MEDIDA
-- =============================================================================
INSERT INTO unidades_medida (id_unidade, sigla, descricao) VALUES
(1, 'kg', 'Quilograma'),
(2, 'g',  'Grama'),
(3, 'un', 'Unidade'),
(4, 'L',  'Litro'),
(5, 'mL', 'Mililitro'),
(6, 'cx', 'Caixa'),
(7, 'pct','Pacote'),
(8, 'fd', 'Fardo'),
(9, 'dz', 'Dúzia'),
(10,'sc', 'Saco');

INSERT INTO tipos_culinaria (id_tipo_culinaria, nome, descricao) VALUES
(1, 'Italiana', 'Pratos típicos da culinária italiana.'),
(2, 'Brasileira', 'Pratos tradicionais da culinária brasileira.'),
(3, 'Francesa', 'Pratos da culinária francesa.'),
(4, 'Japonesa', 'Pratos da culinária japonesa.');

-- =============================================================================
-- 2. PRODUTOS (Vinculados ao ADM Carlos - ID: 1)
-- =============================================================================
-- Inserindo produtos com estoque mínimo para validar os cenários de compras e estoque
INSERT INTO produtos (id_produto, id_usuario, nome, descricao, id_categoria, id_unidade, estoque_minimo) VALUES
(1, 1, 'Filé Mignon', 'Corte bovino premium', 1, 1, 15.00),     -- Mínimo: 15kg
(2, 1, 'Queijo Mozzarela', 'Queijo fatiado', 2, 1, 10.00),       -- Mínimo: 10kg
(3, 1, 'Molho de Tomate', 'Lata de molho pronto', 4, 3, 20.00),  -- Mínimo: 20un
(4, 1, 'Camarão Rosa', 'Camarão limpo congelado', 1, 1, 8.00);    -- Mínimo: 8kg

-- =============================================================================
-- 3. LOTES (Cenários controlados para ativar TODOS os gatilhos das consultas)
-- =============================================================================
INSERT INTO lotes (id_lote, id_produto, numero_lote, validade, quantidade_inicial, quantidade_atual, custo_unitario, data_entrada) VALUES
-- Produto 1 (Filé Mignon): Total 18kg. Acima do mínimo (15kg), mas possui um lote que vence em 3 dias!
-- (Valida: Lotes vencendo em 7 dias no Dashboard)
(1, 1, 'LOT-FM-01', DATE_ADD(CURDATE(), INTERVAL 15 DAY), 10.00, 10.00, 45.00, NOW()),
(2, 1, 'LOT-FM-02', DATE_ADD(CURDATE(), INTERVAL 3 DAY),  10.00, 8.00,  47.00, NOW()), 

-- Produto 2 (Queijo Mozzarela): Total 4kg. Abaixo do mínimo (10kg). Lote com validade OK.
-- (Valida: Estoque Baixo no Dashboard, Estoque e Compras)
(3, 2, 'LOT-QM-01', DATE_ADD(CURDATE(), INTERVAL 20 DAY), 10.00, 4.00,  28.00, NOW()),

-- Produto 3 (Molho de Tomate): Total 0un. Totalmente zerado!
-- (Valida: Estoque Zerado no módulo de Compras e Estoque Baixo)
(4, 3, 'LOT-MT-01', DATE_ADD(CURDATE(), INTERVAL 30 DAY), 15.00, 0.00,  4.50, NOW()),

-- Produto 4 (Camarão Rosa): Total 5kg. Possui um lote já VENCIDO há 2 dias com saldo restante.
-- (Valida: Status de Lote Vencido na consulta de Compras)
(5, 4, 'LOT-CR-01', DATE_SUB(CURDATE(), INTERVAL 2 DAY),  10.00, 5.00,  60.00, NOW());

-- =============================================================================
-- 4. CARDÁPIO (Pratos vinculados ao ADM Carlos - ID: 1)
-- =============================================================================
INSERT INTO pratos (id_prato, id_usuario, nome, id_tipo_culinaria, tempo_preparo, rendimento, modo_preparo) VALUES
(1, 1, 'Filé à Parmegiana', 1, 35, 2, 'Grelhar o filé, cobrir com molho e queijo e gratinar.'),
(2, 1, 'Risoto de Camarão', 1, 30, 2, 'Cozinhar o arroz arbóreo e adicionar os camarões grelhados.');

-- =============================================================================
-- 5. HISTÓRICO DE MOVIMENTAÇÕES (Registros temporais estratégicos)
-- =============================================================================
-- Movimentação 1: Ocorrida HOJE (Entrada)
INSERT INTO movimentacoes (id_movimentacao, id_usuario, tipo, data_movimentacao) VALUES
(1, 1, 'Entrada', NOW());

INSERT INTO movimentacao_itens (id_movimentacao_item, id_movimentacao, id_produto, quantidade) VALUES
(1, 1, 1, 20.00); -- Entrada de 20kg de Filé Mignon hoje

-- Movimentação 2: Ocorrida HOJE (Saída)
INSERT INTO movimentacoes (id_movimentacao, id_usuario, tipo, data_movimentacao) VALUES
(2, 1, 'Saida', NOW());

INSERT INTO movimentacao_itens (id_movimentacao_item, id_movimentacao, id_produto, quantidade) VALUES
(2, 2, 1, 2.00); -- Saída de 2kg de Filé Mignon hoje

-- Movimentação 3: Ocorrida há 3 dias atrás (Dentro de "ESTA SEMANA", mas não hoje)
INSERT INTO movimentacoes (id_movimentacao, id_usuario, tipo, data_movimentacao) VALUES
(3, 1, 'Entrada', DATE_SUB(NOW(), INTERVAL 3 DAY));

INSERT INTO movimentacao_itens (id_movimentacao_item, id_movimentacao, id_produto, quantidade) VALUES
(3, 3, 2, 10.00); -- Entrada de 10kg de Queijo há 3 dias





-- =============================================================================
-- MÓDULO: COMPRAS
-- =============================================================================
-- Descrição: Identifica e lista os produtos do ADM que necessitam de atenção 
--            por estarem abaixo do estoque mínimo ou com algum lote vencido.
--            Informa se está zerado, abaixo do mínimo ou vencido com as quantidades.
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_produtos_para_comprar;

DELIMITER $$

CREATE PROCEDURE sp_produtos_para_comprar(IN p_id_adm INT)
BEGIN
    SELECT 
        p.nome AS produto,
        CASE 
            -- Caso a soma de todos os lotes seja exatamente 0
            WHEN COALESCE(SUM(l.quantidade_atual), 0) = 0 THEN 'Estoque Zerado'
            -- Caso possua quantidade em estoque mas a data mínima de validade seja menor que hoje
            WHEN MIN(l.validade) < CURDATE() AND SUM(CASE WHEN l.validade < CURDATE() THEN l.quantidade_atual ELSE 0 END) > 0 THEN 'Possui Lote Vencido'
            -- Caso esteja apenas abaixo do mínimo configurado
            WHEN COALESCE(SUM(l.quantidade_atual), 0) < p.estoque_minimo THEN 'Estoque Baixo'
            ELSE 'Necessita Atenção'
        END AS status_alerta,
        COALESCE(SUM(l.quantidade_atual), 0) AS quantidade_disponivel,
        p.estoque_minimo AS minimo_necessario
    FROM produtos p
    LEFT JOIN lotes l ON p.id_produto = l.id_produto
    WHERE p.id_usuario = p_id_adm 
      AND p.ativo = TRUE
    GROUP BY p.id_produto, p.nome, p.estoque_minimo
    -- Filtra apenas produtos que batem com os critérios de atenção (abaixo do mínimo ou vencidos)
    HAVING COALESCE(SUM(l.quantidade_atual), 0) < p.estoque_minimo 
       OR MIN(l.validade) < CURDATE();
END $$

DELIMITER ;


-- Para listar as sugestões de Compras/Reposição do ADM 1:
CALL sp_produtos_para_comprar(1);








-- =============================================================================
-- MÓDULO: ESTOQUE
-- =============================================================================
-- Descrição: Lista a posição atual de estoque de cada produto associado ao ADM, 
--            mostrando o nome, a categoria correspondente, o saldo total somado 
--            de todos os lotes e o valor mínimo configurado.
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_listar_estoque;

DELIMITER $$

CREATE PROCEDURE sp_listar_estoque(IN p_id_adm INT)
BEGIN
    SELECT 
        p.nome AS produto,
        c.nome AS categoria,
        COALESCE(SUM(l.quantidade_atual), 0) AS quantidade,
        p.estoque_minimo AS valor_minimo
    FROM produtos p
    INNER JOIN categorias c ON p.id_categoria = c.id_categoria
    LEFT JOIN lotes l ON p.id_produto = l.id_produto
    WHERE p.id_usuario = p_id_adm 
      AND p.ativo = TRUE
    GROUP BY p.id_produto, p.nome, c.nome, p.estoque_minimo;
END $$

DELIMITER ;



-- Para listar a tabela de Estoque do ADM 1:
CALL sp_listar_estoque(1);






USE stockchef;

-- =============================================================================
-- MÓDULO HISTÓRICO: CONSULTA 1 - TOTAL ACUMULADO DE ENTRADAS
-- =============================================================================
-- Descrição: Soma a quantidade total de produtos que deram entrada no estoque 
--            da empresa associada ao ADM informado (Histórico Geral).
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_historico_total_entradas;

DELIMITER $$

CREATE PROCEDURE sp_historico_total_entradas(IN p_id_adm INT)
BEGIN
    SELECT COALESCE(SUM(mi.quantidade), 0) AS total_acumulado_entradas
    FROM movimentacoes m
    INNER JOIN movimentacao_itens mi ON m.id_movimentacao = mi.id_movimentacao
    INNER JOIN produtos p ON mi.id_produto = p.id_produto
    WHERE p.id_usuario = p_id_adm
      AND m.tipo = 'Entrada';
END $$

DELIMITER ;


-- =============================================================================
-- MÓDULO HISTÓRICO: CONSULTA 2 - TOTAL ACUMULADO DE SAÍDAS
-- =============================================================================
-- Descrição: Soma a quantidade total de produtos que saíram do estoque 
--            da empresa associada ao ADM informado (Histórico Geral).
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_historico_total_saidas;

DELIMITER $$

CREATE PROCEDURE sp_historico_total_saidas(IN p_id_adm INT)
BEGIN
    SELECT COALESCE(SUM(mi.quantidade), 0) AS total_acumulado_saidas
    FROM movimentacoes m
    INNER JOIN movimentacao_itens mi ON m.id_movimentacao = mi.id_movimentacao
    INNER JOIN produtos p ON mi.id_produto = p.id_produto
    WHERE p.id_usuario = p_id_adm
      AND m.tipo = 'Saida';
END $$

DELIMITER ;


USE stockchef;

-- =============================================================================
-- MÓDULO HISTÓRICO: CONSULTA 3 - LISTAGEM DE MOVIMENTAÇÕES COM FILTROS NUMÉRICOS
-- =============================================================================
-- Descrição: Retorna a lista detalhada de movimentações da empresa utilizando 
--            códigos numéricos (0, 1, 2) para os filtros, otimizando o desempenho.
--
-- PARÂMETROS DE DATA (p_filtro_data):
--   0 = HOJE         -> Filtra apenas os registros do dia atual.
--   1 = ESTA SEMANA  -> Filtra os registros desde a segunda-feira desta semana.
--   2 = TODAS        -> Não aplica filtro de data (traz todo o histórico).
--
-- PARÂMETROS DE TIPO (p_filtro_tipo):
--   0 = Entrada      -> Traz apenas as movimentações de entrada de estoque.
--   1 = Saída        -> Traz apenas as movimentações de saída de estoque.
--   2 = TODAS        -> Não aplica filtro de tipo (traz entradas e saídas).
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_historico_listar_movimentacoes;

DELIMITER $$

CREATE PROCEDURE sp_historico_listar_movimentacoes(
    IN p_id_adm INT,
    IN p_filtro_data INT, -- Recebe 0 (Hoje), 1 (Esta Semana) ou 2 (Todas)
    IN p_filtro_tipo INT  -- Recebe 0 (Entrada), 1 (Saída) ou 2 (Todas)
)
BEGIN
    SELECT 
        p.nome AS nome_produto,
        m.data_movimentacao AS data_registro,
        m.tipo AS tipo_movimentacao,
        c.nome AS categoria,
        mi.quantidade AS quantidade_movimentada
    FROM movimentacoes m
    INNER JOIN movimentacao_itens mi ON m.id_movimentacao = mi.id_movimentacao
    INNER JOIN produtos p ON mi.id_produto = p.id_produto
    INNER JOIN categorias c ON p.id_categoria = c.id_categoria
    WHERE p.id_usuario = p_id_adm
      
      -- =======================================================================
      -- REGRA DO FILTRO DE TIPO DE MOVIMENTAÇÃO (Entrada / Saída)
      -- =======================================================================
      -- Se p_filtro_tipo for 2, a primeira parte é verdadeira e ignora o filtro.
      -- Se for 0, obriga o m.tipo a ser 'Entrada'.
      -- Se for 1, obriga o m.tipo a ser 'Saida'.
      AND (
          p_filtro_tipo = 2 
          OR (p_filtro_tipo = 0 AND m.tipo = 'Entrada')
          OR (p_filtro_tipo = 1 AND m.tipo = 'Saida')
      )
      
      -- =======================================================================
      -- REGRA DO FILTRO DE PERÍODO (Data)
      -- =======================================================================
      -- Se p_filtro_data for 2, a primeira parte é verdadeira e traz tudo.
      -- Se for 0, compara apenas o DIA, MES e ANO da movimentação com a data de hoje.
      -- Se for 1, busca datas maiores ou iguais à segunda-feira da semana atual 
      -- (WEEKDAY retorna 0 para segunda, 1 para terça... subtraindo isso da data atual, achamos a segunda-feira).
      AND (
          p_filtro_data = 2
          OR (p_filtro_data = 0 AND DATE(m.data_movimentacao) = CURDATE())
          OR (p_filtro_data = 1 AND m.data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY))
      )
      
    -- Ordena as movimentações mostrando as mais recentes primeiro
    ORDER BY m.data_movimentacao DESC;
END $$

DELIMITER ;




-- Exemplo 1: Buscar tudo o que entrou ou saiu HOJE
-- ID do ADM = 1, Data = 0 (HOJE), Tipo = 2 (TODAS)
CALL sp_historico_listar_movimentacoes(1, 0, 2);

-- Exemplo 2: Buscar apenas as ENTRADAS que aconteceram ESTA SEMANA
-- ID do ADM = 1, Data = 1 (ESTA SEMANA), Tipo = 0 (Entrada)
CALL sp_historico_listar_movimentacoes(1, 1, 0);

-- Exemplo 3: Buscar todas as SAÍDAS de todo o histórico do sistema
-- ID do ADM = 1, Data = 2 (TODAS), Tipo = 1 (Saida)
CALL sp_historico_listar_movimentacoes(1, 2, 1);














USE stockchef;

-- =============================================================================
-- MÓDULO INÍCIO: CONSULTA 1 - TOTAL DE ITENS CADASTRADOS
-- =============================================================================
-- Descrição: Retorna a quantidade exata de produtos ativos cadastrados no 
--            sistema que pertencem especificamente à empresa do ADM informado.
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_inicio_total_cadastrados;

DELIMITER $$

CREATE PROCEDURE sp_inicio_total_cadastrados(IN p_id_adm INT)
BEGIN
    SELECT COUNT(*) AS total_itens_cadastrados 
    FROM produtos 
    WHERE id_usuario = p_id_adm 
      AND ativo = TRUE;
END $$

DELIMITER ;


-- =============================================================================
-- MÓDULO INÍCIO: CONSULTA 2 - TOTAL DE ITENS COM ESTOQUE BAIXO
-- =============================================================================
-- Descrição: Calcula a soma da quantidade_atual de todos os lotes de cada produto.
--            Se essa soma total for menor do que o 'estoque_minimo' configurado 
--            no produto, ele entra na contagem de estoque baixo da empresa.
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_inicio_total_estoque_baixo;

DELIMITER $$

CREATE PROCEDURE sp_inicio_total_estoque_baixo(IN p_id_adm INT)
BEGIN
    SELECT COUNT(*) AS total_itens_estoque_baixo
    FROM (
        SELECT p.id_produto
        FROM produtos p
        LEFT JOIN lotes l ON p.id_produto = l.id_produto
        WHERE p.id_usuario = p_id_adm 
          AND p.ativo = TRUE
        GROUP BY p.id_produto, p.estoque_minimo
        HAVING COALESCE(SUM(l.quantidade_atual), 0) < p.estoque_minimo
    ) AS produtos_abaixo_do_minimo;
END $$

DELIMITER ;


-- =============================================================================
-- MÓDULO INÍCIO: CONSULTA 3 - TOTAL DE LOTES VENCENDO EM 7 DIAS
-- =============================================================================
-- Descrição: Retorna o total de lotes da empresa que ainda possuem mercadoria 
--            em estoque (quantidade_atual > 0) e cuja data de validade está 
--            dentro do intervalo dos próximos 7 dias (inclusive hoje).
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_inicio_total_vencendo_7_dias;

DELIMITER $$

CREATE PROCEDURE sp_inicio_total_vencendo_7_dias(IN p_id_adm INT)
BEGIN
    SELECT COUNT(*) AS total_lotes_vencendo_7_dias
    FROM lotes l
    INNER JOIN produtos p ON l.id_produto = p.id_produto
    WHERE p.id_usuario = p_id_adm
      AND p.ativo = TRUE
      AND l.quantidade_atual > 0
      AND l.validade <= DATE_ADD(CURDATE(), INTERVAL 7 DAY);
END $$

DELIMITER ;




DROP PROCEDURE IF EXISTS sp_inicio_total_vencendo_7_dias_lista;

DELIMITER $$

CREATE PROCEDURE sp_inicio_total_vencendo_7_dias_lista(IN p_id_adm INT)
BEGIN

    SELECT 
        l.id_lote,
        l.id_produto,
        p.nome AS produto,
        l.numero_lote,
        l.validade,
        l.quantidade_atual,
        l.custo_unitario
    FROM lotes l
    INNER JOIN produtos p ON l.id_produto = p.id_produto
    WHERE p.id_usuario = p_id_adm
      AND p.ativo = TRUE
      AND l.quantidade_atual > 0
      AND l.validade <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
    ORDER BY l.validade ASC;

END $$

DELIMITER ;



-- Saber apenas o total de produtos da empresa:
CALL sp_inicio_total_cadastrados(1);

-- Saber apenas quantos produtos estão operando abaixo do mínimo:
CALL sp_inicio_total_estoque_baixo(1);

-- Saber apenas quantos lotes ativos vão vencer na próxima semana:
CALL sp_inicio_total_vencendo_7_dias(1);

-- Saber apenas a lista dos produtos que vão vencer na próxima semana:
CALL sp_inicio_total_vencendo_7_dias_lista(2);







-- =============================================================================
-- MÓDULO: CARDÁPIO
-- =============================================================================
-- Descrição: Mostra os pratos de acordo com a sua categoria (tipo_culinaria).
--            Se o parâmetro de categoria for passado como NULL ou vazio (''), 
--            a procedure retornará todo o cardápio ativo pertencente ao ADM.
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_filtrar_cardapio_por_categoria;

DELIMITER $$

CREATE PROCEDURE sp_filtrar_cardapio_por_categoria(
    IN p_id_adm INT,
    IN p_nome_categoria VARCHAR(100)
)
BEGIN
    SELECT 
        pr.nome AS prato,
        tc.nome AS tipo_culinaria,
        pr.tempo_preparo,
        pr.rendimento,
        pr.modo_preparo
    FROM pratos pr
    INNER JOIN tipos_culinaria tc ON pr.id_tipo_culinaria = tc.id_tipo_culinaria
    WHERE pr.id_usuario = p_id_adm 
      AND pr.ativo = TRUE
      -- Se o parâmetro for nulo ou vazio traz todas as categorias, senão filtra pelo nome enviado
      AND (p_nome_categoria IS NULL OR p_nome_categoria = '' OR tc.nome LIKE CONCAT('%', p_nome_categoria, '%'));
END $$

DELIMITER ;


-- Para listar o Cardápio filtrando pela categoria 'Italiana' do ADM 1:
CALL sp_filtrar_cardapio_por_categoria(1, 'Italiana');



-- =============================================================================
-- MÓDULO ESTOQUE: LISTAGEM DETALHADA (PRODUTO + LOTES)
-- =============================================================================
-- Descrição: Retorna uma linha por lote de cada produto ativo do ADM
--            informado (produtos sem lote aparecem com as colunas de lote
--            em NULL). O agrupamento por produto é feito na aplicação.
-- =============================================================================

DROP PROCEDURE IF EXISTS sp_listar_estoque_detalhado;

DELIMITER $$

CREATE PROCEDURE sp_listar_estoque_detalhado(IN p_id_adm INT)
BEGIN
    SELECT
        p.id_produto,
        p.nome AS produto,
        c.nome AS categoria,
        u.sigla AS unidade,
        p.estoque_minimo AS valor_minimo,
        l.id_lote,
        l.numero_lote,
        l.quantidade_atual,
        l.validade
    FROM produtos p
    INNER JOIN categorias c ON p.id_categoria = c.id_categoria
    INNER JOIN unidades_medida u ON p.id_unidade = u.id_unidade
    LEFT JOIN lotes l ON p.id_produto = l.id_produto
    WHERE p.id_usuario = p_id_adm
      AND p.ativo = TRUE
    ORDER BY p.nome, l.validade;
END $$

DELIMITER ;

-- Para listar o Estoque detalhado (com lotes) do ADM 1:
CALL sp_listar_estoque_detalhado(1);




