-- =============================================================================
-- FIC Engenharia de Dados | Aula 03 (Módulo 2): Apache Hop & Orquestração
-- Script DDL Idempotente: 5 Fontes Brasileiras (IBGE, DataSUS, INMET, CNES, Alertas)
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- -----------------------------------------------------------------------------
-- 1. CAMADA BRONZE / STAGING (5 Fontes de Cidades, População e Saúde)
-- -----------------------------------------------------------------------------
-- Fonte 1: IBGE População & Censo
CREATE TABLE IF NOT EXISTS staging.ibge_municipios (
    cod_mun TEXT,
    cod_mun_6 TEXT,
    nome_municipio TEXT,
    uf TEXT,
    regiao TEXT,
    populacao TEXT,
    area_km2 TEXT
);

-- Fonte 2: DataSUS Notificações Epidemiológicas (Dengue)
CREATE TABLE IF NOT EXISTS staging.datasus_dengue (
    id_notificacao TEXT,
    cod_mun_6 TEXT,
    data_notificacao TEXT,
    casos_notificados TEXT,
    casos_confirmados TEXT,
    classificacao TEXT
);

-- Fonte 3: INMET Clima e Chuva
CREATE TABLE IF NOT EXISTS staging.inmet_chuva (
    cod_mun_6 TEXT,
    chuva_acumulada_mm TEXT,
    dias_com_chuva TEXT,
    estacao_monitorada TEXT
);

-- Fonte 4: CNES Capacidade Hospitalar e Leitos SUS (Relacional)
CREATE TABLE IF NOT EXISTS staging.cnes_leitos (
    cod_mun_6 TEXT,
    municipio TEXT,
    leitos_clinicos TEXT,
    leitos_uti TEXT,
    postos_saude TEXT
);

-- Fonte 5: Vigilância Sanitária & Alertas Epidemiológicos (MongoDB NoSQL)
CREATE TABLE IF NOT EXISTS staging.alertas_vigilancia (
    id_alerta TEXT,
    cod_mun_6 TEXT,
    cidade TEXT,
    nivel_risco TEXT,
    acao TEXT,
    data TEXT
);

-- Tabelas legadas mantidas para compatibilidade com os exercícios da apostila
CREATE TABLE IF NOT EXISTS staging.produtos (codigo TEXT, nome TEXT, preco TEXT, categoria TEXT, data_cadastro TEXT);
CREATE TABLE IF NOT EXISTS staging.vendas (id_venda TEXT, codigo_produto TEXT, quantidade TEXT, valor_unitario TEXT, valor_total TEXT, data_venda TEXT, cliente_id TEXT);
CREATE TABLE IF NOT EXISTS staging.avaliacoes (id_avaliacao TEXT, codigo_produto TEXT, nota TEXT, comentario TEXT, data_avaliacao TEXT);
CREATE TABLE IF NOT EXISTS staging.clientes (cliente_id TEXT, nome TEXT, cidade TEXT, uf TEXT, segmento TEXT);

-- -----------------------------------------------------------------------------
-- 2. CAMADA SILVER (Higienizada, deduplicada e tipada)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS silver.municipios (
    cod_mun_6 VARCHAR(10) PRIMARY KEY,
    cod_mun VARCHAR(10),
    nome_municipio VARCHAR(255) NOT NULL,
    uf VARCHAR(5) NOT NULL,
    regiao VARCHAR(50) NOT NULL,
    populacao INTEGER NOT NULL,
    area_km2 NUMERIC(10,2),
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.notificacoes_dengue (
    id_notificacao VARCHAR(50) PRIMARY KEY,
    cod_mun_6 VARCHAR(10) NOT NULL,
    data_notificacao DATE NOT NULL,
    casos_notificados INTEGER NOT NULL,
    casos_confirmados INTEGER NOT NULL,
    classificacao VARCHAR(100),
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.inmet_chuva (
    cod_mun_6 VARCHAR(10) PRIMARY KEY,
    chuva_acumulada_mm NUMERIC(10,2) NOT NULL,
    dias_com_chuva INTEGER NOT NULL,
    estacao_monitorada VARCHAR(255),
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.cnes_leitos (
    cod_mun_6 VARCHAR(10) PRIMARY KEY,
    municipio VARCHAR(255) NOT NULL,
    leitos_clinicos INTEGER NOT NULL,
    leitos_uti INTEGER NOT NULL,
    postos_saude INTEGER NOT NULL,
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.alertas_vigilancia (
    id_alerta VARCHAR(50) PRIMARY KEY,
    cod_mun_6 VARCHAR(10) NOT NULL,
    cidade VARCHAR(255),
    nivel_risco VARCHAR(50) NOT NULL,
    acao TEXT,
    data DATE,
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Silver consolidada via ELT no PostgreSQL (Passo 5 - Desafio ELT)
CREATE TABLE IF NOT EXISTS silver.indicadores_municipais_elt (
    cod_mun_6 VARCHAR(10) PRIMARY KEY,
    nome_municipio VARCHAR(255),
    uf VARCHAR(5),
    regiao VARCHAR(50),
    populacao INTEGER,
    total_casos INTEGER,
    taxa_incidencia_100k NUMERIC(10,2),
    chuva_mm NUMERIC(10,2),
    leitos_uti INTEGER,
    classificacao_risco VARCHAR(50),
    calculado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quarentena de Rejeitados
CREATE TABLE IF NOT EXISTS silver.rejeitados (
    id SERIAL PRIMARY KEY,
    pipeline_origem VARCHAR(50) NOT NULL,
    motivo_erro VARCHAR(255) NOT NULL,
    registro_bruto TEXT,
    data_rejeicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabelas legadas silver
CREATE TABLE IF NOT EXISTS silver.produtos (codigo VARCHAR(50) PRIMARY KEY, nome VARCHAR(255), preco NUMERIC(12,2), categoria VARCHAR(100), data_cadastro DATE, processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS silver.vendas (id_venda VARCHAR(50) PRIMARY KEY, codigo_produto VARCHAR(50), quantidade INTEGER, valor_unitario NUMERIC(12,2), valor_total NUMERIC(12,2), data_venda DATE, cliente_id VARCHAR(50), processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS silver.avaliacoes (id_avaliacao VARCHAR(50) PRIMARY KEY, codigo_produto VARCHAR(50), nota INTEGER, comentario TEXT, data_avaliacao DATE, processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS silver.avaliacoes_elt (id_avaliacao VARCHAR(50) PRIMARY KEY, codigo_produto VARCHAR(50), nota INTEGER, comentario TEXT, data_avaliacao DATE, carregado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
