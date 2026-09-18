-- =============================================================================
-- FIC Engenharia de Dados | Aula 03 (Módulo 2): Apache Hop & Orquestração
-- Padrão ELT: Transformação Executada Diretamente no Banco de Destino (PostgreSQL)
-- Arquivo: sql/02_elt_silver_produtos.sql (Baseado na Seção 7 da Apostila)
-- =============================================================================

-- Os 3 sinais do ELT puro:
-- 1. O SQL roda no destino (nada passa por engine externa de processamento);
-- 2. O WHERE recorta apenas a fatia demandada pelo negócio (o resto permanece intacto em staging);
-- 3. A transformação é reexecutável e idempotente via ON CONFLICT.

INSERT INTO silver.produtos (codigo, nome, categoria, preco, data_cadastro)
SELECT
    TRIM(codigo),
    INITCAP(TRIM(nome)),
    LOWER(TRIM(categoria)),
    REPLACE(REPLACE(REPLACE(preco, 'R$', ''), '.', ''), ',', '.')::NUMERIC(12,2),
    TO_DATE(data_cadastro, 'DD/MM/YYYY')
FROM staging.produtos
WHERE LOWER(TRIM(categoria)) IN ('eletronicos', 'livros', 'casa')
  AND preco ~ '^[R\$\s]*[0-9]+(\.[0-9]{3})*(,[0-9]{2})?$'
  AND data_cadastro ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
ON CONFLICT (codigo) DO UPDATE
SET nome = EXCLUDED.nome,
    preco = EXCLUDED.preco,
    processado_em = CURRENT_TIMESTAMP;
