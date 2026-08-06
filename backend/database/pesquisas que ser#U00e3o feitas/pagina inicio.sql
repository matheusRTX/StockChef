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
      AND l.quantidade_atual > 0
      AND l.validade BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY);
END $$

DELIMITER ;




-- Saber apenas o total de produtos da empresa:
CALL sp_inicio_total_cadastrados(1);

-- Saber apenas quantos produtos estão operando abaixo do mínimo:
CALL sp_inicio_total_estoque_baixo(1);

-- Saber apenas quantos lotes ativos vão vencer na próxima semana:
CALL sp_inicio_total_vencendo_7_dias(1);


