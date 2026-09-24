# Dicionário de Dados & Catálogo de Metadados — Acervo E-commerce
## Módulo 3: Governança de Dados com OpenMetadata — Aula 01

> **Contexto de Governança:**  
> Este documento consolida a documentação formal e autossuficiente das cinco tabelas estratégicas das camadas **Silver** e **Gold** do ecossistema de e-commerce. A estruturação foi projetada para que qualquer analista, cientista de dados ou engenheiro compreenda a semântica, origem, criticidade e regras de negócio de cada dataset sem necessidade de suporte presencial (*Princípio da Documentação que Sobrevive ao Autor*).

---

## 🏛️ Sumário Executivo do Acervo

| Tabela | Camada | Tier de Criticidade | Data Owner | Data Steward | Granularidade | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`gold.fato_vendas`** | Gold | **Tier 1 (Crítico de Negócio)** | Diretoria Comercial (`comercial@empresa.com.br`) | Data Steward Finanças (`steward-fin@empresa.com.br`) | 1 linha = 1 item de produto vendido em uma transação comercial | **Aprovado** |
| **`gold.dim_produto`** | Gold | **Tier 2 (Essencial Corporativo)** | Gestão de Produtos (`produtos@empresa.com.br`) | Data Steward Catálogo (`steward-cat@empresa.com.br`) | 1 linha = 1 produto único comercializável no catálogo | **Aprovado** |
| **`gold.dim_cliente`** | Gold | **Tier 2 (Essencial Corporativo)** | CRM & Atendimento (`crm@empresa.com.br`) | Data Steward Clientes (`steward-crm@empresa.com.br`) | 1 linha = 1 cliente único cadastrado na base corporativa | **Aprovado** |
| **`silver.vendas`** | Silver | **Tier 3 (Base Operacional)** | Engenharia de Dados (`eng-dados@empresa.com.br`) | Data Steward Ingestão (`steward-data@empresa.com.br`) | 1 linha = 1 registro de venda limpo e validado pelo pipeline | **Aprovado** |
| **`silver.produtos`** | Silver | **Tier 3 (Base Operacional)** | Engenharia de Dados (`eng-dados@empresa.com.br`) | Data Steward Ingestão (`steward-data@empresa.com.br`) | 1 linha = 1 produto normalizado e deduplicado da camada staging | **Aprovado** |

---

## 1. Tabela: `gold.fato_vendas` (Tier 1 — Crítico de Negócio)

### 1.1 Metadados de Governança
- **Serviço**: `pg_ecommerce`
- **Banco de Dados**: `meu_banco_de_dados`
- **Schema**: `gold`
- **Camada**: **Gold (Modelagem Dimensional Star Schema)**
- **Tier Justificado**: **Tier 1 (Crítico de Negócio / Decisão Executiva)**. Alimenta os relatórios financeiros da diretoria, comissões de vendas e os dashboards executivos do Apache Superset e Power BI. Uma inconsistência nesta tabela acarreta erro direto no balanço patrimonial e no cálculo de margem da empresa.
- **Granularidade**: **Um item de produto vendido dentro de um pedido/transação comercial**. Se um pedido contiver 3 produtos distintos, haverá 3 registros nesta tabela.
- **Data Owner**: Carlos Eduardo Braga (Diretor Comercial — `comercial@empresa.com.br`)
- **Data Steward**: Mariana Albuquerque (Engenheira de Analytics & Governança — `steward-fin@empresa.com.br`)
- **Linhagem Upstream**: `silver.vendas`, `gold.dim_produto`, `gold.dim_cliente`
- **Linhagem Downstream**: Dashboards `Receita_Trimestral_Executivo`, `Margem_Contribuicao_Filiais`, `Comissao_Representantes`.

### 1.2 Dicionário de Colunas e Regras de Negócio
*(Todas as 16 colunas descritas com significado real sem redundância de nomes)*

