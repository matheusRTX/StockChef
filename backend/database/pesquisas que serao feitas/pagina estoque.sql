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