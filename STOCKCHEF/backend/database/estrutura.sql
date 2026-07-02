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