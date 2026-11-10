
CALL sp_inicio_total_cadastrados(1);

CALL sp_inicio_total_estoque_baixo(1);

CALL sp_inicio_total_vencendo_7_dias(1);




CALL sp_listar_estoque(1);



CALL sp_produtos_para_comprar(1);



CALL sp_filtrar_cardapio_por_categoria(1, 'Italiana');
CALL sp_filtrar_cardapio_por_categoria(1, '');


CALL sp_historico_total_entradas(1);
CALL sp_historico_total_saidas(1);

CALL sp_historico_listar_movimentacoes(1, 0, 2);

CALL sp_historico_listar_movimentacoes(1, 1, 0);

CALL sp_historico_listar_movimentacoes(1, 2, 1);

CALL sp_historico_listar_movimentacoes(1, 2, 2);
