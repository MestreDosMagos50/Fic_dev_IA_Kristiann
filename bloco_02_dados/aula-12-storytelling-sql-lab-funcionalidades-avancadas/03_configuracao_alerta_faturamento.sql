-- ====================================================================
-- FIC DEV IA – Engenharia de Dados | Aula 12
-- Roteiro Prático 4.4.3: Configurando um Alerta Simples no Superset
-- ====================================================================

-- 1. Consulta base executada internamente pelo gráfico do Superset:
SELECT 
    SUM(faturamento_diario) AS total_faturamento_sudeste
FROM (
    SELECT
        CAST(data_hora_venda AS DATE) AS data_venda,
        regiao_cliente AS regiao,
        SUM(quantidade * preco_unitario) AS faturamento_diario
    FROM vendas_detalhe
    WHERE regiao_cliente = 'Sudeste'
    GROUP BY 1, 2
) AS subquery;

-- 2. Condição do Alerta (Alert Condition no Superset):
-- No Superset, o alerta avalia a expressão sobre o resultado da agregação:
-- SUM(faturamento_diario) < 500

-- Consulta de validação para simulação da regra de disparo:
SELECT 
    CASE 
        WHEN SUM(quantidade * preco_unitario) < 500 THEN TRUE 
        ELSE FALSE 
    END AS alerta_disparado,
    SUM(quantidade * preco_unitario) AS faturamento_atual,
    500 AS limiar_alerta
FROM vendas_detalhe
WHERE regiao_cliente = 'Sudeste';

/*
Passo a passo no Superset:
1. No dataset "Faturamento Diario por Regiao", crie um gráfico tipo "Big Number".
2. Métrica: SUM(faturamento_diario)
3. Filtro simples: regiao == 'Sudeste'
4. Salve o gráfico com o nome: "KPI Faturamento Sudeste".
5. Vá em Settings (ícone de engrenagem) -> Alerts & Reports.
6. Clique em "+ ALERT":
   - Name: Alerta Faturamento Sudeste Baixo
   - Chart: KPI Faturamento Sudeste
   - Owners: Seu Usuário (admin)
   - Frequency: Daily (ex: CRON 0 9 * * *)
   - Alert Condition: < 500 (ou SUM(faturamento_diario) < 500)
   - Message: "O faturamento da região Sudeste caiu abaixo de 500. Verifique o dashboard!"
7. Clique em SAVE.
*/
