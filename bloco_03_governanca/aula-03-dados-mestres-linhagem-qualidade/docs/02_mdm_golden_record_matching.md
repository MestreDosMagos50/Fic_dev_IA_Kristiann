# 🧩 Master Data Management (MDM): Golden Record e Regras de Matching

## 1. O Problema da Visão Única (*Single Source of Truth*)

Em grandes organizações, diferentes sistemas operacionais são desenvolvidos ou adquiridos em épocas distintas, com bancos de dados isolados (*silos de dados*). O mesmo cliente pode ser registrado de três formas diferentes:
1. No E-Commerce: `Maria S. Souza` (cadastrada com e-mail pessoal e sem CPF).
2. No CRM: `MARIA SILVA SOUZA` (com CPF e telefone residencial).
3. No ERP/Faturamento: `M. S. Souza` (com endereço de entrega comercial).

### As Consequências do Descontrole
- **Contagem inflada:** Uma única pessoa física é contada como 3 clientes distintos no dashboard de marketing.
- **Quebra na análise de recorrência (*LTV / Churn*):** As compras feitas em canais diferentes nunca são agregadas ao mesmo histórico.
- **Spam e desgaste:** A mesma cliente recebe três e-mails promocionais idênticos na mesma semana.
- **Inconsistência contábil:** Divergência de faturamento entre o financeiro e o comercial.

---

## 2. O Ciclo do MDM (*Master Data Management*)

A disciplina de **Gestão de Dados Mestres (MDM)** resolve essa fragmentação através de um ciclo estruturado em 5 etapas:

```text
┌───────────────────────────────┐
│ 1. Identificar Entidades      │ (Clientes, Produtos, Autores, Fornecedores)
└──────────────┬────────────────┘
               │
┌──────────────▼────────────────┐
│ 2. Definir Fonte de Verdade   │ (Qual sistema manda em caso de conflito?)
└──────────────┬────────────────┘
               │
┌──────────────▼────────────────┐
│ 3. Regras de Correspondência  │ (Matching: determinístico por chave ou difuso)
└──────────────┬────────────────┘
               │
┌──────────────▼────────────────┐
│ 4. Estabelecer Golden Record  │ (Consolidação da versão canônica única)
└──────────────┬────────────────┘
               │
┌──────────────▼────────────────┐
│ 5. Governar e Manter          │ (Auditoria contínua por Data Stewards)
└───────────────────────────────┘
```

---

## 3. O Conceito de *Golden Record* (Registro Dourado)

O **Golden Record** é a versão única, oficial, confiável e consolidada de uma entidade mestre. Ele é construído reunindo os atributos mais precisos de cada sistema de origem:
- **Origem A (E-Commerce):** Fornece o e-mail mais recente e preferências de navegação.
- **Origem B (ERP Fiscal):** Fornece o CPF validado e a razão social.
- **Origem C (CRM):** Fornece o telefone de contato e o segmento de relacionamento.

O resultado final na camada Gold (`gold.dim_cliente`) é um registro enriquecido que nenhuma fonte isolada possuía sozinha.

---

## 4. Tipos de Regras de Correspondência (*Matching Rules*)

Para saber se dois registros pertencem à mesma entidade sem que haja uma chave primária compartilhada, o MDM utiliza duas abordagens:

### A. Matching Determinístico (Baseado em Regras Exatas)
- Comparações lógicas diretas:
  - `CPF_A == CPF_B`
  - `LOWER(TRIM(EMAIL_A)) == LOWER(TRIM(EMAIL_B))`
  - `CODIGO_PRODUTO_A == CODIGO_PRODUTO_B`
- **Vantagem:** Sem falso-positivos (100% determinístico).
- **Desvantagem:** Falha quando há erros de digitação (ex: `usuario@gmail.con` vs `usuario@gmail.com`).

### B. Matching Probabilístico / Difuso (*Fuzzy Matching*)
- Algoritmos matemáticos de similaridade de texto:
  - **Distância de Levenshtein:** Conta o número mínimo de inserções, remoções e substituições para transformar uma palavra na outra.
  - **Jaro-Winkler:** Avalia semelhança entre nomes, dando peso extra a prefixos comuns.
  - **Metaphone / Soundex:** Agrupa palavras pela semelhança fonética (ex: "Luiz" e "Luís" soam idênticos).
- **Exemplo de Regra:** Se `JaroWinkler(Nome_A, Nome_B) > 0.88` E `Cidade_A == Cidade_B` E `AnoNasc_A == AnoNasc_B` $\rightarrow$ Considerar mesma pessoa.

---

## 5. Regras de Sobrevivência (*Survivorship Rules*)

Quando dois registros colidem e precisam ser unificados em um único Golden Record, as regras de sobrevivência determinam de qual linha vem cada atributo:
- **Mais Recente (*Most Recent*):** Prevalece o valor com a maior data de atualização (usado para endereço e telefone).
- **Fonte Mais Confiável (*Source Authority*):** O ERP manda no CNPJ/Razão Social; o CRM manda nas preferências.
- **Maior Frequência (*Frequency / Mode*):** Se 4 sistemas dizem que o gênero é "M" e 1 diz "F", prevalece "M".
- **Completude / Não-Nulo (*Completeness*):** Prevalece o registro que possui o campo preenchido sobre o nulo.

### Caso Prático no Dataset de Conteúdos da Aula 03
No arquivo `conteudos.csv`, encontramos **11 duplicatas de negócio (22 registros)** de títulos republicados com pequenas variações de carga horária e datas. Aplicamos a regra:
- **Matching:** `LOWER(TRIM(titulo)) + LOWER(TRIM(autor))`
- **Golden Record:** A versão com a menor data de publicação original (`FIRST_VALUE(conteudo_id)`).
- **Histórico:** A tabela dimensional `gold.dim_conteudo` consolidou 989 Golden Records, e a tabela fato `gold.fato_publicacoes` preservou todas as 1000 publicações vinculadas à chave mestra canônica.
