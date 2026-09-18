-- ============================================================================
-- sql/05_prepara_fontes_concorrentes.sql
-- FIC Engenharia de Dados | Aula 03 (Módulo 2): Orquestração & Reconciliação
-- DDL para as fontes concorrentes de temperatura (INMET Terrestre vs CPTEC Satélite)
-- ============================================================================

-- Staging Fonte 3A: INMET Terrestre
CREATE TABLE IF NOT EXISTS staging.inmet_temperatura (
    cod_mun_6 TEXT,
    municipio TEXT,
    temperatura_c TEXT,
    umidade_relativa TEXT,
    status_sensor TEXT,
    data_leitura TEXT
);

-- Staging Fonte 3B: CPTEC Satélite
CREATE TABLE IF NOT EXISTS staging.cptec_temperatura (
    cod_mun_6 TEXT,
    municipio TEXT,
    temperatura_satelite_c TEXT,
    umidade_satelite TEXT,
    indice_cobertura TEXT,
    data_leitura TEXT
);

-- Silver: Tabela Reconciliada (Golden Record Climático com Rastreabilidade de Origem)
CREATE TABLE IF NOT EXISTS silver.clima_reconciliado (
    cod_mun_6 VARCHAR(6) PRIMARY KEY,
    municipio VARCHAR(100),
    temp_inmet_original NUMERIC(5,2),
    temp_cptec_original NUMERIC(5,2),
    temperatura_eleita NUMERIC(5,2) NOT NULL,
    fonte_eleita VARCHAR(30) NOT NULL,
    status_arbitragem VARCHAR(200) NOT NULL,
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
