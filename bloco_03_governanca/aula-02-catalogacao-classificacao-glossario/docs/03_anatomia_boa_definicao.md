# 03 — A Anatomia de uma Boa Definição de Negócio
## Módulo 3: Governança de Dados com OpenMetadata — Aula 02

---

## 1. Por que Definições Vagas Destroem a Confiança nos Dados?

Em muitas empresas, reuniões de diretoria se transformam em discussões estéreis sobre *"qual planilha tem o número certo"*. O financeiro apresenta um ticket médio de R$ 1.250; o marketing apresenta R$ 980; a equipe de vendas apresenta R$ 1.400.

O erro não está no SQL nem na competência dos analistas. O erro está na **ausência de uma definição de negócio formal**:
- O financeiro excluiu os cancelados e deduziu impostos.
- O marketing dividiu pelo total de acessos de usuários em vez de pedidos.
- As vendas somaram o valor bruto incluindo o frete cobrado.

---

## 2. A Estrutura das Quatro Partes Obrigatórias

Toda definição no Glossário de Negócio deve conter expressamente quatro seções:

### 1. O que é
A descrição conceitual em linguagem clara e acessível para qualquer stakeholder da empresa, evitando jargões puramente técnicos.

### 2. Como se calcula
A expressão matemática, lógica ou fórmula SQL determinística utilizada para materializar o indicador a partir das tabelas físicas.

### 3. O que fica de fora (Exclusões)
**A parte mais importante e frequentemente esquecida.** Especifica claramente quais registros, status, taxas ou situações excepcionais são expurgados do cálculo. É aqui que se eliminam as divergências entre relatórios!

### 4. Recortes válidos (Granularidade)
Define em quais níveis de agregação ou dimensões o indicador pode ser fatiado com consistência (ex: mensal, por categoria, por canal).

---

## 3. Comparativo Prático: Ruim vs. Profissional

### Exemplo 1: Ticket Médio

> ❌ **Definição Ruim:**  
> *"Ticket médio é a média dos pedidos."*  
> *(Comentário: Não explica se considera cancelados, não diz se inclui frete, não indica a tabela de origem).*

> ✅ **Definição Profissional:**  
> *"**Ticket Médio** — Valor monetário médio despendido pelos clientes por pedido de compra concluído em um período determinado.  
> **Cálculo:** Soma da receita faturada (`valor_liquido`) dividida pela contagem distinta de pedidos (`id_venda`) da tabela `gold.fato_vendas`.  
> **Exclusões:** Pedidos com `status_pedido IN ('Cancelado', 'Devolvido')` não entram no numerador nem no denominador; custos de frete cobrados e taxas de juros de parcelamento de cartão não compõem o valor.  
> **Recortes válidos:** Calculável e agregável por mês contábil, departamento/categoria de produto e macrorregião geográfica do cliente."*

---

### Exemplo 2: Margem de Contribuição

> ❌ **Definição Ruim:**  
> *"Margem é o lucro da venda."*

> ✅ **Definição Profissional:**  
> *"**Margem de Contribuição** — Ganho financeiro real remanescente da venda de cada mercadoria após a dedução de todos os custos variáveis diretos e tributos incidentes.  
> **Cálculo:** `valor_liquido - custo_produto - impostos` na tabela `gold.fato_vendas`.  
> **Exclusões:** Custos fixos e despesas corporativas gerais não são rateados no nível do item. **Deduz expressamente 18% de alíquota tributária direta (ICMS + PIS/COFINS)** e o custo de reposição CMV histórico.  
> **Recortes válidos:** Por categoria de produto, canal de conversão e faixa de preço."*
