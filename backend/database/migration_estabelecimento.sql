-- ==========================================================
-- Migração: vínculo Funcionário -> Estabelecimento do ADM
-- ==========================================================
-- Use este script se você já tem o banco `stockchef` criado e não quer
-- perder os dados (o `rodar_tudo_de_uma_vez.sql` dá DROP DATABASE).
--
-- Rode este arquivo uma única vez no seu MySQL, com o banco `stockchef`
-- selecionado. Se alguma coluna já existir, remova a linha correspondente
-- antes de rodar (o MySQL não tem "ADD COLUMN IF NOT EXISTS" em todas as
-- versões).

USE stockchef;

ALTER TABLE usuarios
    ADD COLUMN codigo_estabelecimento VARCHAR(10) UNIQUE AFTER ativo,
    ADD COLUMN id_estabelecimento INT AFTER codigo_estabelecimento,
    ADD COLUMN status ENUM('Pendente','Aprovado','Recusado') NOT NULL DEFAULT 'Aprovado' AFTER id_estabelecimento;

ALTER TABLE usuarios
    ADD CONSTRAINT fk_usuarios_estabelecimento
        FOREIGN KEY (id_estabelecimento) REFERENCES usuarios(id_usuario);

-- Gera um código de estabelecimento único para cada Administrador já
-- existente (necessário porque a coluna é UNIQUE e os ADMs antigos
-- ficariam todos com NULL, o que é permitido, mas fica sem uso).
-- Ajuste/rode manualmente um UPDATE por administrador se preferir
-- códigos mais amigáveis; este é só um gerador simples baseado no id:
UPDATE usuarios
SET codigo_estabelecimento = CONCAT('ADM', LPAD(id_usuario, 3, '0'))
WHERE tipo = 'Administrador' AND codigo_estabelecimento IS NULL;

-- Todo Funcionario cadastrado antes desta migração não tinha vínculo de
-- estabelecimento nem passava por aprovação. Ficam Pendentes por padrão
-- (ver ALTER acima) -- ajuste manualmente conforme a sua realidade, por
-- exemplo vinculando-os todos ao seu único Administrador existente:
--
-- UPDATE usuarios
-- SET id_estabelecimento = (SELECT id_usuario FROM (SELECT id_usuario FROM usuarios WHERE tipo = 'Administrador' LIMIT 1) AS t),
--     status = 'Aprovado'
-- WHERE tipo = 'Funcionario';
