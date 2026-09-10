SELECT id, nome, categoria, embedding FROM produtos_master;

SELECT * FROM avaliacoes_raw;

SELECT * FROM avaliacoes_processadas;

SELECT
 pm.id, pm.nome, pm.categoria,
 pm.embedding <=> (SELECT embedding FROM produtos_master WHERE id = 1) AS distancia_cosseno
FROM produtos_master pm
WHERE pm.id != 1
ORDER BY distancia_cosseno ASC
LIMIT 3;
