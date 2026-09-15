-- ====================================================================
-- FIC DEV IA – Engenharia de Dados | Aula 12
-- Roteiro Prático 4.4.4 (Exercício 2): Criação de Dataset com JOINs
-- ====================================================================

-- Objetivo: Unir vendas_detalhe com a tabela dimensional produtos_master
-- para permitir análises por Categoria de Produto, Custo e Margem de Lucro.

SELECT
    v.id AS venda_id,
    v.data_hora_venda,
    CAST(v.data_hora_venda AS DATE) AS data_venda,
    v.cliente_id,
    v.regiao_cliente,
    p.id AS produto_id,
    p.nome_produto,
    p.categoria AS categoria_produto,
    v.quantidade,
    v.preco_unitario,
    p.custo_unitario,
    (v.quantidade * v.preco_unitario) AS faturamento_bruto,
    (v.quantidade * p.custo_unitario) AS custo_total,
    (v.quantidade * (v.preco_unitario - p.custo_unitario)) AS lucro_bruto
FROM vendas_detalhe v
INNER JOIN produtos_master p ON v.produto_id = p.id
ORDER BY v.data_hora_venda DESC;

/*
Como utilizar no Apache Superset:
1. Abra o SQL Lab -> SQL Editor.
2. Execute a consulta acima.
3. Clique em 'Save As' -> 'Save as Dataset'.
4. Nomeie como: "Vendas Detalhadas com Produtos".
5. Clique em 'Save & Explore'.
6. Crie um gráfico como:
   - Tipo: Bar Chart (ECharts) ou Pie Chart
   - Métrica: SUM(faturamento_bruto) ou SUM(lucro_bruto)
   - Dimensão / Agrupamento: categoria_produto
*/
