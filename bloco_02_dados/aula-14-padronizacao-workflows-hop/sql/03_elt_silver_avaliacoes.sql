-- =============================================================================
-- FIC Engenharia de Dados | Aula 03 (Módulo 2): Apache Hop & Orquestração
-- Passo 5 — Desafio ELT: Avaliações com Recorte no Destino (PostgreSQL)
-- Arquivo: sql/03_elt_silver_avaliacoes.sql
-- =============================================================================

-- Justificativa do recorte da fatia no ELT:
-- O negócio demanda análise apenas de avaliações válidas no intervalo regulamentar (1 a 5).
-- Em vez de carregar todos os dados brutos pela memória de uma ferramenta de ETL,
-- os dados brutos já estão na staging e o PostgreSQL executa a filtragem da fatia (WHERE)
-- e higienização em alta velocidade no próprio storage.

INSERT INTO silver.avaliacoes_elt (id_avaliacao, codigo_produto, nota, comentario, data_avaliacao)
SELECT
    TRIM(id_avaliacao),
    TRIM(codigo_produto),
    nota::INTEGER,
    TRIM(comentario),
    CASE 
        WHEN data_avaliacao ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN TO_DATE(data_avaliacao, 'YYYY-MM-DD')
        WHEN data_avaliacao ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' THEN TO_DATE(data_avaliacao, 'DD/MM/YYYY')
        ELSE NULL
    END
FROM staging.avaliacoes
WHERE nota ~ '^[0-9]+$'
  AND (nota::INTEGER BETWEEN 1 AND 5)
ON CONFLICT (id_avaliacao) DO UPDATE
SET nota = EXCLUDED.nota,
    comentario = EXCLUDED.comentario,
    data_avaliacao = EXCLUDED.data_avaliacao,
    carregado_em = CURRENT_TIMESTAMP;

-- Comparação solicitada pelo Desafio:
-- "No pipeline ETL o Hop lê cada avaliação, consome recursos na JVM para aplicar trim e validar notas antes de desovar no banco; no padrão ELT, o dado já pousou na staging e o PostgreSQL utiliza seus índices e engine C otimizada para filtrar e transformar apenas a fatia válida em milissegundos."