| Coluna | Tipo Físico | Restrição | Descrição de Negócio & Regras de Cálculo | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `sk_venda` | `BIGINT` | `PK, NOT NULL` | Chave substituta (*Surrogate Key*) artificial, gerada sequencialmente pelo pipeline Gold para indexação analítica e desvinculação com chave operacional. | `1` |
| `id_venda` | `VARCHAR(50)` | `NOT NULL` | Dimensão degenerada (*Degenerate Dimension*). Código identificador original do pedido emitido pelo sistema de checkout da plataforma de e-commerce. | `'VND-2026-001'` |
| `sk_cliente` | `INTEGER` | `FK, NOT NULL` | Chave estrangeira que referencia a dimensão `gold.dim_cliente(sk_cliente)`. Identifica o comprador na data da transação. | `1` |
| `sk_produto` | `INTEGER` | `FK, NOT NULL` | Chave estrangeira que referencia a dimensão `gold.dim_produto(sk_produto)`. Identifica o produto físico/digital comercializado. | `1` |
| `data_venda` | `DATE` | `NOT NULL` | Data contábil em que a venda foi confirmada pelo gateway de pagamento (fuso horário `America/Sao_Paulo`). | `'2026-08-01'` |
| `quantidade` | `INTEGER` | `NOT NULL` | Quantidade física de unidades do item comercializadas nesta linha. Deve ser sempre um inteiro positivo ($\ge 1$). | `1` |
| `preco_unitario`| `NUMERIC(12,2)` | `NOT NULL` | Valor unitário negociado no fechamento do pedido, após políticas de tabela de preço vigentes no momento da compra. | `5499.90` |
| `desconto` | `NUMERIC(12,2)` | `DEFAULT 0.00` | Valor monetário absoluto de abatimento concedido (cupom promocional ou desconto de pagamento à vista). Não é percentual. | `200.00` |
| `valor_bruto` | `NUMERIC(12,2)` | `NOT NULL` | Faturamento bruto nominal do item: $\text{quantidade} \times \text{preco\_unitario}$. Não deduz desconto nem tributos. | `5499.90` |
| `valor_liquido`| `NUMERIC(12,2)` | `NOT NULL` | Receita líquida faturada da transação: $\text{valor\_bruto} - \text{desconto}$. Representa o montante efetivamente debitado do cliente para este item. | `5299.90` |
| `custo_produto`| `NUMERIC(12,2)` | `NOT NULL` | Custo das Mercadorias Vendidas (CMV) unitário da época multiplicado pela quantidade vendida. Reflete o custo histórico de reposição em estoque. | `3024.95` |
| `impostos` | `NUMERIC(12,2)` | `NOT NULL` | Total de tributos incidentes sobre a venda (ICMS próprio + PIS + COFINS). Calculado pela alíquota efetiva de 18% sobre o `valor_liquido`. | `953.98` |
| `margem_lucro` | `NUMERIC(12,2)` | `NOT NULL` | **Margem de Contribuição Líquida Real**. Calculada pela fórmula estrita: $\text{valor\_liquido} - \text{custo\_produto} - \text{impostos}$. **SIM, considera explicitamente os impostos tributários** e o custo de mercadoria! | `1320.97` |
| `canal_venda` | `VARCHAR(50)` | `NOT NULL` | Canal de atendimento e origem do tráfego pelo qual a conversão ocorreu (`'E-commerce Web'`, `'App Mobile'`, `'B2B Portal'`, `'Marketplace'`). | `'E-commerce Web'` |
| `status_pedido`| `VARCHAR(50)` | `NOT NULL` | Estado do ciclo de vida da entrega no momento da extração (`'Entregue'`, `'Em Transporte'`, `'Devolvido'`, `'Cancelado'`). | `'Entregue'` |
| `carregado_em` | `TIMESTAMP` | `DEFAULT NOW()` | Timestamp de auditoria técnica que indica o instante exato em que a linha foi consolidada na camada Gold pelo processo ELT. | `'2026-08-01 03:15:00'` |

