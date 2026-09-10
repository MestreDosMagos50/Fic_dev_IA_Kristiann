-- Tabela para produtos com embedding vetorial
CREATE TABLE IF NOT EXISTS produtos_master (
 id SERIAL PRIMARY KEY,
 nome VARCHAR(255) NOT NULL,
 descricao TEXT,
 categoria VARCHAR(100),
 embedding vector(3) -- Usaremos 3 dimensões para simplificar
);

-- Tabela para avaliações brutas (JSONB)
CREATE TABLE IF NOT EXISTS avaliacoes_raw (
 id SERIAL PRIMARY KEY,
 dados JSONB
);

-- Tabela para avaliações processadas
CREATE TABLE IF NOT EXISTS avaliacoes_processadas (
 id SERIAL PRIMARY KEY,
 produto_id INT REFERENCES produtos_master(id),
 cliente_id VARCHAR(50),
 avaliacao INT,
 comentario TEXT,
 sentimento VARCHAR(20) -- Ex: 'positivo', 'negativo', 'neutro'
);
