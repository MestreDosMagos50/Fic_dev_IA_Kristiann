# 03 — Papéis de Governança: Owner, Steward, Engineer e Consumer
## Módulo 3: Governança de Dados com OpenMetadata — Aula 01

---

## 1. O Princípio Fundamental: *"Dado sem Dono é Dado sem Manutenção"*

Em organizações com pouca maturidade de dados, datasets são frequentemente criados para projetos pontuais e depois abandonados. Quando surge uma dúvida ou uma quebra em produção, ninguém sabe quem tem autoridade para aprovar correções ou responder pelas consequências.

No OpenMetadata, **atribuir um dono (Owner) a cada tabela é a primeiríssima medida de governança**.

---

## 2. Os Quatro Papéis na Prática

| Papel | Responsabilidade Principal | Quem é no Mundo Real | Atuação no OpenMetadata |
| :--- | :--- | :--- | :--- |
| 👔 **Data Owner** *(Proprietário dos Dados)* | Responde pelo dado perante o negócio: aprova solicitações de acesso, define regras de retenção, estabelece o nível de confidencialidade e classifica o Tier. | Gestor ou Diretor da área de negócio (ex: Gerente Comercial para vendas, Diretor de RH para pessoas, CFO para finanças). | Atribuído no campo **Owner** da entidade. É notificado quando há solicitações de acesso ou alterações críticas de schema. |
| 🛡️ **Data Steward** *(Curador dos Dados)* | Cuida da qualidade, integridade, documentação e padronização no dia a dia. Conecta a linguagem técnica à semântica de negócios. | Analista de Dados Sênior, Engenheiro de Analytics ou Especialista de Governança da área. | Preenche descrições ricas, cria termos de glossário, valida o Teste do Colega e define regras de qualidade e testes. |
| ⚙️ **Data Engineer** *(Engenheiro de Dados)* | Constrói, orquestra, otimiza e monitora a infraestrutura e os pipelines de extração, transformação e carga (ETL/ELT). | Você, no Módulo 2 do curso (construindo fluxos no Apache Hop, Python e PostgreSQL). | Configura Database Services, agenda workflows de ingestão e garante a integridade dos schemas técnicos e conectores. |
| 📊 **Data Consumer** *(Consumidor dos Dados)* | Utiliza os dados catalogados para gerar insights analíticos, treinar modelos de machine learning e alimentar decisões estratégicas. | Analistas de BI, Cientistas de Dados, Executivos e Gerentes de Operações. | Utiliza a busca semântica para descobrir tabelas, lê o dicionário para entender métricas e abre chamados de governança. |

---

## 3. Matriz RACI da Governança de Dados

A matriz RACI estabelece com clareza quem é **R**esponsável pela execução (*Responsible*), quem **A**prova (*Accountable*), quem é **C**onsultado (*Consulted*) e quem é apenas **I**nformado (*Informed*):

| Atividade de Governança | Data Owner | Data Steward | Data Engineer | Data Consumer |
| :--- | :---: | :---: | :---: | :---: |
| **Definição da regra de negócio (ex: fórmula de margem)** | **A** | **R** | C | I |
| **Aprovação de acesso a dados sensíveis (PII / Financeiro)** | **A** | C | I | R (solicitante) |
| **Documentação de colunas e dicionário no catálogo** | C | **R** / **A** | C | I |
| **Construção e manutenção das tabelas no PostgreSQL** | I | C | **R** / **A** | I |
| **Classificação de criticidade (Tier 1 a Tier 5)** | **A** | **R** | C | I |
| **Criação de novos dashboards a partir da camada Gold** | I | C | I | **R** / **A** |

---

## 4. Contexto do Nosso Mini-Lab

Nos laboratórios de aprendizado e em equipes enxutas de engenharia, é comum que uma mesma pessoa acumule temporariamente mais de um papel:
- **Você como Data Engineer:** Cria os scripts DDL, sobe o contêiner do OpenMetadata e configura o usuário de menor privilégio.
- **Você como Data Steward & Owner:** Atribui os Tiers às cinco tabelas do e-commerce, documenta as regras de margem de lucro na `gold.fato_vendas` e submete o catálogo à prova no **Teste do Colega**.

Entretanto, modelar esses papéis desde o primeiro dia no OpenMetadata garante que, à medida que a organização escala, a governança permaneça distribuída e sustentável.
