# Aula 10 — Gráficos, Charts e Construção de Visualizações Eficazes com Análise Exploratória

## 📌 Visão Geral da Aula
A Aula 10 aborda a escolha criteriosa do tipo de gráfico conforme a necessidade da Análise Exploratória de Dados (EDA), dividindo as visualizações em 4 grandes categorias:
1. **Comparação:** Barras, Linhas, Colunas (ex: Vendas por produto, séries temporais).
2. **Composição:** Pizza/Rosca, Barras Empilhadas (ex: Participação de mercado, custos por área).
3. **Distribuição:** Histogramas, Box Plots, Dispersão (ex: Dispersão de valores, faixas salariais).
4. **Relacionamento:** Dispersão (Scatter Plot), Bolhas (Bubble Chart) (ex: Correlação entre preço e demanda).

---

## 🎯 Divisão das Duas Partes Práticas da Aula

### 🔹 Parte 1: Gráficos Exploratórios no Apache Superset com PostgreSQL
- **Banco de Dados:** Conexão com a base de dados `superset_data` e tabela `vendas_teste`.
- **Carga de Dados Adicionais:** Inserção de 12 novos registros abrangendo vendas de outubro e novembro de 2023.
- **Gráficos Criados:**
  1. `Vendas por Produto - Barras` (Bar Chart - Comparação de valores totais por categoria).
  2. `Vendas Mensais - Linhas` (Line Chart - Tendência temporal agrupada por mês).
  3. `Proporção Vendas por Produto - Pizza` (Pie Chart - Proporção de vendas por produto).
  4. `Vendas por Data e Produto - Dispersão` (Scatter Plot - Relação temporal e valor por categoria).
  5. `Vendas por Produto ao Longo dos Meses - Barras Empilhadas` (Stacked Bar Chart - Composição temporal).
  6. `Distribuição dos Valores de Vendas - Histograma` (Histogram - Frequência das faixas de preço/valor).
- **Dashboard Criado:** `Meu Primeiro Dashboard` organizando todas as visualizações em grid estruturado.

### 🔹 Parte 2: Gráfico de Recomendações e Publicação Externa (Concluída)
- **Tabela PostgreSQL criada:** `recomendacoes_produtos` (banco `superset_data`), contendo `produto_origem`, `produto_recomendado`, `categoria`, `similaridade`, `nota_avaliacao` e `total_avaliacoes`.
- **Dataset no Superset:** `recomendacoes_produtos` (ID: 24) no banco "Banco de Vendas".
- **Gráficos Criados no Dashboard de Recomendações:**
  1. `Maior Score de Similaridade` (Big Number / KPI destacando o score de 96.20% do top item recomendado).
  2. `Top Recomendações de Produtos` (Bar Chart com `MAX(similaridade)` ordenado de forma decrescente).
  3. `Recomendações por Categoria - Pizza` (Donut Chart com a proporção de produtos sugeridos por segmento).
  4. `Similaridade vs Nota de Avaliação` (Scatter Plot correlacionando similaridade vetorial com a nota dos clientes).
- **Dashboard Criado:** `Dashboard de Recomendações` (ID: 12, slug: `dashboard_recomendacoes`) com layout em grade 2x2.
- **Acesso Público (Role Public):**
  - Concedidas permissões anônimas: `can_read on Dashboard`, `can_read on Chart`, `can_read on Dataset`, `can_dashboard on Superset`, `can_slice on Superset`, `all_datasource_access on all_datasource_access` e `database_access on [Banco de Vendas]`.
  - Ambos os dashboards podem ser acessados em aba anônima/sem login!

---

## 🔗 Links de Acesso Direto aos Dashboards (Sem Login)

1. **Dashboard de Recomendações (Parte 2):**
   - [http://localhost:8088/superset/dashboard/dashboard_recomendacoes/](http://localhost:8088/superset/dashboard/dashboard_recomendacoes/)
   - Ou por ID: [http://localhost:8088/superset/dashboard/12/](http://localhost:8088/superset/dashboard/12/)

2. **Meu Primeiro Dashboard (Parte 1):**
   - [http://localhost:8088/superset/dashboard/meu_primeiro_dashboard/](http://localhost:8088/superset/dashboard/meu_primeiro_dashboard/)
   - Ou por ID: [http://localhost:8088/superset/dashboard/11/](http://localhost:8088/superset/dashboard/11/)

---

## 📂 Arquivos e Scripts Gerados

- [01_inserir_dados_adicionais.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-10-graficos-charts/01_inserir_dados_adicionais.sql): Inserção dos dados de vendas no PostgreSQL.
- [02_criar_tabela_recomendacoes.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-10-graficos-charts/02_criar_tabela_recomendacoes.sql): Criação e carga da tabela de similaridade de recomendações.
- [setup_aula10_parte1.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-10-graficos-charts/setup_aula10_parte1.py): Provisionamento automático dos 6 gráficos e montagem do Dashboard da Parte 1.
- [setup_aula10_parte2.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-10-graficos-charts/setup_aula10_parte2.py): Provisionamento do Dataset, Gráfico, Dashboard e Role `Public` da Parte 2.

