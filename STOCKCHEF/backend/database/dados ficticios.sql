USE stockchef;

-- Limpar dados anteriores para evitar conflitos de chaves estrangeiras
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE movimentacao_lotes;
TRUNCATE TABLE movimentacao_itens;
TRUNCATE TABLE movimentacoes;
TRUNCATE TABLE prato_ingredientes;
TRUNCATE TABLE pratos;
TRUNCATE TABLE lotes;
TRUNCATE TABLE produtos;
TRUNCATE TABLE usuarios;
SET FOREIGN_KEY_CHECKS = 1;

-- =============================================================================
-- 1. USUÁRIOS
-- =============================================================================
INSERT INTO usuarios (id_usuario, nome, email, senha, tipo, ativo) VALUES
(1, 'Carlos Oliveira', 'carlos@zenith.com', 'senha_hash_1', 'Administrador', TRUE);

-- =============================================================================
-- 2. PRODUTOS (Vinculados ao ADM Carlos - ID: 1)
-- =============================================================================
-- Inserindo produtos com estoque mínimo para validar os cenários de compras e estoque
INSERT INTO produtos (id_produto, id_usuario, nome, descricao, id_categoria, id_unidade, estoque_minimo) VALUES
(1, 1, 'Filé Mignon', 'Corte bovino premium', 1, 1, 15.00),     -- Mínimo: 15kg
(2, 1, 'Queijo Mozzarela', 'Queijo fatiado', 2, 1, 10.00),       -- Mínimo: 10kg
(3, 1, 'Molho de Tomate', 'Lata de molho pronto', 4, 3, 20.00),  -- Mínimo: 20un
(4, 1, 'Camarão Rosa', 'Camarão limpo congelado', 1, 1, 8.00);    -- Mínimo: 8kg

-- =============================================================================
-- 3. LOTES (Cenários controlados para ativar TODOS os gatilhos das consultas)
-- =============================================================================
INSERT INTO lotes (id_lote, id_produto, numero_lote, validade, quantidade_inicial, quantidade_atual, custo_unitario, data_entrada) VALUES
-- Produto 1 (Filé Mignon): Total 18kg. Acima do mínimo (15kg), mas possui um lote que vence em 3 dias!
-- (Valida: Lotes vencendo em 7 dias no Dashboard)
(1, 1, 'LOT-FM-01', DATE_ADD(CURDATE(), INTERVAL 15 DAY), 10.00, 10.00, 45.00, NOW()),
(2, 1, 'LOT-FM-02', DATE_ADD(CURDATE(), INTERVAL 3 DAY),  10.00, 8.00,  47.00, NOW()), 

-- Produto 2 (Queijo Mozzarela): Total 4kg. Abaixo do mínimo (10kg). Lote com validade OK.
-- (Valida: Estoque Baixo no Dashboard, Estoque e Compras)
(3, 2, 'LOT-QM-01', DATE_ADD(CURDATE(), INTERVAL 20 DAY), 10.00, 4.00,  28.00, NOW()),

-- Produto 3 (Molho de Tomate): Total 0un. Totalmente zerado!
-- (Valida: Estoque Zerado no módulo de Compras e Estoque Baixo)
(4, 3, 'LOT-MT-01', DATE_ADD(CURDATE(), INTERVAL 30 DAY), 15.00, 0.00,  4.50, NOW()),

-- Produto 4 (Camarão Rosa): Total 5kg. Possui um lote já VENCIDO há 2 dias com saldo restante.
-- (Valida: Status de Lote Vencido na consulta de Compras)
(5, 4, 'LOT-CR-01', DATE_SUB(CURDATE(), INTERVAL 2 DAY),  10.00, 5.00,  60.00, NOW());

-- =============================================================================
-- 4. CARDÁPIO (Pratos vinculados ao ADM Carlos - ID: 1)
-- =============================================================================
INSERT INTO pratos (id_prato, id_usuario, nome, id_tipo_culinaria, tempo_preparo, rendimento, modo_preparo) VALUES
(1, 1, 'Filé à Parmegiana', 1, 35, 2, 'Grelhar o filé, cobrir com molho e queijo e gratinar.'),
(2, 1, 'Risoto de Camarão', 1, 30, 2, 'Cozinhar o arroz arbóreo e adicionar os camarões grelhados.');

-- =============================================================================
-- 5. HISTÓRICO DE MOVIMENTAÇÕES (Registros temporais estratégicos)
-- =============================================================================
-- Movimentação 1: Ocorrida HOJE (Entrada)
INSERT INTO movimentacoes (id_movimentacao, id_usuario, tipo, data_movimentacao) VALUES
(1, 1, 'Entrada', NOW());

INSERT INTO movimentacao_itens (id_movimentacao_item, id_movimentacao, id_produto, quantidade) VALUES
(1, 1, 1, 20.00); -- Entrada de 20kg de Filé Mignon hoje

-- Movimentação 2: Ocorrida HOJE (Saída)
INSERT INTO movimentacoes (id_movimentacao, id_usuario, tipo, data_movimentacao) VALUES
(2, 1, 'Saida', NOW());

INSERT INTO movimentacao_itens (id_movimentacao_item, id_movimentacao, id_produto, quantidade) VALUES
(2, 2, 1, 2.00); -- Saída de 2kg de Filé Mignon hoje

-- Movimentação 3: Ocorrida há 3 dias atrás (Dentro de "ESTA SEMANA", mas não hoje)
INSERT INTO movimentacoes (id_movimentacao, id_usuario, tipo, data_movimentacao) VALUES
(3, 1, 'Entrada', DATE_SUB(NOW(), INTERVAL 3 DAY));

INSERT INTO movimentacao_itens (id_movimentacao_item, id_movimentacao, id_produto, quantidade) VALUES
(3, 3, 2, 10.00); -- Entrada de 10kg de Queijo há 3 dias









-- 1. Dashboard Inicial (Deve retornar: 4 itens cadastrados, 3 com estoque baixo/zerado, 1 lote vencendo em 7 dias)
CALL sp_dashboard_inicio(1);

-- 2. Listagem de Estoque (Retorna os 4 produtos mapeando as somas e categorias corretamente)
CALL sp_listar_estoque(1);

-- 3. Lista de Compras (Retornará o Queijo como 'Estoque Baixo', o Molho como 'Estoque Zerado' e o Camarão como 'Possui Lote Vencido')
CALL sp_produtos_para_comprar(1);

-- 4. Cardápio por Categoria (Retorna os pratos da categoria 'Italiana')
CALL sp_filtrar_cardapio_por_categoria(1, 'Italiana');

-- 5. Histórico - Filtro: HOJE (Retorna apenas os registros criados na data atual)
CALL sp_historico_movimentacoes(1, 'HOJE', 'TODAS');

-- 6. Histórico - Filtro: ESTA SEMANA (Retorna os registros de hoje + o registro de 3 dias atrás)
CALL sp_historico_movimentacoes(1, 'ESTA SEMANA', 'TODAS');