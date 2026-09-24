-- =============================================================================
-- FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
-- Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
-- Arquivo: sql/01_carga_conteudos_staging_silver_gold.sql
-- Objetivo: Scripts SQL de transformação Staging -> Silver (MDM) -> Gold (Dimensional)
-- =============================================================================

-- 1. STAGING -> SILVER: Deduplicação e Identificação de Golden Record
-- Regra de Matching: LOWER(TRIM(titulo)) + LOWER(TRIM(autor))
-- Regra de Sobrevivência (Survivorship): Menor data_publicacao / menor conteudo_id
WITH cte_classificacao AS (
    SELECT 
        conteudo_id,
        titulo,
        tipo,
        categoria,
        nivel,
        carga_horaria_min,
        data_publicacao,
        descricao,
        autor,
        ROW_NUMBER() OVER (
            PARTITION BY LOWER(TRIM(titulo)), LOWER(TRIM(autor)) 
            ORDER BY data_publicacao ASC, conteudo_id ASC
        ) as rn,
        FIRST_VALUE(conteudo_id) OVER (
            PARTITION BY LOWER(TRIM(titulo)), LOWER(TRIM(autor)) 
            ORDER BY data_publicacao ASC, conteudo_id ASC
        ) as golden_id
    FROM staging.conteudos
)
INSERT INTO silver.conteudos (
    conteudo_id, titulo, tipo, categoria, nivel,
    carga_horaria_min, data_publicacao, descricao, autor,
    is_duplicata, golden_record_id
)
SELECT 
    conteudo_id,
    titulo,
    tipo,
    categoria,
    nivel,
    carga_horaria_min,
    data_publicacao,
    descricao,
    autor,
    CASE WHEN rn > 1 THEN TRUE ELSE FALSE END as is_duplicata,
    golden_id
FROM cte_classificacao
ON CONFLICT (conteudo_id) DO NOTHING;

-- 2. SILVER -> GOLD: Dimensão Categoria (Dado de Referência)
INSERT INTO gold.dim_categoria (nome_categoria, macro_area, total_titulos)
SELECT 
    categoria,
    CASE 
        WHEN categoria IN ('Engenharia de Dados', 'DevOps & Cloud', 'Banco de Dados') THEN 'Infraestrutura & Engenharia'
        WHEN categoria IN ('Business Intelligence', 'Ciência de Dados', 'Inteligência Artificial') THEN 'Analytics & Inteligência Artificial'
        ELSE 'Engenharia de Software & Governança'
    END as macro_area,
    COUNT(DISTINCT conteudo_id)
FROM silver.conteudos
GROUP BY categoria
ON CONFLICT (nome_categoria) DO UPDATE 
SET total_titulos = EXCLUDED.total_titulos,
    atualizado_em = CURRENT_TIMESTAMP;

-- 3. SILVER -> GOLD: Dimensão Autor (Master Data)
INSERT INTO gold.dim_autor (nome_autor, titulacao, nome_limpo, total_conteudos, total_horas, categoria_principal)
SELECT 
    autor,
    CASE 
        WHEN autor LIKE 'Profa.%' THEN 'Professora'
        WHEN autor LIKE 'Prof.%' THEN 'Professor'
        WHEN autor LIKE 'Dra.%' THEN 'Doutora'
        WHEN autor LIKE 'Dr.%' THEN 'Doutor'
        WHEN autor LIKE 'Eng.%' THEN 'Engenheiro(a)'
        ELSE 'Especialista'
    END as titulacao,
    REGEXP_REPLACE(autor, '^(Profa\.|Prof\.|Dra\.|Dr\.|Eng\.)\s*', '') as nome_limpo,
    COUNT(*) as total_conteudos,
    ROUND(SUM(carga_horaria_min)::numeric / 60, 2) as total_horas,
    MODE() WITHIN GROUP (ORDER BY categoria) as categoria_principal
FROM silver.conteudos
GROUP BY autor
ON CONFLICT (nome_autor) DO UPDATE 
SET total_conteudos = EXCLUDED.total_conteudos,
    total_horas = EXCLUDED.total_horas,
    atualizado_em = CURRENT_TIMESTAMP;

-- 4. SILVER -> GOLD: Dimensão Conteúdo (Master Data / Golden Record Unificado)
INSERT INTO gold.dim_conteudo (
    conteudo_id, titulo, tipo, categoria, nivel, 
    carga_horaria_min, carga_horaria_horas, autor, 
    data_primeira_publicacao, versoes_identificadas
)
SELECT 
    s.golden_record_id,
    s.titulo,
    s.tipo,
    s.categoria,
    s.nivel,
    s.carga_horaria_min,
    ROUND(s.carga_horaria_min::numeric / 60, 2),
    s.autor,
    s.data_publicacao,
    sub.qtd_versoes
FROM silver.conteudos s
JOIN (
    SELECT golden_record_id, count(*) as qtd_versoes
    FROM silver.conteudos
    GROUP BY golden_record_id
) sub ON sub.golden_record_id = s.golden_record_id
WHERE s.is_duplicata = FALSE
ON CONFLICT (conteudo_id) DO UPDATE 
SET versoes_identificadas = EXCLUDED.versoes_identificadas,
    atualizado_em = CURRENT_TIMESTAMP;

-- 5. SILVER -> GOLD: Fato Publicações (Transacional)
INSERT INTO gold.fato_publicacoes (
    conteudo_id, sk_conteudo, sk_autor, sk_categoria, 
    tipo, nivel, data_publicacao, ano_publicacao, mes_publicacao, 
    carga_horaria_min, carga_horaria_horas
)
SELECT 
    s.conteudo_id,
    dc.sk_conteudo,
    da.sk_autor,
    dcat.sk_categoria,
    s.tipo,
    s.nivel,
    s.data_publicacao,
    EXTRACT(YEAR FROM s.data_publicacao)::int,
    EXTRACT(MONTH FROM s.data_publicacao)::int,
    s.carga_horaria_min,
    ROUND(s.carga_horaria_min::numeric / 60, 2)
FROM silver.conteudos s
JOIN gold.dim_conteudo dc ON dc.conteudo_id = s.golden_record_id
JOIN gold.dim_autor da ON da.nome_autor = s.autor
JOIN gold.dim_categoria dcat ON dcat.nome_categoria = s.categoria;
