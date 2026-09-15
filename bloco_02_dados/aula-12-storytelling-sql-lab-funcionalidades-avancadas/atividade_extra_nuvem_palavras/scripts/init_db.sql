-- ====================================================================
-- Atividade Extra: Nuvem de Palavras sobre Tecnologia no Apache Superset
-- Script DDL de Inicialização e Dados Iniciais
-- ====================================================================

-- 1. Criação da tabela de termos tecnológicos
CREATE TABLE IF NOT EXISTS nuvem_palavras_tech (
    id SERIAL PRIMARY KEY,
    palavra VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    frequencia INT NOT NULL DEFAULT 1,
    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índice para acelerar consultas periódicas do Superset
CREATE INDEX IF NOT EXISTS idx_nuvem_palavra_data ON nuvem_palavras_tech (data_atualizacao DESC);

-- 2. Carga inicial de palavras com pesos de frequência
INSERT INTO nuvem_palavras_tech (palavra, categoria, frequencia, data_atualizacao) VALUES
('Python', 'Linguagens', 95, CURRENT_TIMESTAMP),
('PostgreSQL', 'Bancos de Dados', 88, CURRENT_TIMESTAMP),
('Apache Superset', 'Engenharia de Dados', 92, CURRENT_TIMESTAMP),
('Docker', 'Cloud & DevOps', 85, CURRENT_TIMESTAMP),
('Kubernetes', 'Cloud & DevOps', 78, CURRENT_TIMESTAMP),
('Inteligência Artificial', 'IA & ML', 99, CURRENT_TIMESTAMP),
('Machine Learning', 'IA & ML', 90, CURRENT_TIMESTAMP),
('LLMs', 'IA & ML', 96, CURRENT_TIMESTAMP),
('FastAPI', 'Linguagens', 72, CURRENT_TIMESTAMP),
('SQL Lab', 'Engenharia de Dados', 84, CURRENT_TIMESTAMP),
('Data Warehouse', 'Engenharia de Dados', 76, CURRENT_TIMESTAMP),
('Apache Kafka', 'Engenharia de Dados', 80, CURRENT_TIMESTAMP),
('Pandas', 'IA & ML', 82, CURRENT_TIMESTAMP),
('PyTorch', 'IA & ML', 86, CURRENT_TIMESTAMP),
('Terraform', 'Cloud & DevOps', 68, CURRENT_TIMESTAMP),
('AWS', 'Cloud & DevOps', 89, CURRENT_TIMESTAMP),
('OpenAI', 'IA & ML', 94, CURRENT_TIMESTAMP),
('ETL Pipeline', 'Engenharia de Dados', 83, CURRENT_TIMESTAMP),
('Redis', 'Bancos de Dados', 65, CURRENT_TIMESTAMP),
('TypeScript', 'Linguagens', 74, CURRENT_TIMESTAMP),
('LangChain', 'IA & ML', 88, CURRENT_TIMESTAMP),
('Big Data', 'Engenharia de Dados', 77, CURRENT_TIMESTAMP),
('Git', 'Ferramentas', 70, CURRENT_TIMESTAMP),
('Linux', 'Sistemas', 81, CURRENT_TIMESTAMP);

-- 3. Consulta de Agregação usada no Superset para a Nuvem de Palavras
-- No Superset, o gráfico 'Word Cloud' seleciona:
-- Series / Dimension: palavra
-- Metric: SUM(frequencia)
SELECT
    palavra,
    categoria,
    SUM(frequencia) AS peso_frequencia,
    MAX(data_atualizacao) AS ultima_coleta
FROM nuvem_palavras_tech
WHERE data_atualizacao >= CURRENT_TIMESTAMP - INTERVAL '30 minutes'
GROUP BY palavra, categoria
ORDER BY peso_frequencia DESC;
