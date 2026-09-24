# 05 — Guia Prático do Mini-Lab: Construindo o Glossário do E-commerce
## Módulo 3: Governança de Dados com OpenMetadata — Aula 02

Este guia orienta a execução dos cinco passos do Mini-Lab da Aula 02, detalhando o que fazer na interface do OpenMetadata e como validar os 10 pontos da avaliação.

---

## 📋 Critérios de Avaliação Oficial (10 Pontos)

| Critério Oficial | Pontos | Como Validamos no Projeto |
| :--- | :---: | :--- |
| **Passo 2:** Cinco termos criados com definição nas quatro partes | **4 pontos** | Termos `Ticket Médio`, `Cliente Ativo`, `Receita Líquida`, `Margem de Contribuição` e `Item de Pedido` com formulação completa. |
| **Passo 3:** Hierarquia Cliente $\rightarrow$ Cliente Ativo/Inativo com critério explícito | **2 pontos** | Termo pai `Cliente` contendo o critério de 90 dias e os filhos `Cliente Ativo` e `Cliente Inativo` subordinados. |
| **Passo 4:** Termos vinculados a tabelas/colunas do catálogo | **2 pontos** | Termos atrelados a `gold.fato_vendas` e `gold.dim_cliente`. |
| **Passo 5:** Classification Camada criada e aplicada, com busca comprovada | **2 pontos** | Classificação `Camada` com tags `Bronze`, `Silver` e `Gold` aplicada e testada no filtro de busca. |

---

## Passo a Passo na Interface do OpenMetadata

### Passo 1 — Criar o Glossário (`Glossário E-commerce`)
1. No menu lateral esquerdo, clique no ícone **Govern (🏛️) > Glossaries**.
2. Clique no botão superior direito **`+ Add Glossary`**.
3. Preencha:
   - **Name:** `Glossario_Ecommerce`
   - **Display Name:** `Glossário E-commerce`
   - **Description:** *"Glossário oficial corporativo dos conceitos de negócio de vendas, clientes e produtos."*
   - **Owner:** `admin`
   - **Reviewers:** `admin`
4. Clique em **Save**.

---

### Passo 2 & 3 — Criar os Termos e a Hierarquia Semântica
Dentro do `Glossário E-commerce`, clique em **`+ Add Term`**:

1. **Termo Pai: `Cliente`**
   - **Name:** `Cliente`
   - **Description:** *"Pessoa física ou jurídica cadastrada na plataforma. Critério de separação: A distinção entre Cliente Ativo e Inativo é estritamente temporal, baseada na janela de 90 dias da última compra faturada."*
   - Salve.

2. **Termos Filhos (Subordinados a `Cliente`):**
   - Abra o termo `Cliente` recém-criado.
   - Na aba **Terms** interna ou no botão **`+ Add Term`**, adicione:
     - **`Cliente Ativo`**: Definição nas 4 partes com justificativa dos 90 dias.
     - **`Cliente Inativo`**: Definição nas 4 partes com critérios de churn.

3. **Termos de Vendas e Margem:**
   - Volte à raiz do `Glossário E-commerce` e adicione os termos:
     - **`Ticket Médio`**: Obrigatório, com fórmula $\frac{\sum \text{valor\_liquido}}{\text{DISTINCT } \text{id\_venda}}$ e exclusão de cancelados.
     - **`Receita Líquida`**: Faturamento líquido com dedução de cupons e descontos.
     - **`Margem de Contribuição`**: Margem com dedução expressa de 18% de impostos e CMV.
     - **`Item de Pedido`**: Unidade atômica da venda.

---

### Passo 4 — Vincular Termos às Colunas dos Ativos
1. Vá em **Explore > Tables** e abra **`gold.fato_vendas`**.
2. Na lista de colunas:
   - Na coluna `valor_liquido`, clique em **`+ Add Glossary Term`** e selecione `Ticket Médio` e `Receita Líquida`.
   - Na coluna `margem_lucro`, vincule o termo `Margem de Contribuição`.
   - Na coluna `sk_venda`, vincule o termo `Item de Pedido`.
3. Abra **`gold.dim_cliente`**:
   - No topo da tabela, vincule o termo pai `Cliente`.
   - Na coluna `status_cliente`, vincule o termo `Cliente Ativo`.

---

### Passo 5 — Criar Classification `Camada` e Tags
1. No menu lateral, clique em **Settings (⚙️) > Tags > Classifications**.
2. Clique em **`+ Add Classification`**:
   - **Name:** `Camada`
   - **Mutually Exclusive:** Marque `Yes`.
3. Dentro da Classification `Camada`, adicione as três tags:
   - **`Bronze`** (Staging/Ingestão Bruta)
   - **`Silver`** (Higienizado e Tipado)
   - **`Gold`** (Star Schema / Analítico)
4. Vá em **Explore > Tables** e aplique a tag `Camada.Gold` nas tabelas `fato_vendas`, `dim_produto` e `dim_cliente`.
5. Faça o teste de busca: filtre pelo menu lateral por **Tag: `Camada.Gold`** e comprove que o catálogo isola perfeitamente as tabelas analíticas!
