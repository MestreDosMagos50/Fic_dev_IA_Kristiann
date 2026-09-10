-- 4.4.1 Instalação do pgvector (Habilitar a extensão)
-- Conecte-se ao seu banco de dados PostgreSQL antes:
-- psql -U seu_usuario -d meu_banco_de_dados

CREATE EXTENSION IF NOT EXISTS vector;

-- Verifique se a extensão foi instalada no psql usando o comando:
-- \dx
