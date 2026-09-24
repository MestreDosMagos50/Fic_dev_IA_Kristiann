-- =============================================================================
-- FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
-- Aula 01: Conceitos de Documentação, Metadados e Governança de Dados
-- Arquivo: sql/00_prepara_banco_ecommerce.sql
-- Objetivo: Estruturar os schemas (staging, silver, gold) e tabelas do e-commerce
-- Banco: meu_banco_de_dados
-- =============================================================================

-- 1. Criação dos Schemas da Arquitetura Medalhão
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- -----------------------------------------------------------------------------
-- 2. CAMADA STAGING (Bronze / Ingestão Bruta)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS staging.produtos (
    codigo TEXT,
    nome TEXT,
    preco TEXT,
    categoria TEXT,
    data_cadastro TEXT
);

CREATE TABLE IF NOT EXISTS staging.vendas (
    id_venda TEXT,
    codigo_produto TEXT,
    quantidade TEXT,
    valor_unitario TEXT,
    valor_total TEXT,
    data_venda TEXT,
    cliente_id TEXT
);

CREATE TABLE IF NOT EXISTS staging.clientes (
    cliente_id TEXT,
    nome TEXT,
    email TEXT,
    cidade TEXT,
    uf TEXT,
    segmento TEXT
);

-- -----------------------------------------------------------------------------
-- 3. CAMADA SILVER (Limpa, Padronizada, Tipada e Deduplicada)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS silver.produtos (
    codigo VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    preco NUMERIC(12,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    data_cadastro DATE NOT NULL,
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.vendas (
    id_venda VARCHAR(50) PRIMARY KEY,
    codigo_produto VARCHAR(50) NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario NUMERIC(12,2) NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL,
    data_venda DATE NOT NULL,
    cliente_id VARCHAR(50) NOT NULL,
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.clientes (
    cliente_id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    segmento VARCHAR(50) NOT NULL,
    processado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.rejeitados (
    id SERIAL PRIMARY KEY,
    pipeline_origem VARCHAR(100) NOT NULL,
    motivo_erro VARCHAR(255) NOT NULL,
    registro_bruto TEXT,
    data_rejeicao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 4. CAMADA GOLD (Modelagem Dimensional Star Schema para BI e Analytics)
-- -----------------------------------------------------------------------------

-- Dimensão Cliente (SCD Tipo 1 / Cadastro Corporativo Enriquecido)
CREATE TABLE IF NOT EXISTS gold.dim_cliente (
    sk_cliente SERIAL PRIMARY KEY,
    cliente_id VARCHAR(50) UNIQUE NOT NULL,
    nome_cliente VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    uf VARCHAR(2) NOT NULL,
    regiao VARCHAR(50) NOT NULL,
    segmento VARCHAR(50) NOT NULL,
    status_cliente VARCHAR(20) DEFAULT 'Ativo',
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimensão Produto (Catálogo Padronizado de Mercadorias)
CREATE TABLE IF NOT EXISTS gold.dim_produto (
    sk_produto SERIAL PRIMARY KEY,
    codigo_produto VARCHAR(50) UNIQUE NOT NULL,
    nome_produto VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    subcategoria VARCHAR(100),
    preco_tabela NUMERIC(12,2) NOT NULL,
    faixa_preco VARCHAR(50) NOT NULL,
    status_ativo BOOLEAN DEFAULT TRUE,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela Fato Vendas (Tier 1 — Crítico de Negócio / Decisão Executiva)
CREATE TABLE IF NOT EXISTS gold.fato_vendas (
    sk_venda BIGSERIAL PRIMARY KEY,
    id_venda VARCHAR(50) NOT NULL,
    sk_cliente INTEGER NOT NULL REFERENCES gold.dim_cliente(sk_cliente),
    sk_produto INTEGER NOT NULL REFERENCES gold.dim_produto(sk_produto),
    data_venda DATE NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario NUMERIC(12,2) NOT NULL,
    desconto NUMERIC(12,2) DEFAULT 0.00,
    valor_bruto NUMERIC(12,2) NOT NULL,
    valor_liquido NUMERIC(12,2) NOT NULL,
    custo_produto NUMERIC(12,2) NOT NULL,
    impostos NUMERIC(12,2) NOT NULL,
    margem_lucro NUMERIC(12,2) NOT NULL,
    canal_venda VARCHAR(50) NOT NULL,
    status_pedido VARCHAR(50) NOT NULL,
    carregado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 5. CARGA DE DADOS DE EXEMPLO (SEED REALISTA)
-- -----------------------------------------------------------------------------

-- Staging
TRUNCATE TABLE staging.produtos, staging.vendas, staging.clientes RESTART IDENTITY;
INSERT INTO staging.produtos (codigo, nome, preco, categoria, data_cadastro) VALUES
('PROD-001', 'Notebook Gamer Legion 5', '5499.90', 'Informatica', '2026-01-15'),
('PROD-002', 'Monitor UltraWide 29 IPS', '1249.00', 'Informatica', '2026-01-16'),
('PROD-003', 'Teclado Mecanico RGB Pro', '349.50', 'Perifericos', '2026-02-01'),
('PROD-004', 'Cadeira Ergonomica Mesh', '899.99', 'Moveis', '2026-02-10'),
('PROD-005', 'Mouse Sem Fio Ergonomico', '189.90', 'Perifericos', '2026-02-15');

INSERT INTO staging.clientes (cliente_id, nome, email, cidade, uf, segmento) VALUES
('CLI-101', 'Ana Paula Souza', 'ana.souza@email.com', 'Sao Paulo', 'SP', 'B2C'),
('CLI-102', 'Bruno Rocha Lima', 'bruno.lima@techcorp.com.br', 'Campinas', 'SP', 'B2B'),
('CLI-103', 'Carla Mendes Alencar', 'carla.mendes@email.com', 'Belo Horizonte', 'MG', 'B2C'),
('CLI-104', 'Diego Fernandes Pinto', 'diego.fernandes@invest.com.br', 'Curitiba', 'PR', 'VIP'),
('CLI-105', 'Eliana Vasconcelos', 'eliana.v@email.com', 'Recife', 'PE', 'B2C');

INSERT INTO staging.vendas (id_venda, codigo_produto, quantidade, valor_unitario, valor_total, data_venda, cliente_id) VALUES
('VND-2026-001', 'PROD-001', '1', '5499.90', '5499.90', '2026-08-01', 'CLI-101'),
('VND-2026-002', 'PROD-002', '2', '1249.00', '2498.00', '2026-08-02', 'CLI-102'),
('VND-2026-003', 'PROD-003', '3', '349.50', '1048.50', '2026-08-03', 'CLI-103'),
('VND-2026-004', 'PROD-004', '1', '899.99', '899.99', '2026-08-04', 'CLI-104'),
('VND-2026-005', 'PROD-005', '2', '189.90', '379.80', '2026-08-05', 'CLI-105');

-- Silver
TRUNCATE TABLE silver.produtos, silver.vendas, silver.clientes, silver.rejeitados RESTART IDENTITY CASCADE;

INSERT INTO silver.produtos (codigo, nome, preco, categoria, data_cadastro) VALUES
('PROD-001', 'Notebook Gamer Legion 5', 5499.90, 'Informática', '2026-01-15'),
('PROD-002', 'Monitor UltraWide 29 IPS', 1249.00, 'Informática', '2026-01-16'),
('PROD-003', 'Teclado Mecânico RGB Pro', 349.50, 'Periféricos', '2026-02-01'),
('PROD-004', 'Cadeira Ergonômica Mesh', 899.99, 'Móveis', '2026-02-10'),
('PROD-005', 'Mouse Sem Fio Ergonômico', 189.90, 'Periféricos', '2026-02-15')
ON CONFLICT (codigo) DO UPDATE SET preco = EXCLUDED.preco;

INSERT INTO silver.clientes (cliente_id, nome, email, cidade, uf, segmento) VALUES
('CLI-101', 'Ana Paula Souza', 'ana.souza@email.com', 'São Paulo', 'SP', 'B2C'),
('CLI-102', 'Bruno Rocha Lima', 'bruno.lima@techcorp.com.br', 'Campinas', 'SP', 'B2B'),
('CLI-103', 'Carla Mendes Alencar', 'carla.mendes@email.com', 'Belo Horizonte', 'MG', 'B2C'),
('CLI-104', 'Diego Fernandes Pinto', 'diego.fernandes@invest.com.br', 'Curitiba', 'PR', 'VIP'),
('CLI-105', 'Eliana Vasconcelos', 'eliana.v@email.com', 'Recife', 'PE', 'B2C')
ON CONFLICT (cliente_id) DO UPDATE SET nome = EXCLUDED.nome;

INSERT INTO silver.vendas (id_venda, codigo_produto, quantidade, valor_unitario, valor_total, data_venda, cliente_id) VALUES
('VND-2026-001', 'PROD-001', 1, 5499.90, 5499.90, '2026-08-01', 'CLI-101'),
('VND-2026-002', 'PROD-002', 2, 1249.00, 2498.00, '2026-08-02', 'CLI-102'),
('VND-2026-003', 'PROD-003', 3, 349.50, 1048.50, '2026-08-03', 'CLI-103'),
('VND-2026-004', 'PROD-004', 1, 899.99, 899.99, '2026-08-04', 'CLI-104'),
('VND-2026-005', 'PROD-005', 2, 189.90, 379.80, '2026-08-05', 'CLI-105')
ON CONFLICT (id_venda) DO UPDATE SET valor_total = EXCLUDED.valor_total;

-- Gold
TRUNCATE TABLE gold.fato_vendas, gold.dim_produto, gold.dim_cliente RESTART IDENTITY CASCADE;

INSERT INTO gold.dim_cliente (cliente_id, nome_cliente, email, cidade, uf, regiao, segmento, status_cliente) VALUES
('CLI-101', 'Ana Paula Souza', 'ana.souza@email.com', 'São Paulo', 'SP', 'Sudeste', 'B2C', 'Ativo'),
('CLI-102', 'Bruno Rocha Lima', 'bruno.lima@techcorp.com.br', 'Campinas', 'SP', 'Sudeste', 'B2B', 'Ativo'),
('CLI-103', 'Carla Mendes Alencar', 'carla.mendes@email.com', 'Belo Horizonte', 'MG', 'Sudeste', 'B2C', 'Ativo'),
('CLI-104', 'Diego Fernandes Pinto', 'diego.fernandes@invest.com.br', 'Curitiba', 'PR', 'Sul', 'VIP', 'Ativo'),
('CLI-105', 'Eliana Vasconcelos', 'eliana.v@email.com', 'Recife', 'PE', 'Nordeste', 'B2C', 'Ativo');

INSERT INTO gold.dim_produto (codigo_produto, nome_produto, categoria, subcategoria, preco_tabela, faixa_preco, status_ativo) VALUES
('PROD-001', 'Notebook Gamer Legion 5', 'Informática', 'Laptops', 5499.90, 'Premium', TRUE),
('PROD-002', 'Monitor UltraWide 29 IPS', 'Informática', 'Monitores', 1249.00, 'Médio', TRUE),
('PROD-003', 'Teclado Mecânico RGB Pro', 'Periféricos', 'Teclados', 349.50, 'Acessível', TRUE),
('PROD-004', 'Cadeira Ergonômica Mesh', 'Móveis', 'Cadeiras', 899.99, 'Médio', TRUE),
('PROD-005', 'Mouse Sem Fio Ergonômico', 'Periféricos', 'Mouses', 189.90, 'Acessível', TRUE);

-- Fato Vendas: Regra de Negócio Formal
-- valor_bruto = quantidade * preco_unitario
-- valor_liquido = valor_bruto - desconto
-- custo_produto = valor_bruto * 0.55 (ex: 55% de CMV)
-- impostos = valor_liquido * 0.18 (ICMS + PIS/COFINS = 18%)
-- margem_lucro = valor_liquido - custo_produto - impostos
INSERT INTO gold.fato_vendas (
    id_venda, sk_cliente, sk_produto, data_venda, quantidade, preco_unitario, desconto,
    valor_bruto, valor_liquido, custo_produto, impostos, margem_lucro, canal_venda, status_pedido
) VALUES
('VND-2026-001', 1, 1, '2026-08-01', 1, 5499.90, 200.00, 5499.90, 5299.90, 3024.95, 953.98, 1320.97, 'E-commerce Web', 'Entregue'),
('VND-2026-002', 2, 2, '2026-08-02', 2, 1249.00, 100.00, 2498.00, 2398.00, 1373.90, 431.64, 592.46, 'B2B Portal', 'Entregue'),
('VND-2026-003', 3, 3, '2026-08-03', 3, 349.50, 0.00, 1048.50, 1048.50, 576.68, 188.73, 283.09, 'App Mobile', 'Entregue'),
('VND-2026-004', 4, 4, '2026-08-04', 1, 899.99, 50.00, 899.99, 849.99, 494.99, 153.00, 202.00, 'E-commerce Web', 'Entregue'),
('VND-2026-005', 5, 5, '2026-08-05', 2, 189.90, 10.00, 379.80, 369.80, 208.89, 66.56, 94.35, 'Marketplace', 'Entregue');
