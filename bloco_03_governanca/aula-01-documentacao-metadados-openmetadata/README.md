# 📘 Módulo 3: Governança de Dados com OpenMetadata
## 📄 Aula 01 — Conceitos de Documentação, Metadados e Governança de Dados

Bem-vindo ao repositório oficial da **Aula 01 do Módulo 3** do curso FIC Engenharia de Dados.

Nesta aula, superamos a barreira do código SQL isolado para transformar o pipeline do e-commerce em um **acervo de dados formalmente governado, catalogado e auditável**, utilizando a plataforma líder de mercado **OpenMetadata**.

---

## 🚀 Estrutura do Projeto

```text
bloco_03_governanca/aula-01-documentacao-metadados-openmetadata/
├── docker/
│   └── docker-compose.yml           # Arquivo oficial do OpenMetadata v1.6.0 (Servidor, Busca, Ingestão, BD)
├── sql/
│   ├── 00_prepara_banco_ecommerce.sql # DDL e carga com schemas staging, silver e gold no meu_banco_de_dados
│   └── 01_usuario_openmetadata.sql  # Criação do usuário somente-leitura (Princípio do Menor Privilégio)
├── metadados/
│   ├── dicionario_de_dados.md       # Documentação formal e completa das 5 tabelas (Passo 3 e Teste do Colega)
│   └── catalogo_metadados.json      # Backup estruturado das definições, tiers, donos e regras em JSON
├── docs/
│   ├── 01_quatro_pilares_governanca.md     # Descoberta, Entendimento, Confiança e Conformidade
│   ├── 02_classificacao_metadados.md       # Técnicos, De Negócio e Operacionais
│   ├── 03_papeis_owner_steward_consumer.md # RACI: Data Owner, Steward, Engineer e Consumer
│   ├── 04_arquitetura_openmetadata.md      # As 4 peças fundamentais da plataforma OpenMetadata
│   └── 05_guia_pratico_minilab.md          # Tutorial passo a passo do Mini-Lab (10 pontos)
├── scripts/
│   └── validar_conexao_postgres.py  # Script de diagnóstico de conectividade e menor privilégio
├── index.html                       # Dashboard interativo de Governança do Acervo
└── README.md                        # Este documento
```

---

## ⚡ Como Executar o Mini-Lab Passo a Passo

### 1. Preparar o Banco de Dados no PostgreSQL
Execute os scripts DDL e de concessão de permissões no contêiner do PostgreSQL:

```bash
# Entrar na pasta do projeto
cd bloco_03_governanca/aula-01-documentacao-metadados-openmetadata

# Criar os schemas e popular as tabelas das camadas staging, silver e gold
docker exec -i meu_postgres psql -U vinycius -d meu_banco_de_dados < sql/00_prepara_banco_ecommerce.sql

# Criar o usuário openmetadata_user com menor privilégio
docker exec -i meu_postgres psql -U vinycius -d meu_banco_de_dados < sql/01_usuario_openmetadata.sql
```

### 2. Validar a Conectividade via Python
Execute o script de diagnóstico automatizado para garantir que o usuário somente-leitura tem acesso a todos os schemas e que qualquer tentativa de escrita é rejeitada:

```bash
python3 scripts/validar_conexao_postgres.py
```

### 3. Iniciar o Ecossistema OpenMetadata via Docker
```bash
cd docker
docker compose up -d
```
Acesse a interface web em [http://localhost:8585](http://localhost:8585) (credenciais padrão: `admin` / `admin`).

### 4. Configurar o Serviço `pg_ecommerce` no OpenMetadata
1. Acesse **Settings > Services > Databases > Add New Service** e escolha **Postgres**.
2. Nomeie como `pg_ecommerce`.
3. Preencha os dados de conexão:
   - Host/Port: `meu_postgres:5432` ou `host.docker.internal:5433`
   - Usuário: `openmetadata_user`
   - Senha: `openmetadata_pass123`
   - Banco: `meu_banco_de_dados`
4. Crie o pipeline de **Metadata Ingestion** filtrando os schemas `staging`, `silver` e `gold`.
5. Execute o workflow e confira a extração com status **Success**.

### 5. Documentar as 5 Tabelas (Passo 3) & Aplicar o Teste do Colega (Passo 4)
Consulte os arquivos [dicionario_de_dados.md](metadados/dicionario_de_dados.md) e [05_guia_pratico_minilab.md](docs/05_guia_pratico_minilab.md) para registrar:
- `gold.fato_vendas` (Tier 1 — Crítico)
- `gold.dim_produto` (Tier 2 — Essencial)
- `gold.dim_cliente` (Tier 2 — Essencial)
- `silver.vendas` (Tier 3 — Operacional)
- `silver.produtos` (Tier 3 — Operacional)

### 6. Explorar o Dashboard Interativo
Abra o arquivo `index.html` em qualquer navegador web para interagir com o portal de governança completo, incluindo o simulador interativo do **Teste do Colega**, busca dinâmica no dicionário de dados e visualização dos 4 pilares.
