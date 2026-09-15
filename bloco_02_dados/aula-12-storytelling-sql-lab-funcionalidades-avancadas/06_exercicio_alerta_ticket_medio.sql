-- ====================================================================
-- FIC DEV IA – Engenharia de Dados | Aula 12
-- Roteiro Prático 4.4.4 (Exercício 4): Alerta de Ticket Médio
-- ====================================================================

-- 1. Consulta SQL para cálculo do Ticket Médio por Região:
SELECT
    regiao_cliente,
    SUM(quantidade * preco_unitario) AS faturamento_total,
    COUNT(id) AS total_pedidos,
    ROUND(SUM(quantidade * preco_unitario) / COUNT(id), 2) AS ticket_medio
FROM vendas_detalhe
GROUP BY regiao_cliente
ORDER BY ticket_medio ASC;

-- 2. Expressão de Métrica para o gráfico no Apache Superset:
-- Métrica personalizada no Superset:
-- SUM(quantidade * preco_unitario) / COUNT(id)
-- Label: "Ticket Médio (R$)"

-- 3. Configuração do Alerta no Superset (Settings -> Alerts & Reports):
/*
Configurações do Alerta:
- Name: Alerta Ticket Médio Crítico
- Chart: KPI Ticket Médio Geral (ou por Região)
- Frequency: Hourly ou Daily
- Alert Condition:
  ticket_medio < 150.00
- SQL Query alternativa (caso use SQL direto no Alerta):
  SELECT 
      CASE 
          WHEN (SUM(quantidade * preco_unitario) / NULLIF(COUNT(id), 0)) < 150.00 THEN 1 
          ELSE 0 
      END AS alerta_ativo
  FROM vendas_detalhe;
- Message:
  "ATENÇÃO: O Ticket Médio caiu para menos de R$ 150,00. Analise a performance de vendas!"
*/
