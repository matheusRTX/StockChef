DROP PROCEDURE IF EXISTS sp_produtos_para_comprar;

DELIMITER $$

CREATE PROCEDURE sp_produtos_para_comprar(IN p_id_adm INT)
BEGIN
    SELECT 
        p.nome AS produto,
        CASE 
            WHEN COALESCE(SUM(l.quantidade_atual), 0) = 0 THEN 'Estoque Zerado'
            WHEN MIN(l.validade) < CURDATE() AND SUM(CASE WHEN l.validade < CURDATE() THEN l.quantidade_atual ELSE 0 END) > 0 THEN 'Possui Lote Vencido'
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
    HAVING COALESCE(SUM(l.quantidade_atual), 0) < p.estoque_minimo 
       OR MIN(l.validade) < CURDATE();
END $$

DELIMITER ;


CALL sp_produtos_para_comprar(1);