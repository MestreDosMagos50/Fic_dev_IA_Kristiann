# 🏷️ Passo 1 — Inventário Completo de Master Data, Dados Transacionais e Referência

Este documento formaliza o **Inventário de Dados** do catálogo corporativo, classificando cada tabela do ecossistema de dados segundo o framework **DAMA-DMBOK** e as diretrizes da Aula 03.

---

## 📊 Matriz de Classificação das Tabelas do Catálogo

| Tabela | Classificação (`TipoDado`) | Justificativa (Por que é mestre, transacional ou referência?) | Fonte de Verdade (*System of Record*) |
| :--- | :--- | :--- | :--- |
| `gold.dim_produto` | **Mestre (Master Data)** | Entidade central do portfólio de produtos; substantivo ("produto"); baixo volume e baixa volatilidade; compartilhado entre ERP, e-commerce e faturamento. | ERP Corporativo / Catálogo de Produtos |
| `gold.dim_cliente` | **Mestre (Master Data)** | Entidade central de relacionamento com compradores; substantivo ("cliente"); compartilhado entre e-commerce, CRM e atendimento ao cliente. | CRM Corporativo / Cadastro Único de Clientes |
| `gold.dim_conteudo` | **Mestre (Master Data)** | Catálogo canônico de cursos, artigos, podcasts e vídeos gerados no ecossistema educacional; entidade substantiva persistente (*Golden Record* consolidado). | Plataforma LMS / Acervo Acadêmico |
| `gold.dim_autor` | **Mestre (Master Data)** | Entidade central de instrutores, autores e especialistas geradores de conteúdo; identificação profissional única citada em múltiplos cursos e artigos. | Sistema de RH / Cadastro de Especialistas |
| `silver.produtos` | **Mestre (Master Data)** | Versão higienizada e deduplicada da entidade mestre produto na camada Silver, mantendo a chave canônica `codigo`. | Staging Produtos / ERP |
| `silver.clientes` | **Mestre (Master Data)** | Versão limpa da entidade mestre cliente na camada Silver, com tratamento de dados cadastrais e e-mails normalizados. | Staging Clientes / CRM |
| `silver.conteudos` | **Mestre (Master Data)** | Entidade mestre intermediária de conteúdos educacionais com flags de duplicatas de negócio e ponteiro para o *Golden Record*. | Staging Conteúdos / LMS |
| `staging.produtos` | **Mestre (Master Data)** | Representação bruta da entidade mestre produto na camada de ingestão inicial (Bronze). | Arquivo `produtos.csv` / ERP |
| `staging.clientes` | **Mestre (Master Data)** | Representação bruta da entidade mestre cliente na camada de ingestão inicial (Bronze). | Arquivo `clientes.csv` / CRM |
| `staging.conteudos` | **Mestre (Master Data)** | Ingestão bruta do acervo educacional com 1000 registros de cursos, podcasts, artigos e vídeos. | Arquivo `conteudos.csv` / LMS |
| `gold.fato_vendas` | **Transacional** | Registro dos eventos de compra efetuados pelos clientes; verbo ("vender/comprar"); alto volume, crescimento contínuo e dependência temporal. | Gateway de Pagamentos / Checkout E-Commerce |
| `gold.fato_publicacoes`| **Transacional** | Registro dos eventos temporais de publicação de conteúdos na plataforma, relacionando autores, categorias e carga horária. | Log de Publicações / Plataforma LMS |
| `silver.vendas` | **Transacional** | Movimentações transacionais de vendas higienizadas, tipadas e com métricas unitárias e totais calculadas. | Staging Vendas |
| `staging.vendas` | **Transacional** | Carga bruta de eventos transacionais de vendas extraídos diretamente das fontes operacionais. | Arquivo `vendas.csv` |
| `silver.rejeitados` | **Transacional** | Log operacional contínuo de registros rejeitados pelas regras de qualidade e integridade do pipeline de dados. | Motor de Ingestão Apache Hop / ETL |
| `gold.dim_categoria` | **Referência** | Lista padronizada e quase estática de domínios do conhecimento (DevOps, BI, IA, etc.) usada exclusivamente para categorizar conteúdos. | Taxonomia Oficial do Comitê de Governança |

---

## 🎯 Regras Práticas Aplicadas na Identificação

1. **O Teste Substantivo vs. Verbo:**
   - **Substantivo:** *Cliente*, *Produto*, *Conteúdo*, *Autor* $\rightarrow$ **Dados Mestres**.
   - **Verbo / Ação:** *Vender*, *Comprar*, *Publicar*, *Avaliar*, *Rejeitar* $\rightarrow$ **Dados Transacionais**.
2. **Volatilidade e Volume:**
   - **Mestre:** Baixo volume, muda pouco (uma empresa adiciona dezenas de produtos por mês, mas processa milhares de vendas por hora).
   - **Transacional:** Alto volume, acumula-se continuamente ao longo do tempo (apenas inserções, sem atualizações frequentes de estado).
   - **Referência:** Praticamente estático (categorias de produtos, UFs, moedas, níveis de complexidade).
3. **Compartilhamento Multissistêmico:**
   - O dado mestre é referenciado por mais de um sistema corporativo (o mesmo cliente existe no e-commerce, no ERP de faturamento e no CRM de suporte).
