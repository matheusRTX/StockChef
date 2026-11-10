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



CALL sp_listar_estoque(1);






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














USE stockchef;

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



CALL sp_inicio_total_cadastrados(1);

CALL sp_inicio_total_estoque_baixo(1);

CALL sp_inicio_total_vencendo_7_dias(1);

CALL sp_inicio_total_vencendo_7_dias_lista(2);







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
      AND (p_nome_categoria IS NULL OR p_nome_categoria = '' OR tc.nome LIKE CONCAT('%', p_nome_categoria, '%'));
END $$

DELIMITER ;


CALL sp_filtrar_cardapio_por_categoria(1, 'Italiana');



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

CALL sp_listar_estoque_detalhado(1);



