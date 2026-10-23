
/* PRODUTOS */
ALTER TABLE produtos
ADD CONSTRAINT fk_produto_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE produtos
ADD CONSTRAINT fk_produto_unidade
FOREIGN KEY (id_unidade) REFERENCES unidades_medida(id_unidade)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* LOTES */
ALTER TABLE lotes
ADD CONSTRAINT fk_lote_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE CASCADE;

/* MOVIMENTAÇÕES */
ALTER TABLE movimentacoes
ADD CONSTRAINT fk_movimentacao_usuario
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* MOVIMENTAÇÃO ITENS */
ALTER TABLE movimentacao_itens
ADD CONSTRAINT fk_mov_item_movimentacao
FOREIGN KEY (id_movimentacao) REFERENCES movimentacoes(id_movimentacao)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE movimentacao_itens
ADD CONSTRAINT fk_mov_item_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* MOVIMENTAÇÃO LOTES */
ALTER TABLE movimentacao_lotes
ADD CONSTRAINT fk_mov_lote_item
FOREIGN KEY (id_movimentacao_item) REFERENCES movimentacao_itens(id_movimentacao_item)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE movimentacao_lotes
ADD CONSTRAINT fk_mov_lote_lote
FOREIGN KEY (id_lote) REFERENCES lotes(id_lote)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* PRATOS */
ALTER TABLE pratos
ADD CONSTRAINT fk_prato_culinaria
FOREIGN KEY (id_tipo_culinaria) REFERENCES tipos_culinaria(id_tipo_culinaria)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* PRATO INGREDIENTES */
ALTER TABLE prato_ingredientes
ADD CONSTRAINT fk_prato_ingrediente_prato
FOREIGN KEY (id_prato) REFERENCES pratos(id_prato)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE prato_ingredientes
ADD CONSTRAINT fk_prato_ingrediente_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* FORNECEDOR PRODUTO */
ALTER TABLE fornecedor_produto
ADD CONSTRAINT fk_fornecedor_produto_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE fornecedor_produto
ADD CONSTRAINT fk_fornecedor_produto_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE CASCADE;

/* FORNECEDOR CATEGORIA */
ALTER TABLE fornecedor_categoria
ADD CONSTRAINT fk_fornecedor_categoria_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE fornecedor_categoria
ADD CONSTRAINT fk_fornecedor_categoria_categoria
FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
ON UPDATE CASCADE ON DELETE CASCADE;

/* LISTAS DE COMPRAS */
ALTER TABLE listas_compras
ADD CONSTRAINT fk_lista_usuario
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE CASCADE ON DELETE RESTRICT;

/* LISTA DE COMPRAS ITENS */
ALTER TABLE lista_compras_itens
ADD CONSTRAINT fk_lista_item_lista
FOREIGN KEY (id_lista_compras) REFERENCES listas_compras(id_lista_compras)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE lista_compras_itens
ADD CONSTRAINT fk_lista_item_produto
FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE lista_compras_itens
ADD CONSTRAINT fk_lista_item_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE SET NULL;

/* HISTÓRICO DE SUGESTÕES */
ALTER TABLE historico_sugestoes
ADD CONSTRAINT fk_hist_usuario
FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE historico_sugestoes
ADD CONSTRAINT fk_hist_prato
FOREIGN KEY (id_prato) REFERENCES pratos(id_prato)
ON UPDATE CASCADE ON DELETE CASCADE;

/* HISTÓRICO DE ENVIOS */
ALTER TABLE historico_envios
ADD CONSTRAINT fk_envio_lista
FOREIGN KEY (id_lista_compras) REFERENCES listas_compras(id_lista_compras)
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE historico_envios
ADD CONSTRAINT fk_envio_fornecedor
FOREIGN KEY (id_fornecedor) REFERENCES fornecedores(id_fornecedor)
ON UPDATE CASCADE ON DELETE CASCADE;