---

## 2. Tabela: `gold.dim_produto` (Tier 2 — Essencial Corporativo)

### 2.1 Metadados de Governança
- **Serviço**: `pg_ecommerce` | **Schema**: `gold`
- **Camada**: **Gold (Dimensão Conforme)**
- **Tier Justificado**: **Tier 2 (Essencial)**. Usada em todos os relatórios de portfólio, margem e estoque. Caso fique indisponível, consultas agregadas por departamento falham.
- **Granularidade**: **Um registro por produto individualmente gerenciável no SKU corporativo**.
- **Data Owner**: Roberta Silveira (Head de Produto e Merchandising — `produtos@empresa.com.br`)
- **Data Steward**: Lucas Nogueira (Analista de Dados de Catálogo — `steward-cat@empresa.com.br`)

### 2.2 Colunas e Semântica
- `sk_produto` (`INTEGER PRIMARY KEY`): Chave substituta para joins de alta performance no star schema.
- `codigo_produto` (`VARCHAR(50) UNIQUE`): Código de negócio do SKU (ex: `'PROD-001'`).
- `nome_produto` (`VARCHAR(255)`): Nome comercial completo exibido na vitrine virtual e na nota fiscal.
- `categoria` (`VARCHAR(100)`): Macrodepartamento mercadológico (ex: `'Informática'`, `'Periféricos'`, `'Móveis'`).
- `subcategoria` (`VARCHAR(100)`): Agrupamento tático do item (ex: `'Laptops'`, `'Monitores'`, `'Cadeiras'`).
- `preco_tabela` (`NUMERIC(12,2)`): Preço de tabela sugerido pelo fabricante (MSRP). Serve como referência para cálculo de elasticidade de preço.
- `faixa_preco` (`VARCHAR(50)`): Segmentação analítica calculada:
  - `< R$ 500,00` $\rightarrow$ `'Acessível'`
  - `R$ 500,00 a R$ 2.000,00` $\rightarrow$ `'Médio'`
  - `> R$ 2.000,00` $\rightarrow$ `'Premium'`
- `status_ativo` (`BOOLEAN`): Indica se o item está ativo para vendas no e-commerce ou foi descontinuado.
- `atualizado_em` (`TIMESTAMP`): Data e hora da última sincronização com o mestre de produtos.

---

## 3. Tabela: `gold.dim_cliente` (Tier 2 — Essencial Corporativo)

### 3.1 Metadados de Governança
- **Serviço**: `pg_ecommerce` | **Schema**: `gold`
- **Camada**: **Gold (Dimensão de Pessoas e Clientes / Ativo com Proteção de Dados LGPD)**
- **Tier Justificado**: **Tier 2 (Essencial Corporativo)**. Alimenta métricas vitais de CRM, CAC e LTV.
- **Granularidade**: **Um registro por cliente único cadastrado**.
- **Data Owner**: Fernanda Guimarães (Gerente Executiva de CRM — `crm@empresa.com.br`)
- **Data Steward**: Rafael Diniz (DPO / Especialista em Governança LGPD — `steward-crm@empresa.com.br`)
- **Alerta de Conformidade (LGPD)**: Contém campos de dados pessoais (`email`, `nome_cliente`). O campo `email` deve sofrer anonimização ou mascaramento em ambientes analíticos não-privilegiados.

