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



