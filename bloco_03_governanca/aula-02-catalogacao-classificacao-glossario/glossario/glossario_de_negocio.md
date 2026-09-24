# Glossário de Negócio do E-commerce
## Módulo 3: Governança de Dados com OpenMetadata — Aula 02

> **Objetivo Semântico:**  
> O Glossário de Negócio constrói a ponte entre a linguagem falada pelas áreas corporativas (Diretoria, Marketing, Comercial, Finanças) e as colunas físicas dos bancos de dados. Seu objetivo é **eliminar ambiguidades**, garantindo que um mesmo conceito possua uma única definição oficial compartilhada em toda a organização (*Single Source of Truth*).

---

## 🏛️ A Metodologia das Quatro Partes Obrigatórias

Conforme estipulado na **Seção 5 da Apostila**, uma definição de negócio amadora diz apenas o óbvio (ex: *"Ticket médio é a média dos pedidos"*). Uma definição profissional e auditável deve obrigatoriamente responder a quatro dimensões:

```
┌────────────────────────────────────────────────────────┐
│             AS QUATRO PARTES DA DEFINIÇÃO              │
├────────────────────────────────────────────────────────┤
│ 1. O que é:         Definição conceitual clara         │
│ 2. Como se calcula: Fórmula matemática determinística  │
│ 3. O que fica fora: Critérios de exclusão explícitos   │
│ 4. Recortes válidos:Granularidade e filtros permitidos │
└────────────────────────────────────────────────────────┘
```

> **Atenção:** A terceira parte (*o que fica de fora*) é a mais esquecida na engenharia de dados — e é exatamente ela que gera reuniões improdutivas onde três analistas apresentam três números de faturamento divergentes para o mesmo mês fiscal.

---

## 📚 Catálogo Oficial de Termos do Glossário

### 1. Termo: Ticket Médio *(Obrigatório)*

| Dimensão | Conteúdo Oficial de Negócio |
| :--- | :--- |
| **1. O que é** | Valor monetário médio despendido pelos clientes por pedido de compra concluído em um período determinado. |
| **2. Como se calcula** | $\frac{\sum \text{valor\_liquido}}{\text{COUNT(DISTINCT } \text{id\_venda)}}$ a partir dos registros faturados da tabela `gold.fato_vendas`. |
| **3. O que fica de fora** | Pedidos com `status_pedido IN ('Cancelado', 'Devolvido')` são expressamente excluídos do numerador e do denominador. Custos de frete cobrados e taxas de juros de parcelamento de cartão **não compõem o valor**. |
| **4. Recortes válidos** | Agregável por mês fiscal, categoria de produto, canal de conversão e macrorregião geográfica. |
| **Sinônimos** | *AOV (Average Order Value)*, *Valor Médio por Pedido*. |
| **Termos Relacionados**| *Receita Líquida*, *Item de Pedido*. |
| **Data Owner** | Diretoria Comercial (`comercial@empresa.com.br`) |
| **Vínculo Físico** | Coluna `valor_liquido` da tabela `gold.fato_vendas`. |

---

### 2. Hierarquia Semântica: Cliente *(Termo Pai)*

- **Definição do Termo Pai:** Pessoa física ou jurídica formalmente cadastrada na base corporativa do e-commerce.
- **Critério de Separação Explícito:**  
  > *"A distinção entre Cliente Ativo e Cliente Inativo é estritamente temporal, baseada na janela de **90 dias** transcorridos desde a data da última compra faturada (`CURRENT_DATE - MAX(data_venda)`)."*
- **Sinônimos:** *Consumidor*, *Comprador*, *Titular do Cadastro*.
- **Vínculo Físico:** Tabela inteira `gold.dim_cliente`.

```
                    ┌─────────────────────────┐
                    │    CLIENTE (Pai)        │
                    │ Regra: Janela de 90 dias│
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
      ┌─────────────────────┐         ┌─────────────────────┐
      │ CLIENTE ATIVO (≤90d)│         │CLIENTE INATIVO (>90d│
      │ Recompra Recente    │         │  Risco de Churn     │
      └─────────────────────┘         └─────────────────────┘
```

#### 2.1 Termo Filho: Cliente Ativo *(Obrigatório)*
| Dimensão | Conteúdo Oficial de Negócio |
| :--- | :--- |
| **1. O que é** | Cliente cadastrado que realizou ao menos um pedido de compra faturado e entregue dentro da janela de referência de 90 dias. |
| **2. Como se calcula** | Condição lógica: `CURRENT_DATE - MAX(data_venda) <= 90 dias` com `status_pedido = 'Entregue'`. |
| **3. Justificativa dos 90 Dias** | No segmento de bens semiduráveis, eletrônicos e periféricos, o ciclo médio de recompra varia entre 60 e 75 dias. A janela de 90 dias engloba um trimestre fiscal completo e sinaliza o cliente que ainda mantém engajamento com a marca antes do esfriamento relacional. |
| **4. O que fica de fora** | Clientes cadastrados há anos sem compras recentes; clientes com pedidos recentes integralmente estornados ou cancelados por fraude. |
| **5. Recortes válidos** | Segmentação comercial (B2C, B2B, VIP) e valor acumulado de vida útil (*LTV*). |
| **Sinônimos** | *Active Customer*, *Cliente Engajado*, *Comprador Recorrente*. |
| **Vínculo Físico** | Coluna `status_cliente` da tabela `gold.dim_cliente`. |

