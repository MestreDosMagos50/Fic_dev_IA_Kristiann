-- ====================================================================
-- FIC DEV IA – Engenharia de Dados | Aula 12
-- Roteiro Prático 4.4.2: Usando o SQL Lab para Criar um Dataset
-- ====================================================================

-- Passo a passo no Apache Superset:
-- 1. Abra o Apache Superset (http://localhost:8088) e autentique-se.
-- 2. Navegue até o menu superior: SQL Lab -> SQL Editor.
-- 3. No painel à esquerda, selecione o Database: superset_data e schema: public.
-- 4. Cole e execute a consulta abaixo:

SELECT
    CAST(data_hora_venda AS DATE) AS data_venda,
    regiao_cliente AS regiao,
    SUM(quantidade * preco_unitario) AS faturamento_diario
FROM vendas_detalhe
GROUP BY 1, 2
ORDER BY 1, 2;

-- 5. Após visualizar o resultado na tabela:
--    - Clique em 'SAVE AS' (ou 'Save' no topo da tabela de resultados).
--    - Selecione 'Save as Dataset'.
--    - Nomeie o dataset como: "Faturamento Diario por Regiao".
--    - Clique em 'SAVE & EXPLORE'.
-- 6. No modo de exploração, selecione o tipo de gráfico 'Time-Series Line Chart'
--    ou 'Bar Chart' para visualizar a evolução das vendas diárias por região.
