-- ====================================================================
-- FIC DEV IA – Engenharia de Dados | Aula 12
-- Roteiro Prático 4.4.4 (Exercício 3) & Seção 4.3.2: Row-Level Security (RLS)
-- ====================================================================

/*
O Row-Level Security (RLS) no Apache Superset injeta dinamicamente cláusulas
WHERE nas consultas executadas pelos usuários, de acordo com seus papéis (roles).

Cenário Prático de Governança de Acesso:
- Gerente Sudeste: Acessa exclusivamente dados da região Sudeste.
- Gerente Sul: Acessa exclusivamente dados da região Sul.
- Gerente Nordeste: Acessa exclusivamente dados da região Nordeste.
- Diretor Nacional: Acessa todas as regiões sem filtro.

--- Regras SQL configuradas no Superset (Settings -> Row Level Security): ---

1. REGRA REGIONAL ESTÁTICA (Por Papel/Role):
   - Name: Filtro Sudeste
   - Filter Type: Regular
   - Tables: vendas_detalhe, Vendas Detalhadas com Produtos
   - Roles: Gerente_Sudeste
   - Clause:
*/
regiao_cliente = 'Sudeste'

/*
2. REGRA PARA GERENTE SUL:
   - Name: Filtro Sul
   - Clause:
*/
regiao_cliente = 'Sul'

/*
3. REGRA DINÂMICA VIA JINJA TEMPLATE (Baseada no Usuário Conectado):
   Caso os usuários possuam atributos vinculados no Superset ou via convenção de nome:
*/
regiao_cliente = '{{ current_user_extra_attributes.get("regiao", "Sudeste") }}'

/*
Como o Superset reescreve a consulta final quando o usuário Gerente_Sudeste visualiza um dashboard:

Consulta Original emitida pelo gráfico:
SELECT regiao_cliente, SUM(quantidade * preco_unitario) AS total
FROM vendas_detalhe
GROUP BY regiao_cliente;

Consulta Reescrita pelo motor RLS do Superset:
SELECT regiao_cliente, SUM(quantidade * preco_unitario) AS total
FROM vendas_detalhe
WHERE (regiao_cliente = 'Sudeste')
GROUP BY regiao_cliente;
*/