#### 2.2 Termo Filho: Cliente Inativo
| Dimensão | Conteúdo Oficial de Negócio |
| :--- | :--- |
| **1. O que é** | Cliente cadastrado cuja última transação concluída ocorreu há mais de 90 dias, ou que realizou o cadastro na loja virtual mas nunca finalizou uma compra. |
| **2. Como se calcula** | Condição lógica: `CURRENT_DATE - MAX(data_venda) > 90 dias` ou `MAX(data_venda) IS NULL`. |
| **3. O que fica de fora** | Clientes com contas suspensas por segurança ou que solicitaram exclusão de dados com base na LGPD (rotulados sob status específico de *Anonimizado/Bloqueado*). |
| **4. Recortes válidos** | Subdivisão em faixas de inatividade: 91 a 180 dias (*em risco*), 181 a 365 dias (*churn consolidado*) e >365 dias (*perdido*). |
| **Sinônimos** | *Dormant Customer*, *Cliente Adormecido*, *Churn*. |
| **Vínculo Físico** | Coluna `status_cliente` da tabela `gold.dim_cliente`. |

---

### 3. Termo: Receita Líquida

| Dimensão | Conteúdo Oficial de Negócio |
| :--- | :--- |
| **1. O que é** | Montante financeiro faturado efetivo decorrente da comercialização de itens, após o abatimento de descontos comerciais concedidos. |
| **2. Como se calcula** | $\sum (\text{quantidade} \times \text{preco\_unitario} - \text{desconto})$ na tabela `gold.fato_vendas`. |
| **3. O que fica de fora** | Fretes cobrados à parte, seguros de transporte, taxas de juros de parcelamento do gateway e pedidos cancelados/estornados. |
| **4. Recortes válidos** | Por período diário/mensal/anual, canal de venda (Web, App, B2B, Marketplace) e departamento. |
| **Sinônimos** | *Net Revenue*, *Net Sales*, *Faturamento Líquido*. |
| **Termos Relacionados**| *Ticket Médio*, *Margem de Contribuição*. |
| **Vínculo Físico** | Coluna `valor_liquido` da tabela `gold.fato_vendas`. |

---

### 4. Termo: Margem de Contribuição

| Dimensão | Conteúdo Oficial de Negócio |
| :--- | :--- |
| **1. O que é** | Ganho financeiro real remanescente da venda de cada mercadoria após a dedução de todos os custos variáveis diretos e impostos incidentes. |
| **2. Como se calcula** | $\text{valor\_liquido} - \text{custo\_produto} - \text{impostos}$ em `gold.fato_vendas`. |
| **3. O que fica de fora** | Custos fixos de infraestrutura (aluguel de CD, salários de TI, servidores) não entram no cálculo do item. **Deduz expressamente 18% de tributos diretos (ICMS + PIS/COFINS)** e o custo de reposição CMV histórico. |
| **4. Recortes válidos** | Por categoria de produto, fabricante/fornecedor, canal de venda e faixa de preço. |
| **Sinônimos** | *Margem Líquida do Item*, *Contribution Margin*, *Margem Real*. |
| **Termos Relacionados**| *Receita Líquida*, *Item de Pedido*. |
| **Vínculo Físico** | Coluna `margem_lucro` da tabela `gold.fato_vendas`. |

---

### 5. Termo: Item de Pedido

| Dimensão | Conteúdo Oficial de Negócio |
| :--- | :--- |
| **1. O que é** | Unidade atômica transacionada que representa a aquisição de um SKU de produto dentro de um pedido de compra. |
| **2. Como se calcula** | Cada linha individual registrada na tabela `gold.fato_vendas` (`sk_venda`). |
| **3. O que fica de fora** | O pedido como um todo não é o item. Se um pedido contiver 1 notebook e 1 mouse, haverá 1 pedido e 2 itens de pedido distintos. |
| **4. Recortes válidos** | Por pedido (`id_venda`), por departamento e por cliente. |
| **Sinônimos** | *Order Line*, *Line Item*, *Item Vendido*. |
| **Termos Relacionados**| *Ticket Médio*, *Receita Líquida*. |
| **Vínculo Físico** | Coluna `sk_venda` da tabela `gold.fato_vendas`. |
