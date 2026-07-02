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