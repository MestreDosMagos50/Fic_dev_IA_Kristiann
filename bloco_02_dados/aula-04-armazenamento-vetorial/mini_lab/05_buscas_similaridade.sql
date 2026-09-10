-- 4.4.4 Realizando Buscas de Similaridade

-- 1. Busca por Distância Euclidiana (L2 distance): Operador: <->
-- Vamos buscar os documentos mais próximos do vetor [0.15, 0.15, 0.35]:
SELECT conteudo, embedding, embedding <-> '[0.15, 0.15, 0.35]' AS distancia
FROM documentos
ORDER BY distancia ASC
LIMIT 2;

-- O resultado deve mostrar os documentos sobre o gato e o cachorro, 
-- pois seus vetores são mais próximos do vetor de consulta.

-- 2. Busca por Distância Cosseno: Operador: <=>
-- Vamos buscar os documentos mais próximos do vetor [0.8, 0.8, 0.15]:
SELECT conteudo, embedding, embedding <=> '[0.8, 0.8, 0.15]' AS distancia_cosseno
FROM documentos
ORDER BY distancia_cosseno ASC
LIMIT 2;

-- O resultado deve mostrar os documentos sobre o carro e a bicicleta.
