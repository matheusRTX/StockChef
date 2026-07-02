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