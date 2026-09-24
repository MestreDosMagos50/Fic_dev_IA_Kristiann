# 🧭 Passo 3 — Linhagem de Dados Ponta a Ponta: Análise de Impacto e Causa Raiz

A linhagem de dados (*Data Lineage*) é a representação cartográfica do ciclo de vida dos dados: desde suas fontes geradoras, passando pelas transformações das camadas Medalhão, até as tabelas agregadas e painéis de consumo.

No OpenMetadata, a linhagem permite conduzir duas investigações operacionais críticas e opostas:
1. **Análise de Impacto (*Impact Analysis*)** — Olhar para frente (**Downstream**): *"Se eu alterar ou corromper este ativo, o que quebra lá na frente?"*
2. **Análise de Causa Raiz (*Root Cause Analysis*)** — Olhar para trás (**Upstream**): *"Este número no dashboard está incorreto; onde ele se corrompeu ao longo do caminho?"*

---

## 🗺️ Mapa Completo da Linhagem no Ecossistema

### Fluxo 1: Pipeline E-Commerce (`gold.fato_vendas`)

```text
[produtos.csv] ──> staging.produtos ──> silver.produtos ──> gold.dim_produto ────┐
                                                                                  │
[clientes.csv] ──> staging.clientes ──> silver.clientes ──> gold.dim_cliente ────┼──> gold.fato_vendas ──> Dashboard Executivo
                                                                                  │
[vendas.csv]   ──> staging.vendas   ──> silver.vendas   ─────────────────────────┘
```

### Fluxo 2: Pipeline de Conteúdos Educacionais (`dados/conteudos.csv`)

```text
                                                        ┌──> gold.dim_conteudo ──┐
                                                        │                        │
[conteudos.csv] ──> staging.conteudos ──> silver.conteudos ──> gold.dim_autor ───┼──> gold.fato_publicacoes ──> Portal de Governança
                                                        │                        │
                                                        └──> gold.dim_categoria ─┘
```

---

## 🔍 Respostas Formais do Desafio (Passo 3)

### Questão (a): Se `silver.vendas` for corrompida, quais ativos são impactados? (Análise de Impacto / Downstream)

Se a tabela `silver.vendas` sofrer qualquer corrupção (ex: campos nulos, registros truncados, tipos incorretos ou valores duplicados), o grafo de linhagem revela o impacto imediato em cascata:

1. **`gold.fato_vendas` (Impacto Crítico Imediato):**
   - Esta tabela fato consome diretamente os registros de `silver.vendas` para realizar os lookups de surrogate keys (`sk_cliente`, `sk_produto`) e computar os valores analíticos (`valor_liquido`, `margem_lucro`).
   - Se `silver.vendas` for corrompida, as cargas incrementais da fato falharão (quebrando integridade referencial ou gerando valores financeiros errados).
2. **Consultas Analíticas e Datamarts:**
   - Quaisquer agregações de faturamento diário, ticket médio mensal e curva ABC de produtos que dependam de `fato_vendas`.
3. **Dashboards Executivos de BI (Apache Superset / Tableau / Power BI):**
   - Os painéis de faturamento e vendas por categoria apresentarão distorções ou erros de renderização.
4. **Relatórios da Diretoria e Tomada de Decisão:**
   - Decisões de investimento de marketing, reposição de estoque e fechamento contábil serão tomadas com base em números inválidos.

> **Importante:** As dimensões `gold.dim_produto` e `gold.dim_cliente` **NÃO** são impactadas downstream por `silver.vendas`, pois elas alimentam a fato de forma paralela e independente.

---

### Questão (b): Se `fato_vendas` estiver errada, quais são os suspeitos a investigar, em ordem? (Análise de Causa Raiz / Upstream)

Quando a diretoria reclama que "o faturamento da categoria Casa caiu 40%", o engenheiro de dados deve percorrer a árvore de linhagem no sentido **upstream (da direita para a esquerda)** na seguinte ordem estrita:

1. **1º Suspeito: A própria carga e query de transformação de `gold.fato_vendas`**
   - **O que checar:** O pipeline de carga da fato (ex: script de transformação ou job Apache Hop `fato_vendas.hpl`).
   - **Hipótese:** Houve falha no cálculo do join? Algum `INNER JOIN` com as dimensões filtrou registros de vendas sem chave correspondente? A regra de conversão de moeda mudou?
2. **2º Suspeito: A tabela intermediária transacional `silver.vendas`**
   - **O que checar:** A integridade dos dados brutos processados ontem.
   - **Hipótese:** A carga de ontem veio zerada ou parcial? Houve falha no parsing de datas ou conversão de string para numérico? A tabela `silver.rejeitados` tem registros anômalos de vendas descartadas?
3. **3º Suspeito: As dimensões mestras `gold.dim_produto` e `gold.dim_cliente`**
   - **O que checar:** A integridade cadastral das entidades mestras.
   - **Hipótese:** Um produto da categoria "Casa" foi recadastrado com outro nome ou código duplicado? A categoria foi renomeada para "Utilidades Domésticas" no ERP sem atualização do mapeamento?
4. **4º Suspeito: A camada Staging (`staging.vendas`, `staging.produtos`, `staging.clientes`)**
   - **O que checar:** Os dados brutos recém-chegados do lago ou banco operacional.
   - **Hipótese:** A exportação do ERP falhou pela metade? Houve mudança no layout do arquivo CSV ou JSON de origem?
5. **5º Suspeito: A fonte de origem externa (Sistemas Operacionais / Arquivos Brutos)**
   - **O que checar:** O banco de dados do e-commerce, a API de pagamentos ou o arquivo de dump.
   - **Hipótese:** O gateway de pagamento ficou fora do ar no domingo? A integração de checkout parou de enviar eventos?

---

### Questão (c): Aplicação da Linhagem ao Dataset de Conteúdos Educacionais (`conteudos.csv`)

Aplicando a mesma disciplina ao pipeline de 1000 conteúdos:

- **Análise de Impacto:** Se `silver.conteudos` for corrompida, **quatro ativos downstream** são diretamente atingidos:
  - `gold.dim_conteudo` (perde a consolidação de *Golden Records*);
  - `gold.dim_autor` (cálculo de horas produzidas e total de publicações por instrutor fica incorreto);
  - `gold.dim_categoria` (contagem de títulos e distribuição de macro-áreas fica distorcida);
  - `gold.fato_publicacoes` (relatórios analíticos de engajamento e métricas de produção quebram).
- **Análise de Causa Raiz:** Se o total de horas de um autor estiver divergente na dimensão `gold.dim_autor`:
  - **1º:** Verificar a agregação em `gold.dim_autor` (fórmula de soma e agrupamento).
  - **2º:** Verificar a normalização de títulos acadêmicos e flags de duplicatas em `silver.conteudos`.
  - **3º:** Verificar os valores brutos de `carga_horaria_min` em `staging.conteudos`.
  - **4º:** Auditar a linha correspondente no arquivo `conteudos.csv` original.
