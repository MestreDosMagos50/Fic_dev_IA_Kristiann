# 🗺️ Guia de Linhagem de Dados: Métodos de Captura, Impacto e Causa Raiz

## 1. O que é Linhagem de Dados?

A **Linhagem de Dados (*Data Lineage*)** é a história completa do caminho percorrido pelo dado:
- De onde ele se originou (**Origem / Fonte**);
- Por quais transformações, filtros, deduplicações e agregações passou (**Processamento / Pipeline**);
- Em quais tabelas intermediárias e modelos dimensionais residiu (**Armazenamento**);
- Onde e por quem ele é consumido (**Dashboards, Relatórios, Modelos de ML e APIs**).

A linhagem pode existir em dois níveis de granularidade:
- **Nível de Tabela (*Table-level Lineage*):** Demonstra dependências entre conjuntos de dados inteiros.
- **Nível de Coluna (*Column-level Lineage*):** Mostra exatamente de qual coluna de origem derivou um cálculo específico na tabela destino (ex: `gold.fato_vendas.valor_liquido` deriva de `silver.vendas.valor_total` subtraído de impostos).

---

## 2. Como as Plataformas Modernas (OpenMetadata) Capturam a Linhagem

Existem três caminhos arquiteturais para registrar e manter a linhagem em um catálogo de dados:

### A. Automática via Análise de Query Logs (*Query Log Parsing*)
- **Como funciona:** O conector do catálogo lê o log de execução de consultas SQL do Data Warehouse (ex: Snowflake, BigQuery, PostgreSQL). Um analisador de dialetos SQL (*SQL Parser*) detecta comandos como `CREATE TABLE AS SELECT`, `INSERT INTO ... SELECT` e `MERGE`, inferindo automaticamente quais tabelas leram de quais fontes.
- **Vantagem:** Totalmente automatizado e agnóstico da ferramenta de ETL.
- **Limitação:** Não captura transformações realizadas fora do banco (ex: pipelines em Python Pandas, Apache Spark em memória ou Apache Hop).

### B. Por Conectores Nativos de Orquestração (*Pipeline Connectors*)
- **Como funciona:** Ferramentas de engenharia como Apache Airflow (via plugin OpenLineage), dbt (via manifest.json), Dagster e Fivetran publicam suas dependências de tarefas e DAGs diretamente na API do catálogo.
- **Vantagem:** Captura o contexto exato do pipeline com horários de execução e status de sucesso/falha.
- **Limitação:** Exige suporte e configuração de plugins específicos em cada ferramenta.

### C. Manual via Interface / API REST (*Manual Lineage*)
- **Como funciona:** O engenheiro ou arquiteto de dados desenha visualmente as conexões entre os ativos na interface web do OpenMetadata ou consome a API REST (`PUT /api/v1/lineage`).
- **Valor Didático e Estratégico:** Obriga o profissional a reconstruir mentalmente o pipeline de dados de ponta a ponta, permitindo catalogar ferramentas que não possuem conector nativo (como o **Apache Hop**).
- **⚠️ O Custo da Linhagem Manual:**
  > *Linhagem manual não se atualiza sozinha.* Se você modificar o pipeline e não atualizar o catálogo de metadados, a linhagem passa a **mentir**. Uma linhagem desatualizada é mais perigosa que a ausência de linhagem, pois gera falsas certezas que induzem a erros graves durante incidentes.

---

## 3. As Duas Grandes Aplicações da Linhagem

Saber articular essas duas investigações é fundamental em projetos de governança:

### 1. Análise de Impacto (*Impact Analysis*) — Olhar para Frente (Downstream)
- **Quando usar:** Antes de realizar qualquer alteração estrutural no banco (ex: mudar o tipo de uma coluna, renomear uma tabela, depreciar uma view ou aplicar refatoração de schema).
- **A pergunta do engenheiro:** *"Se eu alterar ou quebrar esta tabela agora, quais relatórios, dashboards e modelos de inteligência artificial vão parar de funcionar lá na frente?"*
- **Ação:** Identificar todos os consumidores downstream e enviar um comunicado prévio de manutenção com plano de mitigação.

### 2. Análise de Causa Raiz (*Root Cause Analysis*) — Olhar para Trás (Upstream)
- **Quando usar:** Durante a investigação de incidentes e alertas de qualidade (ex: o dashboard executivo amanheceu com a métrica de margem de contribuição zerada).
- **A pergunta do engenheiro:** *"Este número está incorreto na ponta final; qual pipeline, script ou arquivo fonte se corrompeu ao longo do caminho para trás?"*
- **Ação:** Seguir a trilha da direita para a esquerda, testando a integridade das camadas intermediárias até encontrar o ponto exato da quebra.
