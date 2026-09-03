-- 1. Conecte-se ao seu banco de dados PostgreSQL
-- psql -U seu_usuario -d meu_banco_de_dados

-- 2. Crie uma tabela com uma coluna JSONB
CREATE TABLE clientes (
 id SERIAL PRIMARY KEY,
 nome VARCHAR(100) NOT NULL,
 email VARCHAR(100) UNIQUE,
 detalhes JSONB
);

-- 3. Insira dados com JSONB
INSERT INTO clientes (nome, email, detalhes) VALUES
(
 'Ana Silva', 'ana.silva@example.com',
 '{"idade": 30, "interesses": ["leitura", "viagens"], "preferencias": {"newsletter": true, "idioma": "pt-BR"}}'
),
(
 'Bruno Costa', 'bruno.costa@example.com',
 '{"idade": 25, "interesses": ["esportes", "tecnologia"], "preferencias": {"newsletter": false}}'
);

-- 4. Consulte dados JSONB
-- Selecionar o nome e a idade dos clientes:
SELECT nome, detalhes->>'idade' AS idade FROM clientes;

-- Selecionar clientes que têm 'leitura' como interesse:
SELECT nome, detalhes FROM clientes WHERE detalhes->'interesses' ? 'leitura';

-- Selecionar clientes que desejam receber newsletter:
SELECT nome, detalhes FROM clientes WHERE detalhes->'preferencias'->>'newsletter' = 'true';
