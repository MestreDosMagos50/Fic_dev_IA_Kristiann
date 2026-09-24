# 04 — Arquitetura Interna do OpenMetadata
## Módulo 3: Governança de Dados com OpenMetadata — Aula 01

---

## 1. Visão Geral da Plataforma

O **OpenMetadata** é uma plataforma *open source* de governança, catálogo, linhagem, qualidade e colaboração de dados que adota o conceito de **Metadata as a Service (MaaS)** e padrão unificado baseado em JSON Schema.

Diferente de catálogos legados que atuam apenas como repositórios estáticos de documentação, o OpenMetadata atua como um sistema ativo que monitora, ingere e sincroniza metadados continuamente.

```
                  ┌──────────────────────────────────────────────┐
                  │       INTERFACE WEB & API REST (8585)        │
                  │   Single Page Application (React) + Dropwizard│
                  └──────────────┬───────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────────────┐
         ▼                       ▼                               ▼
┌──────────────────┐    ┌──────────────────┐            ┌──────────────────┐
│   METADATA DB    │    │  SEARCH ENGINE   │            │INGESTION PIPELINE│
│(MySQL/PostgreSQL)│    │   (OpenSearch /  │            │(Airflow + Python)│
│   Porta 3306     │    │  Elasticsearch)  │            │  Conectores DB   │
│                  │    │    Porta 9200    │            │                  │
│  Entidades JSON  │    │  Busca Semântica │            │ Ingestão Técnica │
│   e Relacionamentos│  │  e Autocomplete  │            │    Agendada      │
└──────────────────┘    └──────────────────┘            └──────────────────┘
```

---

## 2. As Quatro Peças Arquiteturais Fundamentais

### 2.1 Servidor Central (OpenMetadata Server)
- **Tecnologia:** Java (Dropwizard Framework) e React SPA.
- **Porta Padrão:** `8585` (API REST e UI Web). Porta de Admin: `8586`.
- **Função:** Centraliza todas as chamadas de API, autenticação JWT, controle de acesso baseado em papéis (RBAC), disparo de webhooks e disponibiliza a interface gráfica interativa do usuário.
- **Princípio:** Nenhuma entidade entra no catálogo sem validação estrita contra a especificação JSON Schema do projeto.

### 2.2 Banco de Armazenamento de Metadados (Metadata Store)
- **Tecnologia:** MySQL 8.x ou PostgreSQL 15+.
- **Porta Padrão:** `3306` (MySQL) ou `5432` (PostgreSQL).
- **Função:** Armazenamento relacional e persistente de todas as entidades, propriedades, usuários, políticas de segurança, histórico de alterações (*versioning*) e testes de qualidade.

### 2.3 Mecanismo de Busca e Agregação (Search Engine)
- **Tecnologia:** OpenSearch 2.x ou Elasticsearch 8.x.
- **Porta Padrão:** `9200`.
- **Função:** Fornece capacidades de pesquisa instantânea (*search-as-you-type*), filtros facetados por camada, schema, tags e tiers, além de agregar métricas analíticas sobre o acervo de dados.

### 2.4 Orquestrador de Ingestão (Ingestion Framework & Airflow)
- **Tecnologia:** Python + Apache Airflow embutido (imagem `openmetadata_ingestion`).
- **Função:** Executa periodicamente os workflows de extração programados. O Airflow conecta-se remotamente aos bancos fontes (ex: PostgreSQL `pg_ecommerce`), extrai metadados técnicos (tabelas, colunas, chaves, tipos) e os envia via API REST para o OpenMetadata Server.

---

## 3. A Hierarquia Universal de Entidades

Para navegar com clareza na interface e evitar desorientação em grandes ambientes corporativos, o OpenMetadata organiza os ativos na seguinte hierarquia em árvore:

```text
Database Service (ex: pg_ecommerce)
└── Database (ex: meu_banco_de_dados)
    ├── Schema: staging (ibge_municipios, datasus_dengue, etc.)
    ├── Schema: silver  (produtos, vendas, clientes, rejeitados)
    └── Schema: gold    (fato_vendas, dim_produto, dim_cliente)
        └── Table: fato_vendas
            ├── Column: sk_venda
            ├── Column: id_venda
            ├── Column: valor_liquido
            └── Column: margem_lucro
```

> **Regra de Ouro da Governança:**  
> A documentação e os metadados podem ser atribuídos em **qualquer nível** dessa árvore (no nível de serviço, no nível de schema, no nível de tabela e no nível de coluna individual). É essa riqueza contextual que transforma uma simples lista de tabelas em verdadeiro patrimônio de conhecimento corporativo.

---

## 4. O Princípio do Menor Privilégio na Conexão com o PostgreSQL

Por que nunca devemos cadastrar o usuário administrador `postgres` no catálogo?

1. **Apenas Leitura Estrita:** O OpenMetadata extrai apenas a estrutura (*Data Dictionary*) e estatísticas de volume (`COUNT(*)`). Ele **nunca precisa escrever, alterar ou deletar** dados do negócio.
2. **Isolamento de Risco:** Caso credenciais do conector sejam comprometidas ou expostas indevidamente, o invasor não terá capacidade de executar comandos destrutivos (`DROP`, `TRUNCATE`, `UPDATE`).
3. **Auditabilidade de Compliance:** Criar o usuário `openmetadata_user` com `GRANT USAGE` e `GRANT SELECT` demonstra maturidade em auditorias de segurança ISO-27001 e conformidade com a LGPD.