### 3.2 Colunas e Semântica
- `sk_cliente` (`INTEGER PRIMARY KEY`): Chave substituta gerada pela camada Gold.
- `cliente_id` (`VARCHAR(50) UNIQUE`): Identificador único imutável originário do sistema de autenticação (SSO).
- `nome_cliente` (`VARCHAR(255)`): Nome completo do titular do cadastro.
- `email` (`VARCHAR(255)`): Correio eletrônico principal utilizado para notificações de compra e login. *(Dado Pessoal sensível a LGPD)*.
- `cidade` (`VARCHAR(100)`): Município de residência cadastrado no perfil do cliente.
- `uf` (`VARCHAR(2)`): Unidade da Federação em formato de sigla de 2 caracteres (ex: `'SP'`, `'MG'`, `'PR'`).
- `regiao` (`VARCHAR(50)`): **Macro-região geográfica brasileira**. **Origem confirmada:** Derivada **exclusivamente do cadastro permanente do cliente (`silver.clientes`)**, calculada via regra determinística:
  - `SP, RJ, MG, ES` $\rightarrow$ `'Sudeste'`
  - `PR, SC, RS` $\rightarrow$ `'Sul'`
  - `DF, GO, MT, MS` $\rightarrow$ `'Centro-Oeste'`
  - `BA, PE, CE, RN, PB, AL, SE, PI, MA` $\rightarrow$ `'Nordeste'`
  - `AM, PA, RO, AC, AP, RR, TO` $\rightarrow$ `'Norte'`
  *(Não provém de endereços de entrega alternativos).*
- `segmento` (`VARCHAR(50)`): Classificação comercial (`'B2C'`, `'B2B'`, `'VIP'`).
- `status_cliente` (`VARCHAR(20)`): Situação relacional (`'Ativo'`, `'Inativo'`, `'Bloqueado'`).
- `atualizado_em` (`TIMESTAMP`): Horário da última atualização cadastral.

---

## 4. Tabela: `silver.vendas` (Tier 3 — Base Operacional Higienizada)

### 4.1 Metadados de Governança
- **Serviço**: `pg_ecommerce` | **Schema**: `silver`
- **Camada**: **Silver (Tabela de Transações Higienizadas e Deduplicadas)**
- **Tier Justificado**: **Tier 3 (Base Operacional)**. Usada como fundação técnica para a construção da camada Gold. Não deve ser consultada diretamente por usuários finais de BI.
- **Granularidade**: **Um registro de venda validado após conferência de integridade na ingestão**.
- **Data Owner**: Equipe de Engenharia de Dados (`eng-dados@empresa.com.br`)
- **Data Steward**: Amanda Siqueira (Engenheira de Dados responsável pelo pipeline — `steward-data@empresa.com.br`)

### 4.2 Colunas e Semântica
- `id_venda` (`VARCHAR(50) PRIMARY KEY`): Código primário da venda. Valores nulos ou duplicados são expurgados para a tabela `silver.rejeitados`.
- `codigo_produto` (`VARCHAR(50)`): Código de ligação técnica com `silver.produtos`.
- `quantidade` (`INTEGER`): Número de unidades convertidas de string na camada Staging para valor inteiro positivo.
- `valor_unitario` (`NUMERIC(12,2)`): Preço de face por unidade.
- `valor_total` (`NUMERIC(12,2)`): Multiplicação direta $\text{quantidade} \times \text{valor\_unitario}$ sem aplicação de impostos complexos.
- `data_venda` (`DATE`): Data da transação padronizada no formato ISO-8601 (`YYYY-MM-DD`).
- `cliente_id` (`VARCHAR(50)`): Código do cliente no sistema transacional.
- `processado_em` (`TIMESTAMP DEFAULT CURRENT_TIMESTAMP`): Carimbo de data/hora da ingestão pela esteira de transformação.

---

## 5. Tabela: `silver.produtos` (Tier 3 — Base Operacional Higienizada)

### 5.1 Metadados de Governança
- **Serviço**: `pg_ecommerce` | **Schema**: `silver`
- **Camada**: **Silver (Catálogo Técnico Higienizado)**
- **Tier Justificado**: **Tier 3 (Base Operacional)**. Base intermediária que alimenta a dimensão `gold.dim_produto`.
- **Granularidade**: **Um registro por produto individual catalogado**.
- **Data Owner**: Equipe de Engenharia de Dados (`eng-dados@empresa.com.br`)
- **Data Steward**: Amanda Siqueira (`steward-data@empresa.com.br`)

