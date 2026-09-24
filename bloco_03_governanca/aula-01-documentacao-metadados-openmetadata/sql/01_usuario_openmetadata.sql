-- =============================================================================
-- FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
-- Aula 01: Conceitos de Documentação, Metadados e Governança de Dados
-- Arquivo: sql/01_usuario_openmetadata.sql
-- Objetivo: Criar usuário somente-leitura com Princípio do Menor Privilégio
-- Banco: meu_banco_de_dados
-- =============================================================================

-- DICA DA APOSTILA (Página 5):
-- "Crie um usuário PostgreSQL somente-leitura para o OpenMetadata (GRANT USAGE ON SCHEMA
-- e GRANT SELECT). Uma ferramenta de catálogo nunca precisa escrever nos seus dados — e
-- princípio do menor privilégio é matéria de governança tanto quanto documentação."

-- 1. Criação do Usuário de Governança
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'openmetadata_user') THEN
      CREATE ROLE openmetadata_user WITH LOGIN PASSWORD 'openmetadata_pass123';
   ELSE
      ALTER ROLE openmetadata_user WITH PASSWORD 'openmetadata_pass123';
   END IF;
END
$do$;

-- 2. Permissão de Conexão ao Banco de Dados do E-commerce
GRANT CONNECT ON DATABASE meu_banco_de_dados TO openmetadata_user;

-- 3. Permissão de USAGE nos Schemas Relevantes (Permite navegar e listar metadados)
GRANT USAGE ON SCHEMA public TO openmetadata_user;
GRANT USAGE ON SCHEMA staging TO openmetadata_user;
GRANT USAGE ON SCHEMA silver TO openmetadata_user;
GRANT USAGE ON SCHEMA gold TO openmetadata_user;

-- 4. Permissão Exclusiva de LEITURA (SELECT) em Todas as Tabelas Existentes
GRANT SELECT ON ALL TABLES IN SCHEMA public TO openmetadata_user;
GRANT SELECT ON ALL TABLES IN SCHEMA staging TO openmetadata_user;
GRANT SELECT ON ALL TABLES IN SCHEMA silver TO openmetadata_user;
GRANT SELECT ON ALL TABLES IN SCHEMA gold TO openmetadata_user;

-- 5. Configuração de Privilégios Padrão para Tabelas Criadas Futuramente
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO openmetadata_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA staging GRANT SELECT ON TABLES TO openmetadata_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA silver GRANT SELECT ON TABLES TO openmetadata_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA gold GRANT SELECT ON TABLES TO openmetadata_user;

-- 6. Garantia de Bloqueio Estrito de Escrita (Revogação Explícita de privilégios de modificação)
REVOKE CREATE ON SCHEMA public FROM openmetadata_user;
REVOKE CREATE ON SCHEMA staging FROM openmetadata_user;
REVOKE CREATE ON SCHEMA silver FROM openmetadata_user;
REVOKE CREATE ON SCHEMA gold FROM openmetadata_user;

-- Comentário explicativo registrado no próprio catálogo do PostgreSQL
COMMENT ON ROLE openmetadata_user IS 'Usuario de Servico de Governanca (OpenMetadata) - Apenas Leitura e Metadados';
