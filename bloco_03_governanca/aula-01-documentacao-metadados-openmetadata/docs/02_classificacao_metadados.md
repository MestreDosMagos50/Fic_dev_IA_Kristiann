# 02 — Classificação de Metadados: Técnico, Negócio e Operacional
## Módulo 3: Governança de Dados com OpenMetadata — Aula 01

---

## 1. Dados vs. Metadados: O Exemplo Canônico

> **Dado é:** `4599.90`  
> Isoladamente, este número é apenas um valor flutuante na memória.

> **Metadado é:** Tudo aquilo que torna o número compreensível, acionável e confiável:
> - Que ele está armazenado na coluna `preco` da tabela `silver.produtos`;
> - Que o tipo de dado físico no PostgreSQL é `NUMERIC(12,2)`;
> - Que representa o **preço de venda de tabela em Reais (BRL), sem impostos e sem frete**;
> - Que foi atualizado hoje às **03h12** pela esteira de orquestração `padroniza_produtos.hpl`;
> - Que o responsável pelo valor perante o negócio é a **Gerência Comercial**.

Metadado é frequentemente definido de forma simplista como *"dados sobre dados"*. Em governança corporativa, metadados são **o contexto que transforma símbolos brutos em conhecimento organizacional acionável**.

---

## 2. A Tríade de Metadados

O OpenMetadata coleta e gerencia três categorias complementares de metadados:

```
                  ┌──────────────────────────────┐
                  │    CATÁLOGO DE METADADOS     │
                  └──────────────┬───────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   1. TÉCNICO     │    │  2. DE NEGÓCIO   │    │  3. OPERACIONAL  │
│  (Físico/Storage)│    │(Semântica/Regras)│    │ (Ciclo de Vida)  │
│                  │    │                  │    │                  │
│ Coleta Automática│    │ Curadoria Humana │    │ Logs de Execução │
│   via Ingestão   │    │  (Owner/Steward) │    │   e Auditoria    │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

### 2.1 Metadados Técnicos
Descrevem a **estrutura física e de armazenamento** dos dados nos sistemas gerenciadores de banco de dados (SGBDs), arquivos e streams:
- **Exemplos:** Nome do serviço, schema, tabela, coluna, tipo de dado físico (`VARCHAR`, `INTEGER`, `NUMERIC`), restrições (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `CHECK`), índices, particionamento e tamanho em bytes.
- **Forma de Coleta:** **100% Automática**. O workflow de ingestão do OpenMetadata conecta-se ao PostgreSQL, consulta o `information_schema` e extrai toda a topologia técnica sem digitação humana.

### 2.2 Metadados de Negócio
Descrevem o **significado corporativo, as regras de cálculo e as políticas de uso** dos dados:
- **Exemplos:** Definição do que é um "cliente ativo", fórmula de margem de contribuição líquida, justificativa do Tier de criticidade (Tier 1 a Tier 5), Data Owner e Data Steward atribuídos, termos de glossário e tags de privacidade (ex: `PII.Sensitive`).
- **Forma de Coleta:** **Curadoria Humana Essencial**. Nenhum algoritmo consegue adivinhar a intenção estratégica de um campo de margem ou quem responde legalmente por ele. É aqui que o engenheiro e o steward agregam valor ao catálogo.

### 2.3 Metadados Operacionais
Descrevem o **ciclo de vida, a saúde da esteira de dados e o padrão de utilização**:
- **Exemplos:** Timestamp da última carga bem-sucedida, duração de execução do pipeline, número de linhas inseridas/atualizadas, taxa de rejeição na quarentena, logs de execução, frequência de consultas e identidade dos usuários que acessaram a tabela nos últimos 30 dias.
- **Forma de Coleta:** **Automática via Logs e Orquestradores**. Extraídos a partir de conectores com o Apache Hop, Apache Airflow, dbt e pg_stat_activity do PostgreSQL.

---

## 3. Matriz Comparativa no Acervo da Aula 01

| Atributo | Metadado Técnico | Metadado de Negócio | Metadado Operacional |
| :--- | :--- | :--- | :--- |
| **Exemplo na `fato_vendas`** | Coluna `margem_lucro NUMERIC(12,2) NOT NULL` | Margem líquida descontando 18% de impostos e CMV; Tier 1 (Crítico) | Última carga hoje às 03:15 UTC; 5 linhas processadas em 1.2s |
| **Exemplo na `dim_cliente`** | Coluna `email VARCHAR(255) NOT NULL` | Dado pessoal regulado pela LGPD; Tag PII atribuída | Acessada 42 vezes nesta semana pelo dashboard de CRM |
| **Quem Mantém?** | SGBD / Engine de Ingestão | Data Owner e Data Steward | Monitoramento de Pipeline / Airflow |
| **Impacto se Ausente** | Incompatibilidade de tipos e falha de compilação | Uso errôneo de números em decisões da diretoria | Pipelines zumbis rodando sem ninguém saber a saúde |