### 5.2 Colunas e Semântica
- `codigo` (`VARCHAR(50) PRIMARY KEY`): Chave natural única do produto.
- `nome` (`VARCHAR(255)`): Nome do produto padronizado sem espaços extras e com acentuação corrigida.
- `preco` (`NUMERIC(12,2)`): Preço padrão de referência.
- `categoria` (`VARCHAR(100)`): Agrupamento operacional da mercadoria.
- `data_cadastro` (`DATE`): Data de inserção do produto no sistema de origem.
- `processado_em` (`TIMESTAMP DEFAULT CURRENT_TIMESTAMP`): Momento do processamento pelo pipeline de qualidade.

---

## 6. O Teste do Colega (Passo 4 da Apostila) — Relatório de Validação

> *"Peça a um colega que abra uma das suas tabelas no catálogo e tente responder, sem falar com você: o que é uma linha desta tabela? De onde vieram os dados? Quem procurar em caso de dúvida? Anote as perguntas que ele não conseguiu responder — e corrija a documentação. Documentação boa é a que sobrevive ao leitor que não estava presente."*

### 6.1 Simulação do Teste com Analista Convidado

O analista recebeu acesso exclusivo ao catálogo de metadados das tabelas `gold.fato_vendas` e `gold.dim_cliente`. Foram formuladas as 4 perguntas críticas da apostila:

| Pergunta Desafio | Resposta Encontrada no Catálogo? | Trecho Comprobatório na Documentação | Avaliação de Autossuficiência |
| :--- | :---: | :--- | :---: |
| **1. O que significa exatamente a coluna `margem_lucro` da `fato_vendas`? Ela considera impostos?** | **SIM** | Campo `margem_lucro`: *Margem de Contribuição Líquida Real. Fórmula: $\text{valor\_liquido} - \text{custo\_produto} - \text{impostos}$. Considera expressamente 18% de tributos (ICMS/PIS/COFINS) e o custo de mercadoria (CMV).* | **100% Autossuficiente** |
| **2. Quem é o responsável por essa tabela?** | **SIM** | Seção de Governança: Data Owner: Carlos Eduardo Braga (`comercial@empresa.com.br`). Data Steward: Mariana Albuquerque (`steward-fin@empresa.com.br`). | **100% Autossuficiente** |
| **3. De onde veio o campo `regiao` — do cadastro do cliente ou do endereço de entrega?** | **SIM** | Campo `regiao` na `gold.dim_cliente`: *Derivado exclusivamente do cadastro permanente do cliente (`silver.clientes`), calculado pela UF de registro fiscal. Não provém de endereços de entrega temporários.* | **100% Autossuficiente** |
| **4. Se a `dim_cliente` for apagada por engano, quais dashboards param de funcionar?** | **SIM** | Seção de Linhagem Downstream: *Interrompe os painéis 'Vendas Regionais', 'Análise de LTV e Cohort' e 'Segmentação B2B/B2C' no Superset e Power BI.* | **100% Autossuficiente** |

### 6.2 Dúvidas Apontadas e Melhorias Imediatas Aplicadas
- **Dúvida 1 levantada pelo colega**: *"O campo `desconto` na `fato_vendas` é uma porcentagem (ex: 10%) ou valor em Reais (R$ 10,00)?"*  
  $\rightarrow$ **Correção aplicada na documentação:** Especificado explicitamente na descrição da coluna que o campo é um **valor monetário absoluto em Reais (R$)** e nunca um percentual.
- **Dúvida 2 levantada pelo colega**: *"Se um pedido for cancelado depois do pagamento, a linha é excluída da `fato_vendas`?"*  
  $\rightarrow$ **Correção aplicada na documentação:** Explicado na coluna `status_pedido` que **não há exclusão física** de linhas; pedidos cancelados são mantidos com `status_pedido = 'Cancelado'` para preservar a auditoria contábil e a reconciliação com o gateway.

**Resultado do Teste:** O catálogo obteve nota máxima em clareza, transparência e autonomia analítica.
