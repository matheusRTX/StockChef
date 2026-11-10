USE stockchef;

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

DROP PROCEDURE IF EXISTS sp_historico_listar_movimentacoes;

DELIMITER $$

CREATE PROCEDURE sp_historico_listar_movimentacoes(
    IN p_id_adm INT,
    IN p_filtro_data INT,
    IN p_filtro_tipo INT
)
BEGIN
    SELECT 
        p.nome AS nome_produto,
        m.data_movimentacao AS data_registro,
        m.tipo AS tipo_movimentacao,
        c.nome AS categoria,
        u.sigla AS unidade,
        mi.quantidade AS quantidade_movimentada
    FROM movimentacoes m
    INNER JOIN movimentacao_itens mi ON m.id_movimentacao = mi.id_movimentacao
    INNER JOIN produtos p ON mi.id_produto = p.id_produto
    INNER JOIN categorias c ON p.id_categoria = c.id_categoria
    INNER JOIN unidades_medida u ON p.id_unidade = u.id_unidade
    WHERE p.id_usuario = p_id_adm
      
      AND (
          p_filtro_tipo = 2 
          OR (p_filtro_tipo = 0 AND m.tipo = 'Entrada')
          OR (p_filtro_tipo = 1 AND m.tipo = 'Saida')
      )
      
      AND (
          p_filtro_data = 2
          OR (p_filtro_data = 0 AND DATE(m.data_movimentacao) = CURDATE())
          OR (p_filtro_data = 1 AND m.data_movimentacao >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY))
      )
      
    ORDER BY m.data_movimentacao DESC;
END $$

DELIMITER ;




CALL sp_historico_listar_movimentacoes(1, 0, 2);

CALL sp_historico_listar_movimentacoes(1, 1, 0);

CALL sp_historico_listar_movimentacoes(1, 2, 1);