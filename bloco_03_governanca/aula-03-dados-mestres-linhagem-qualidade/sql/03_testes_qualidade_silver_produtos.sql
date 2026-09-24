-- =============================================================================
-- FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
-- Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
-- Arquivo: sql/03_testes_qualidade_silver_produtos.sql
-- Objetivo: Passo 4 do Mini-Lab — Quatro Testes de Qualidade em silver.produtos
--           com Simulação de Falha Proposital (Preço Negativo) e Restauração
-- =============================================================================

-- =============================================================================
-- PARTE 1: EXECUÇÃO DOS 4 TESTES NO ESTADO NORMAL (VERDE / APROVADO)
-- =============================================================================

-- Teste 1 (Unicidade): codigo deve ser único (0 duplicatas)
SELECT 
    'Teste 1 - Unicidade de Codigo' as nome_teste,
    COUNT(*) - COUNT(DISTINCT codigo) as falhas,
    CASE WHEN COUNT(*) - COUNT(DISTINCT codigo) = 0 THEN 'PASSED (VERDE)' ELSE 'FAILED (VERMELHO)' END as status
FROM silver.produtos;

-- Teste 2 (Completude / Não-nulidade): categoria não pode ser nula ou vazia
SELECT 
    'Teste 2 - Nao-nulidade de Categoria' as nome_teste,
    COUNT(*) FILTER (WHERE categoria IS NULL OR TRIM(categoria) = '') as falhas,
    CASE WHEN COUNT(*) FILTER (WHERE categoria IS NULL OR TRIM(categoria) = '') = 0 THEN 'PASSED (VERDE)' ELSE 'FAILED (VERMELHO)' END as status
FROM silver.produtos;

-- Teste 3 (Validade): faixa de preco deve ser estritamente positiva (preco > 0)
SELECT 
    'Teste 3 - Faixa Valida de Preco (preco > 0)' as nome_teste,
    COUNT(*) FILTER (WHERE preco <= 0) as falhas,
    CASE WHEN COUNT(*) FILTER (WHERE preco <= 0) = 0 THEN 'PASSED (VERDE)' ELSE 'FAILED (VERMELHO)' END as status
FROM silver.produtos;

-- Teste 4 (Consistência / Volume): contagem de linhas entre 1 e 10.000
SELECT 
    'Teste 4 - Contagem de Linhas (1 a 10.000)' as nome_teste,
    COUNT(*) as valor_atual,
    CASE WHEN COUNT(*) BETWEEN 1 AND 10000 THEN 'PASSED (VERDE)' ELSE 'FAILED (VERMELHO)' END as status
FROM silver.produtos;


-- =============================================================================
-- PARTE 2: SIMULAÇÃO DE FALHA PROPOSITAL (INSERÇÃO DE PREÇO NEGATIVO)
-- =============================================================================

-- Inserindo produto com anomalia de qualidade (preço negativo)
INSERT INTO silver.produtos (codigo, nome, preco, categoria, data_cadastro)
VALUES ('PROD-FALHA-TESTE', 'Cadeira Gamer Anômala com Preço Inválido', -199.90, 'Móveis', CURRENT_DATE)
ON CONFLICT (codigo) DO UPDATE SET preco = -199.90;

-- Reexecutando o Teste 3 para comprovar status FAILED (VERMELHO)
SELECT 
    'Teste 3 - Faixa Valida de Preco (preco > 0)' as nome_teste,
    COUNT(*) FILTER (WHERE preco <= 0) as falhas,
    STRING_AGG(codigo || ' (' || preco || ')', ', ') as registros_infracao,
    CASE WHEN COUNT(*) FILTER (WHERE preco <= 0) = 0 THEN 'PASSED (VERDE)' ELSE 'FAILED (VERMELHO)' END as status
FROM silver.produtos;


-- =============================================================================
-- PARTE 3: REMOÇÃO DO REGISTRO E RESTAURAÇÃO DO STATUS APROVADO (VERDE)
-- =============================================================================

DELETE FROM silver.produtos WHERE codigo = 'PROD-FALHA-TESTE';

-- Verificação final de reabilitação
SELECT 
    'Teste 3 - Faixa Valida de Preco (Apos Limpeza)' as nome_teste,
    COUNT(*) FILTER (WHERE preco <= 0) as falhas,
    CASE WHEN COUNT(*) FILTER (WHERE preco <= 0) = 0 THEN 'PASSED (VERDE)' ELSE 'FAILED (VERMELHO)' END as status
FROM silver.produtos;
