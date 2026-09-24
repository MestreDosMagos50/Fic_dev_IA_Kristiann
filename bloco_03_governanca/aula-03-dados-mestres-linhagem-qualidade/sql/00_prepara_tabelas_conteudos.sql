-- =============================================================================
-- FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
-- Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
-- Arquivo: sql/00_prepara_tabelas_conteudos.sql
-- Objetivo: DDL das camadas staging, silver e gold para o dataset de conteúdos
-- =============================================================================

-- 1. CAMADA STAGING (Ingestão Raw do CSV de Conteúdos)
CREATE TABLE IF NOT EXISTS staging.conteudos (
    conteudo_id INT,
    titulo TEXT,
    tipo TEXT,
    categoria TEXT,
    nivel TEXT,
    carga_horaria_min INT,
    data_publicacao DATE,
    descricao TEXT,
    autor TEXT,
    ingestado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CAMADA SILVER (Limpa, Validada, Tipada com Flags de Duplicata e Golden Record)
CREATE TABLE IF NOT EXISTS silver.conteudos (
    conteudo_id INT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    carga_horaria_min INT NOT NULL,
    data_publicacao DATE NOT NULL,
    descricao TEXT,
    autor VARCHAR(255) NOT NULL,
    is_duplicata BOOLEAN DEFAULT FALSE,
    golden_record_id INT,
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. CAMADA GOLD (Modelagem Dimensional e Master Data)

-- Dimensão Conteúdo (Master Data / Golden Record Consolidado)
CREATE TABLE IF NOT EXISTS gold.dim_conteudo (
    sk_conteudo SERIAL PRIMARY KEY,
    conteudo_id INT UNIQUE NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    carga_horaria_min INT NOT NULL,
    carga_horaria_horas NUMERIC(10,2) NOT NULL,
    autor VARCHAR(255) NOT NULL,
    data_primeira_publicacao DATE NOT NULL,
    versoes_identificadas INT DEFAULT 1,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensão Autor (Master Data / Cadastro Único de Especialistas)
CREATE TABLE IF NOT EXISTS gold.dim_autor (
    sk_autor SERIAL PRIMARY KEY,
    nome_autor VARCHAR(255) UNIQUE NOT NULL,
    titulacao VARCHAR(50),
    nome_limpo VARCHAR(255) NOT NULL,
    total_conteudos INT NOT NULL,
    total_horas NUMERIC(10,2) NOT NULL,
    categoria_principal VARCHAR(100) NOT NULL,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensão Categoria (Dado de Referência / Taxonomia Oficial)
CREATE TABLE IF NOT EXISTS gold.dim_categoria (
    sk_categoria SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(100) UNIQUE NOT NULL,
    macro_area VARCHAR(100) NOT NULL,
    total_titulos INT NOT NULL,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fato Publicações (Transacional / Eventos de Publicação e Métricas)
CREATE TABLE IF NOT EXISTS gold.fato_publicacoes (
    sk_publicacao SERIAL PRIMARY KEY,
    conteudo_id INT NOT NULL,
    sk_conteudo INT NOT NULL REFERENCES gold.dim_conteudo(sk_conteudo),
    sk_autor INT NOT NULL REFERENCES gold.dim_autor(sk_autor),
    sk_categoria INT NOT NULL REFERENCES gold.dim_categoria(sk_categoria),
    tipo VARCHAR(50) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    data_publicacao DATE NOT NULL,
    ano_publicacao INT NOT NULL,
    mes_publicacao INT NOT NULL,
    carga_horaria_min INT NOT NULL,
    carga_horaria_horas NUMERIC(10,2) NOT NULL,
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Concessão de Permissões ao Usuário OpenMetadata (Menor Privilégio)
GRANT USAGE ON SCHEMA staging, silver, gold TO openmetadata_user;
GRANT SELECT ON ALL TABLES IN SCHEMA staging, silver, gold TO openmetadata_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging, silver, gold GRANT SELECT ON TABLES TO openmetadata_user;
