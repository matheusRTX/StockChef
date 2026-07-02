
### MÓDULO: INÍCIO
-- Consulta 1: Total de itens cadastrados
CALL sp_inicio_total_cadastrados(1);

-- Consulta 2: Total de itens com estoque baixo
CALL sp_inicio_total_estoque_baixo(1);

-- Consulta 3: Total de lotes vencendo em 7 dias
CALL sp_inicio_total_vencendo_7_dias(1);




### MÓDULO: ESTOQUE
-- Lista o estoque atualizado (Nome, categoria, quantidade, valor mínimo)
CALL sp_listar_estoque(1);



### MÓDULO: COMPRAS
-- Produtos abaixo do estoque mínimo ou vencidos (Nome, status do alerta, quantidade atual, mínimo necessário)
CALL sp_produtos_para_comprar(1);



### MÓDULO: CARDÁPIO
-- Filtrar pratos por uma categoria específica (Ex: 'Italiana')
CALL sp_filtrar_cardapio_por_categoria(1, 'Italiana');
-- Mostrar o cardápio completo de todas as categorias
CALL sp_filtrar_cardapio_por_categoria(1, '');


### MÓDULO: HISTÓRICO
-- Consulta 1: Total acumulado de Entradas
CALL sp_historico_total_entradas(1);
-- Consulta 2: Total acumulado de Saídas
CALL sp_historico_total_saidas(1);

-- Consulta 3: Listagem de movimentações com filtros numéricos
-- Legenda Data: 0 = HOJE | 1 = ESTA SEMANA | 2 = TODAS
-- Legenda Tipo: 0 = Entrada | 1 = Saída | 2 = TODAS

-- Exemplo: Movimentações (Entradas e Saídas) de HOJE
CALL sp_historico_listar_movimentacoes(1, 0, 2);

-- Exemplo: Apenas as ENTRADAS que ocorreram ESTA SEMANA
CALL sp_historico_listar_movimentacoes(1, 1, 0);

-- Exemplo: Apenas as SAÍDAS de TODO o histórico
CALL sp_historico_listar_movimentacoes(1, 2, 1);

-- Exemplo: Relatório completo (Tudo de todas as datas)
CALL sp_historico_listar_movimentacoes(1, 2, 2);
