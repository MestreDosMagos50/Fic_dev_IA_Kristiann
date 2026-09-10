-- Encontra a Secretaria responsável comparando o vetor do texto do cidadão com os serviços
-- Nota: Aqui usamos uma variável %s no lugar do vetor na string, que seria substituída pelo Python. 
-- Para teste direto no banco, usaríamos um vetor fixo, como '[0.1, -0.2, 0.3]'.
SELECT 
 s.id, s.secretaria, s.servico, s.prazo_dias,
 s.embedding <=> '[0.1, -0.2, 0.3]' AS distancia -- Substituir pelo vetor real do relato
FROM servicos_master s
ORDER BY distancia ASC
LIMIT 1;
