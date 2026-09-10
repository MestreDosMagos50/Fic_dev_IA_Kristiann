-- 4.4.2 Criando uma Tabela com Vetores

CREATE TABLE documentos (
 id SERIAL PRIMARY KEY,
 conteudo TEXT,
 embedding vector(3) -- Vetor de 3 dimensões para simplificar
);
