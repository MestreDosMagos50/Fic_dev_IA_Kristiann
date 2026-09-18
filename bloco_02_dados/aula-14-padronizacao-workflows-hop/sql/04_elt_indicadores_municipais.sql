-- =============================================================================
-- FIC Engenharia de Dados | Aula 03 (Módulo 2): Padrão ELT no PostgreSQL
-- Transformação e Cruzamento Analítico das 5 Fontes Brasileiras no Storage
-- Arquivo: sql/04_elt_indicadores_municipais.sql
-- =============================================================================

-- O padrão ELT puro aplicado a dados geográficos e epidemiológicos:
-- 1. As 5 fontes pousaram na staging (IBGE, DataSUS, INMET, CNES, Alertas).
-- 2. O processamento analítico roda 100% no PostgreSQL utilizando JOINs e fórmulas de saúde pública.
-- 3. A transformação é reexecutável e idempotente via ON CONFLICT.

INSERT INTO silver.indicadores_municipais_elt (
    cod_mun_6,
    nome_municipio,
    uf,
    regiao,
    populacao,
    total_casos,
    taxa_incidencia_100k,
    chuva_mm,
    leitos_uti,
    classificacao_risco,
    calculado_em
)
SELECT
    m.cod_mun_6,
    m.nome_municipio,
    m.uf,
    m.regiao,
    m.populacao,
    COALESCE(SUM(d.casos_confirmados), 0)::INTEGER AS total_casos,
    ROUND(
        (COALESCE(SUM(d.casos_confirmados), 0)::NUMERIC / NULLIF(m.populacao, 0)) * 100000, 
        2
    ) AS taxa_incidencia_100k,
    COALESCE(c.chuva_acumulada_mm, 0) AS chuva_mm,
    COALESCE(l.leitos_uti, 0) AS leitos_uti,
    CASE
        WHEN (COALESCE(SUM(d.casos_confirmados), 0)::NUMERIC / NULLIF(m.populacao, 0)) * 100000 >= 500 THEN 'Epidemia'
        WHEN (COALESCE(SUM(d.casos_confirmados), 0)::NUMERIC / NULLIF(m.populacao, 0)) * 100000 >= 300 THEN 'Alto Risco'
        WHEN (COALESCE(SUM(d.casos_confirmados), 0)::NUMERIC / NULLIF(m.populacao, 0)) * 100000 >= 100 THEN 'Médio Risco'
        ELSE 'Baixo Risco'
    END AS classificacao_risco,
    CURRENT_TIMESTAMP
FROM silver.municipios m
LEFT JOIN silver.notificacoes_dengue d ON m.cod_mun_6 = d.cod_mun_6
LEFT JOIN silver.inmet_chuva c ON m.cod_mun_6 = c.cod_mun_6
LEFT JOIN silver.cnes_leitos l ON m.cod_mun_6 = l.cod_mun_6
GROUP BY m.cod_mun_6, m.nome_municipio, m.uf, m.regiao, m.populacao, c.chuva_acumulada_mm, l.leitos_uti
ON CONFLICT (cod_mun_6) DO UPDATE
SET total_casos = EXCLUDED.total_casos,
    taxa_incidencia_100k = EXCLUDED.taxa_incidencia_100k,
    chuva_mm = EXCLUDED.chuva_mm,
    leitos_uti = EXCLUDED.leitos_uti,
    classificacao_risco = EXCLUDED.classificacao_risco,
    calculado_em = CURRENT_TIMESTAMP;
