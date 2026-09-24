# 05 — Guia Prático do Mini-Lab: Documentando o Acervo do E-commerce
## Módulo 3: Governança de Dados com OpenMetadata — Aula 01

Este guia orienta a execução prática do **Mini-Lab da Aula 01**, cobrindo desde a subida dos contêineres até a realização do Teste do Colega e a validação dos critérios de avaliação (10 pontos).

---

## 📋 Critérios de Avaliação (10 Pontos)

| Critério Oficial da Apostila | Pontuação | Verificação |
| :--- | :---: | :--- |
| **Passo 1 & 2:** OpenMetadata no ar com ingestão executada com sucesso | **3 pontos** | Serviços ativos em Docker, conector `pg_ecommerce` cadastrado e pipeline executado com status *Success*. |
| **Passo 3:** Cinco tabelas documentadas com descrição, owner e tier | **3 pontos** | Tabelas `silver.produtos`, `silver.vendas`, `gold.fato_vendas`, `gold.dim_produto` e `gold.dim_cliente` catalogadas com metadados ricos. |
| **Passo 3:** Colunas de `gold.fato_vendas` descritas com significado real | **2 pontos** | Nenhuma descrição redundante (ex: "valor total = valor total"). Todas as 16 colunas com regras de cálculo detalhadas. |
| **Passo 4:** Teste do Colega realizado, com correções aplicadas e registradas | **2 pontos** | Validação das 4 perguntas-chave sem intervenção do autor, com relatório de dúvidas resolvidas. |

---

## Passo 1 — Subir o Ambiente OpenMetadata via Docker

No terminal, navegue até a pasta `docker/` do projeto:

```bash
cd /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-01-documentacao-metadados-openmetadata/docker

# Subir todos os serviços em background
docker compose up -d

# Acompanhar a subida do servidor principal
docker compose logs -f openmetadata_server
```

> **Aviso de Recursos (Página 4 da Apostila):**  
> O OpenMetadata requer aproximadamente **6 GB de RAM** alocados para o Docker. O primeiro start pode levar de 3 a 5 minutos enquanto o Elasticsearch e as migrações do banco de metadados são inicializados.

### Acesso à Interface Web
Após a inicialização completa, abra o navegador e acesse:
- **URL:** [http://localhost:8585](http://localhost:8585)
- **Usuário Padrão:** `admin`
- **Senha Padrão:** `admin`

---

## Passo 2 — Configuração do Database Service `pg_ecommerce`

1. No menu lateral esquerdo do OpenMetadata, navegue até:  
   **Settings (⚙️) > Services > Databases > Add New Service**.
2. Selecione o conector **Postgres** e clique em **Next**.
3. Defina o nome do serviço estritamente como:  
   `pg_ecommerce`
4. Preencha os parâmetros de conexão utilizando o usuário de menor privilégio criado no PostgreSQL:
   - **Host and Port:** `meu_postgres:5432` *(se na mesma rede docker)* ou `host.docker.internal:5433`
   - **Username:** `openmetadata_user`
   - **Password:** `openmetadata_pass123`
   - **Database Name:** `meu_banco_de_dados`
5. Clique em **Test Connection** para validar o acesso do catálogo ao banco.
6. Salve o serviço.

### Configurando o Metadata Ingestion Workflow
1. Dentro do serviço `pg_ecommerce`, clique na aba **Ingestions** e depois em **Add Ingestion > Add Metadata Ingestion**.
2. No filtro de schemas (**Schema Filter Pattern**), inclua explicitamente:
   - **Include Schemas:** `staging`, `silver`, `gold`
3. Defina o agendamento (*Schedule*) ou mantenha em execução manual (*Ad hoc*).
4. Clique em **Deploy** e, em seguida, em **Run**.
5. Acompanhe a execução até o status exibir **Success**.

Ao término, todas as tabelas das camadas Staging, Silver e Gold estarão visíveis na árvore de exploração com todas as suas colunas e tipos técnicos!

---

## Passo 3 — Documentação Formal das Cinco Tabelas Estratégicas

Abra cada uma das 5 tabelas no catálogo e preencha os elementos obrigatórios:

### 1. `gold.fato_vendas`
- **Description:**  
  *"Tabela fato central contendo o histórico transacional atômico de vendas do e-commerce. Granularidade: Uma linha representa exatamente um item de produto vendido em um pedido comercial. Alimenta relatórios financeiros executivos e o cálculo de margem e comissões."*
- **Owner:** Atribua a `Carlos Eduardo Braga` (Diretoria Comercial).
- **Tier:** Atribua **Tier 1 (Crítico de Negócio)**.
- **Description por coluna:** Documente todas as 16 colunas conforme o [dicionario_de_dados.md](../metadados/dicionario_de_dados.md). Destaque fundamental para a coluna `margem_lucro`:  
  *"Margem de Contribuição Líquida Real calculada pela fórmula: valor_liquido - custo_produto - impostos. Considera expressamente 18% de tributos (ICMS/PIS/COFINS) e o custo de reposição CMV."*

### 2. `gold.dim_produto`
- **Description:**  
  *"Dimensão conforme de produtos catalogados. Granularidade: Uma linha por SKU comercializável. Utilizada para agrupamento mercadológico por categoria e faixa de preço."*
- **Owner:** Atribua a `Roberta Silveira` (Gestão de Produtos).
- **Tier:** Atribua **Tier 2 (Essencial Corporativo)**.

### 3. `gold.dim_cliente`
- **Description:**  
  *"Dimensão de clientes da base corporativa. Granularidade: Uma linha por cliente único cadastrado. Contém dados pessoais sujeitos à LGPD (como email). O campo regiao é derivado exclusivamente do endereço cadastral permanente do cliente (silver.clientes), e não do endereço de entrega."*
- **Owner:** Atribua a `Fernanda Guimarães` (CRM & Atendimento).
- **Tier:** Atribua **Tier 2 (Essencial Corporativo)**.

### 4. `silver.vendas`
- **Description:**  
  *"Tabela de vendas higienizadas e tipadas da camada Silver. Granularidade: Uma linha por venda validada e deduplicada após ingestão da camada Staging."*
- **Owner:** Atribua a `Equipe de Engenharia de Dados`.
- **Tier:** Atribua **Tier 3 (Base Operacional)**.

### 5. `silver.produtos`
- **Description:**  
  *"Catálogo operacional padronizado de produtos da camada Silver. Granularidade: Uma linha por mercadoria com formato de texto e preço sanitizados."*
- **Owner:** Atribua a `Equipe de Engenharia de Dados`.
- **Tier:** Atribua **Tier 3 (Base Operacional)**.

---

## Passo 4 — O Teste do Colega

Simule o teste com um analista ou colega de turma:
1. Compartilhe o link da tabela `gold.fato_vendas` no OpenMetadata ou envie o [dicionario_de_dados.md](../metadados/dicionario_de_dados.md).
2. Peça ao colega para responder às 4 perguntas sem consultar você:
   - *O que é uma linha desta tabela?*
   - *A coluna margem considera impostos?*
   - *Quem procurar em caso de dúvidas sobre regras de negócio?*
   - *De onde veio o campo regiao do cliente?*
3. Verifique se ele acertou 100% das respostas com base apenas no catálogo.
4. Registre o sucesso e as eventuais melhorias no relatório final.
