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