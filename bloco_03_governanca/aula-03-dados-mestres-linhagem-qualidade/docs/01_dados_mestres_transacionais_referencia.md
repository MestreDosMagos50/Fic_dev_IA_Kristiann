# 🏛️ Guia Teórico: Dados Mestres, Transacionais e de Referência

Na governança de dados corporativa, um dos maiores erros de modelagem e arquitetura é tratar todos os dados como se tivessem a mesma natureza, volatilidade e propósito. O framework internacional **DAMA-DMBOK** categoriza os dados corporativos em três grandes grupos:

---

## 1. Dados Mestres (*Master Data*)

### O que são?
Os **Dados Mestres** representam as entidades centrais do negócio em torno das quais as transações ocorrem. São os substantivos fundamentais da empresa:
- **Pessoas:** Clientes, Pacientes, Alunos, Funcionários, Autores, Fornecedores.
- **Lugares:** Lojas, Centros de Distribuição, Filiais, Unidades de Ensino.
- **Coisas:** Produtos, Serviços, Cursos, Veículos, Equipamentos.

### Principais Características
- **Baixo volume:** Raramente crescem aos milhões em um único dia. Uma empresa pode ter 50 mil clientes e 2 mil produtos cadastrados.
- **Baixa volatilidade:** Mudam pouco ao longo do tempo. Um cliente atualiza seu endereço a cada poucos anos; um produto tem seu preço de tabela reajustado semestralmente.
- **Multissistêmicos:** São citados e compartilhados por múltiplos sistemas da empresa (ex: o mesmo cliente é cadastrado no e-commerce, faturado no ERP e consultado no CRM).
- **Alto impacto:** Um erro no cadastro de um produto impacta o estoque, o catálogo online, o faturamento fiscal e a precificação.

---

## 2. Dados Transacionais (*Transactional Data*)

### O que são?
Os **Dados Transacionais** representam os eventos, ocorrências e movimentos que acontecem na operação do negócio. São os **verbos** da organização:
- *Vender* $\rightarrow$ Pedidos de compra, faturamento.
- *Pagar* $\rightarrow$ Lançamentos contábeis, transações de cartão.
- *Navegar* $\rightarrow$ Cliques, acessos ao site, logs de login.
- *Publicar* $\rightarrow$ Lançamento de novos episódios de podcast, vídeos ou artigos.

### Principais Características
- **Alto volume e crescimento infinito:** Crescem segundo a segundo, gerando milhões ou bilhões de registros continuamente.
- **Natureza imutável (Append-Only):** Em sistemas modernos de dados, transações não sofrem updates; são registradas como fatos históricos que ocorreram em um dado instante no tempo (*timestamp*).
- **Dependência dos dados mestres:** Toda transação relaciona dois ou mais dados mestres (ex: *Cliente X* comprou *Produto Y* na *Loja Z* com *Pagamento W*).

---

## 3. Dados de Referência (*Reference Data*)

### O que são?
Os **Dados de Referência** são conjuntos padronizados de códigos, categorias e taxonomias usados estritamente para **classificar ou categorizar outros dados**.

### Exemplos
- Unidades Federativas (UFs): `SP`, `RJ`, `MG`, `BA`...
- Moedas: `BRL`, `USD`, `EUR`...
- Níveis de Dificuldade: `Básico`, `Intermediário`, `Avançado`.
- Categorias de Produto: `Informática`, `Móveis`, `Livros`.
- Áreas do Conhecimento: `Engenharia de Dados`, `Inteligência Artificial`, `DevOps`.

### Principais Características
- **Volume baixíssimo:** Quase sempre cabem em tabelas com menos de 100 linhas.
- **Quase estáticos:** Raramente mudam. A inclusão de uma nova UF ou categoria é um evento excepcional deliberado por comitês de negócio.
- **Domínio fechado (*Closed Domain*):** Ideais para regras de validação por listas aceitas (`IN SET`).

---

## 🎯 Quadro Comparativo Rápido

| Aspecto | Dado Mestre | Dado Transacional | Dado de Referência |
| :--- | :--- | :--- | :--- |
| **Papel Gramatical** | Substantivo (*Quem, O quê*) | Verbo (*Ação, Evento*) | Adjetivo / Código (*Classificação*) |
| **Volume Típico** | Centenas a milhares | Milhões a bilhões | Dezenas a centenas |
| **Frequência de Mudança** | Baixa (meses / anos) | Altíssima (tempo real) | Raríssima (anual) |
| **Ciclo de Vida** | CRUD (criação, edição) | Insert Only (imutável) | Somente Leitura |
| **Exemplo no Projeto** | `gold.dim_produto`, `gold.dim_conteudo` | `gold.fato_vendas`, `gold.fato_publicacoes` | `gold.dim_categoria`, UFs |
