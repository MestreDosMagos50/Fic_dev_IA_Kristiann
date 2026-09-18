-- init_db.sql — Inicialização e Estrutura do Banco PostgreSQL
-- Módulo 2 / Aula 01 — FIC Engenharia de Dados

-- 1. Criação do Schema silver
CREATE SCHEMA IF NOT EXISTS silver;

-- 2. Tabela silver.produtos (Válidos e Modelados)
CREATE TABLE IF NOT EXISTS silver.produtos (
    codigo TEXT PRIMARY KEY,
    nome TEXT,
    categoria TEXT,
    preco NUMERIC(12,2),
    data_cadastro DATE
);

-- 3. Tabela silver.rejeitados (Quarentena com Diagnóstico de Inconsistência)
CREATE TABLE IF NOT EXISTS silver.rejeitados (
    codigo TEXT,
    nome TEXT,
    preco NUMERIC(12,2),
    categoria TEXT,
    data_cadastro DATE,
    motivo_erro TEXT,
    pipeline_origem TEXT
);

-- 4. Consultas Úteis para Auditoria e Conferência
-- Contagem geral:
-- SELECT 'produtos' AS tabela, COUNT(*) AS total FROM silver.produtos
-- UNION ALL
-- SELECT 'rejeitados' AS tabela, COUNT(*) AS total FROM silver.rejeitados;

-- Distribuição dos motivos de rejeição na quarentena:
-- SELECT motivo_erro, COUNT(*) AS quantidade
-- FROM silver.rejeitados
-- GROUP BY motivo_erro
-- ORDER BY quantidade DESC;
