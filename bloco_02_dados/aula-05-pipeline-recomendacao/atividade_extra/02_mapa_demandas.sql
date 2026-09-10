-- Mapa de Demandas Críticas por Bairro e Secretaria:
SELECT 
 op.bairro,
 sm.secretaria,
 COUNT(*) AS total_demandas_criticas
FROM ouvidoria_processada op
JOIN servicos_master sm ON op.servico_sugerido_id = sm.id
WHERE op.nivel_prioridade = 'CRÍTICA'
GROUP BY op.bairro, sm.secretaria
ORDER BY total_demandas_criticas DESC;
