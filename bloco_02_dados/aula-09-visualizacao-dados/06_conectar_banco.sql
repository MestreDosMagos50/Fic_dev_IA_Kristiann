CREATE TABLE vendas_teste (
 id SERIAL PRIMARY KEY,
 data_venda DATE,
 produto VARCHAR(50),
 valor NUMERIC(10,2)
);

INSERT INTO vendas_teste (data_venda, produto, valor) VALUES
('2023-10-01', 'Produto A', 150.00),
('2023-10-02', 'Produto B', 200.50),
('2023-10-03', 'Produto A', 120.00);
