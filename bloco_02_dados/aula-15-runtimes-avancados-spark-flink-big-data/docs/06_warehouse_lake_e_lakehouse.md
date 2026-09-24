# 06 — Onde os Dados Vivem: Data Warehouse, Data Lake e Data Lakehouse

> *"A história da arquitetura de dados é a busca pelo equilíbrio ideal entre controle rígido de governança e custo acessível para escala massiva."*

---

## 🏛️ 1. As Três Gerações de Armazenamento

```
      ERA 1: DATA WAREHOUSE                  ERA 2: DATA LAKE                    ERA 3: DATA LAKEHOUSE
      (Anos 1990 - 2010)                     (Anos 2010 - 2018)                  (2018 - Presente)
   
    ┌──────────────────────┐               ┌──────────────────────┐            ┌───────────────────────────┐
    │    DATA WAREHOUSE    │               │      DATA LAKE       │            │      DATA LAKEHOUSE       │
    │  - Schema-on-write   │               │  - Schema-on-read    │            │  - Schema Enforcement     │
    │  - SQL Estrito       │               │  - Qualquer arquivo  │            │  - Transações ACID        │
    │  - Armazém e CPU     │               │  - Custo baixíssimo  │            │  - Time Travel & Audit    │
    │    acoplados         │               │  - Risco: Data Swamp │            │  - Formatos Abertos:      │
    │  - Padrão: ETL       │               │  - Padrão: ELT       │            │    Delta, Iceberg, Hudi   │
    └──────────────────────┘               └──────────────────────┘            └───────────────────────────┘
```

---

## 🔍 2. Comparativo Aprofundado

| Critério | Data Warehouse (DW) | Data Lake | Data Lakehouse |
| :--- | :--- | :--- | :--- |
| **Formato de Armazenamento** | Proprietário do banco (ex: Redshift, Snowflake, Postgres) | Arquivos brutos (CSV, JSON, imagens, Parquet solto) | **Apache Parquet padronizado** com camada de log transacional |
| **Paradigma Schema** | **Schema-on-Write**: Os dados só entram se atenderem à tabela rigorosamente | **Schema-on-Read**: Salva o arquivo como estiver; quem lê que descubra o formato | **Schema Enforcement & Evolution**: Valida na escrita com capacidade de evolução |
| **Transações ACID** | Nativas e maduras | Inexistentes (se a escrita falhar no meio, deixa lixo) | **Completas (ACID)** via log transacional JSON |
| **Custo de Armazenamento** | Alto (discos SSD provisionados no banco) | Baixíssimo (Object Storage: AWS S3, Google Cloud Storage, MinIO) | Baixíssimo (mesmo Object Storage do lake) |
| **Especialidade** | Relatórios de BI, painéis gerenciais e consultas SQL rápidas | Armazenamento de dados brutos e Machine Learning exploratório | **Unificado**: BI de alto desempenho + Machine Learning + Streaming |
| **Arquitetura de Pipeline** | **ETL** (Transforma antes de carregar no DW) | **ELT** (Carrega bruto e transforma dentro do Lake) | **ELT / Medallion** (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) |

---

## ⚠️ 3. O Dilema do Data Swamp (Pântano de Dados)

Durante a febre dos Data Lakes baseados em Hadoop e S3, milhares de empresas cometeram o mesmo erro:
- Despejavam petabytes de arquivos CSV e JSON em baldes S3 sem catalogações, esquemas ou regras de limpeza;
- Dois anos depois, **ninguém sabia o que havia dentro dos arquivos**, se eram confiáveis, ou se estavam corrompidos.
- O Data Lake degenerava em um **Data Swamp** (*Pântano de Dados*), inutilizável para tomadas de decisão sérias.

---

## 💎 4. A Síntese Lakehouse: Delta Lake, Apache Iceberg e Apache Hudi

O Lakehouse resolve o problema do Data Swamp adicionando uma **camada de governança e metadados transacionais sobre o Object Storage**:

```
                         CONSULTAS SQL (BI) & JOBS DE MACHINE LEARNING
                                              ▲
                                              │
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        CAMADA DE TABELA LAKEHOUSE                                      │
│  - Catálogo de Esquemas e Validação de Tipos                                           │
│  - Log de Transações ACID (commit.json)                                                │
│  - Time Travel: SELECT * FROM vendas VERSION AS OF 3 (ou data '2026-08-01')           │
│  - Vacuum / Otimização Automática de Arquivos Pequenos                                │
└─────────────────────────────────────────────┬──────────────────────────────────────────┘
                                              │
┌─────────────────────────────────────────────▼──────────────────────────────────────────┐
│                   ARMAZENAMENTO FÍSICO: ARQUIVOS APACHE PARQUET                         │
│  dados/ano_mes=2026-08/part-0001.snappy.parquet                                        │
│  dados/ano_mes=2026-08/part-0002.snappy.parquet                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### O Que os Formatos de Tabela Trazem?
1. **Transações ACID**: Operações atômicas. Se uma carga de 1 milhão de linhas falhar na linha 999.999, nada é publicado; nenhuma consulta vê dados pela metade.
2. **Time Travel (Viagem no Tempo)**: Como o log registra cada commit, você pode consultar o estado exato da tabela no dia 1º do mês passado para fins de auditoria financeira ou treinamento de IA.
3. **Por que Parquet é Conteúdo Obrigatório?**
   Todos os três grandes padrões de Lakehouse do mercado mundial — **Delta Lake** (Databricks/Linux Foundation), **Apache Iceberg** (Netflix/Apache) e **Apache Hudi** (Uber/Apache) — **usam Parquet como seu formato de dados subjacente imutável**. Dominar Parquet é dominar o alicerce da engenharia de dados moderna.
