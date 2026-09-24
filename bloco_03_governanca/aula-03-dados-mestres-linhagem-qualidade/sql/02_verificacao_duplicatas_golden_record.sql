-- =============================================================================
-- FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
-- Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
-- Arquivo: sql/02_verificacao_duplicatas_golden_record.sql
-- Objetivo: Passo 2 do Mini-Lab — Verificação de Chave Única e Auditoria de Duplicatas
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. TABELA MESTRE: silver.produtos / gold.dim_produto
-- Chave Única Declarada (Golden Record): codigo_produto / codigo
-- -----------------------------------------------------------------------------
-- Consulta de auditoria de duplicatas:
SELECT 
    codigo,
    COUNT(*) as total_ocorrencias,
    STRING_AGG(nome, ' | ') as variacoes_nome
FROM silver.produtos
GROUP BY codigo
HAVING COUNT(*) > 1;

-- Regra de Matching para Produtos (se houver duplicatas):
-- "Normalizar o código removendo pontuação e zeros à esquerda (LPAD); se o código coincidir,
-- eleger como Golden Record o registro com a maior data_cadastro e preço mais recente."


-- -----------------------------------------------------------------------------
-- 2. TABELA MESTRE: silver.clientes / gold.dim_cliente
-- Chave Única Declarada (Golden Record): cliente_id (e secundariamente email normalizado)
-- -----------------------------------------------------------------------------
-- Consulta de auditoria por ID:
SELECT 
    cliente_id,
    COUNT(*) as total_ocorrencias
FROM silver.clientes
GROUP BY cliente_id
HAVING COUNT(*) > 1;

-- Consulta de auditoria por E-mail (detectando mesma pessoa com IDs diferentes no CRM):
SELECT 
    LOWER(TRIM(email)) as email_normalizado,
    COUNT(*) as total_ocorrencias,
    STRING_AGG(cliente_id, ', ') as ids_encontrados,
    STRING_AGG(nome, ' | ') as variacoes_nome
FROM silver.clientes
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1;

-- Regra de Matching para Clientes:
-- "Realizar matching exato por CPF/e-mail em minúsculas e matching difuso (Jaro-Winkler > 0.85) no nome completo;
-- o Golden Record consolida o endereço mais recente e unifica o histórico de compras."


-- -----------------------------------------------------------------------------
-- 3. TABELA MESTRE: silver.conteudos / gold.dim_conteudo
-- Chave Única Declarada (Golden Record): (LOWER(TRIM(titulo)), LOWER(TRIM(autor)))
-- -----------------------------------------------------------------------------
-- Consulta que comprova e isola as duplicatas de negócio na base de 1000 conteúdos:
SELECT 
    LOWER(TRIM(titulo)) as titulo_normalizado,
    LOWER(TRIM(autor)) as autor_normalizado,
    COUNT(*) as total_versoes,
    MIN(conteudo_id) as golden_record_id,
    STRING_AGG(conteudo_id::text, ', ' ORDER BY data_publicacao) as ids_publicados,
    STRING_AGG(data_publicacao::text, ', ' ORDER BY data_publicacao) as datas_publicacao,
    STRING_AGG(carga_horaria_min::text, ' min, ' ORDER BY data_publicacao) as cargas_horarias
FROM staging.conteudos
GROUP BY LOWER(TRIM(titulo)), LOWER(TRIM(autor))
HAVING COUNT(*) > 1
ORDER BY total_versoes DESC, titulo_normalizado;

-- Regra de Matching para Conteúdos Educacionais:
-- "Agrupar por título normalizado (sem acentos/espaços duplos) e nome do autor; definir como Golden Record
-- a publicação original (menor data), preservando na tabela fato o histórico completo de re-publicações."


-- -----------------------------------------------------------------------------
-- 4. TABELA MESTRE: gold.dim_autor
-- Chave Única Declarada (Golden Record): nome_autor (e nome_limpo sem titulação)
-- -----------------------------------------------------------------------------
-- Consulta de auditoria de autores:
SELECT 
    nome_limpo,
    COUNT(*) as variantes_titulacao,
    STRING_AGG(nome_autor, ' | ') as formas_cadastradas
FROM gold.dim_autor
GROUP BY nome_limpo
HAVING COUNT(*) > 1;

-- Regra de Matching para Autores:
-- "Remover prefixos de titulação acadêmica (Dr., Dra., Prof., Profa., Eng.) e aplicar trim;
-- havendo colisão no nome limpo, unificar em um único Golden Record atribuindo a titulação mais alta."
