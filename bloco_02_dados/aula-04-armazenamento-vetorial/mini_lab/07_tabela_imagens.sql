-- 4.5 Atividade Prática Extra: Busca Semântica Multimodal

-- Garante que a extensão vector está habilitada
CREATE EXTENSION IF NOT EXISTS vector;

-- Cria a tabela para armazenar os metadados e os embeddings das imagens
-- O modelo CLIP (clip-ViT-B-32) gera vetores de 512 dimensões!
CREATE TABLE IF NOT EXISTS catalogo_imagens (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(100),
    url_ou_caminho TEXT,
    embedding vector(512)
);
