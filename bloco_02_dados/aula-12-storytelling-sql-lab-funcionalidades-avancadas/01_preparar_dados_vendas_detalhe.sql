-- ====================================================================
-- FIC DEV IA – Engenharia de Dados | Aula 12
-- Roteiro Prático 4.4.1: Preparação de Dados - Tabela de Vendas Detalhada
-- ====================================================================

-- Conectar ao banco PostgreSQL (superset_data):
-- psql -h localhost -U superset_user -d superset_data

-- 1. Criação da tabela dimensional de produtos (para suporte aos exercícios de JOIN)
CREATE TABLE IF NOT EXISTS produtos_master (
    id INT PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    custo_unitario NUMERIC(10,2) NOT NULL
);

INSERT INTO produtos_master (id, nome_produto, categoria, custo_unitario) VALUES
(1, 'Notebook Pro', 'Hardware', 100.00),
(2, 'Monitor UltraWide', 'Periféricos', 120.00),
(3, 'Teclado Mecânico', 'Acessórios', 40.00)
ON CONFLICT (id) DO NOTHING;

-- 2. Criação da tabela de vendas detalhada
DROP TABLE IF EXISTS vendas_detalhe CASCADE;

CREATE TABLE vendas_detalhe (
    id SERIAL PRIMARY KEY,
    data_hora_venda TIMESTAMP NOT NULL,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(10,2) NOT NULL,
    cliente_id VARCHAR(50) NOT NULL,
    regiao_cliente VARCHAR(50) NOT NULL,
    CONSTRAINT fk_produto FOREIGN KEY (produto_id) REFERENCES produtos_master (id)
);

-- 3. Inserção dos dados da apostila
-- Nota: No PostgreSQL, literais de texto utilizam aspas simples ('...')
INSERT INTO vendas_detalhe (data_hora_venda, produto_id, quantidade, preco_unitario, cliente_id, regiao_cliente) VALUES
('2023-10-01 10:00:00', 1, 2, 150.00, 'C001', 'Sudeste'),
('2023-10-01 11:30:00', 2, 1, 200.50, 'C002', 'Sul'),
('2023-10-02 14:00:00', 1, 1, 150.00, 'C003', 'Sudeste'),
('2023-10-02 16:45:00', 3, 3, 75.00,  'C001', 'Sudeste'),
('2023-10-03 09:15:00', 2, 1, 200.50, 'C004', 'Nordeste'),
('2023-10-03 13:00:00', 1, 1, 150.00, 'C005', 'Sul'),
('2023-11-01 10:00:00', 1, 2, 150.00, 'C006', 'Sudeste'),
('2023-11-01 11:30:00', 2, 1, 200.50, 'C007', 'Sul'),
('2023-11-02 14:00:00', 1, 1, 150.00, 'C008', 'Sudeste'),
('2023-11-02 16:45:00', 3, 3, 75.00,  'C006', 'Sudeste');

-- 4. Verificação dos dados inseridos
SELECT * FROM vendas_detalhe ORDER BY id;
