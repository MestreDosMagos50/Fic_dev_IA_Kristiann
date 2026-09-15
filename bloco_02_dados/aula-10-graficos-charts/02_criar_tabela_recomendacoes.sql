-- Tabela de Recomendações de Produtos para a Parte 2 da Aula 10
-- Banco: superset_data

CREATE TABLE IF NOT EXISTS recomendacoes_produtos (
    id SERIAL PRIMARY KEY,
    produto_origem VARCHAR(100) NOT NULL,
    produto_recomendado VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    similaridade NUMERIC(5, 4) NOT NULL,
    nota_avaliacao NUMERIC(3, 1),
    total_avaliacoes INT
);

INSERT INTO recomendacoes_produtos (produto_origem, produto_recomendado, categoria, similaridade, nota_avaliacao, total_avaliacoes) VALUES
('Notebook Gamer X', 'Mouse Sem Fio Ultra', 'Acessórios', 0.9620, 4.8, 320),
('Notebook Gamer X', 'Teclado Mecânico RGB', 'Acessórios', 0.9150, 4.7, 215),
('Notebook Gamer X', 'Headset 7.1 Surround', 'Áudio', 0.8840, 4.6, 180),
('Notebook Gamer X', 'Monitor 144Hz IPS', 'Monitores', 0.8520, 4.9, 410),
('Notebook Gamer X', 'Suporte Ergonômico Alumínio', 'Suportes', 0.7950, 4.5, 95),
('Notebook Gamer X', 'Mochila Impermeável Tech', 'Acessórios', 0.7410, 4.4, 130),
('Notebook Gamer X', 'Webcam Full HD 60fps', 'Câmeras', 0.6830, 4.3, 85);
