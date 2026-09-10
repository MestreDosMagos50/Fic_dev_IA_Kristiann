-- 4.4.5 Exercício Prático

-- 1. Adicione mais documentos
-- Inserindo mais 3 documentos na tabela documentos com embeddings (animais e veículos)
INSERT INTO documentos (conteudo, embedding) VALUES
('O pássaro construiu um ninho.', '[0.3, 0.1, 0.5]'),
('O avião cruzou o céu.', '[0.9, 0.7, 0.4]'),
('O cavalo galopou pelo campo.', '[0.2, 0.3, 0.2]');

-- 2. Experimente com Produto Escalar: Operador: <#>
-- Consulta para encontrar os 2 documentos com o maior produto escalar em relação ao vetor [0.5, 0.5, 0.5]
-- Nota: no pgvector, <#> retorna o produto escalar negativo, então ordena-se de forma crescente ASC
SELECT conteudo, embedding, embedding <#> '[0.5, 0.5, 0.5]' AS produto_escalar
FROM documentos
ORDER BY produto_escalar ASC
LIMIT 2;

-- 3. Crie um índice
-- Criar um índice IVFFlat na coluna embedding usando a distância euclidiana:
CREATE INDEX ON documentos USING ivfflat (embedding vector_l2_ops) WITH (lists = 2);
-- Nota: lists deve ser ajustado com base no número de linhas (2 é suficiente para este exemplo)

-- Executar novamente a consulta de distância euclidiana para verificar o resultado
SELECT conteudo, embedding, embedding <-> '[0.15, 0.15, 0.35]' AS distancia
FROM documentos
ORDER BY distancia ASC
LIMIT 2;
