# 🎯 Passo 4 — As Dimensões da Qualidade de Dados e Testes no OpenMetadata

Qualidade de dados não é uma opinião estética ou sensação subjetiva; é um **conjunto de propriedades mensuráveis, auditáveis e programáveis** que determinam a aptidão do dado para apoiar decisões operacionais e estratégicas.

Neste relatório técnico, detalhamos as **6 Dimensões Clássicas da Qualidade de Dados** (DAMA-DMBOK / Batini & Scannapieco) e demonstramos a execução da **Suíte de Testes Automatizada** em `silver.produtos`, incluindo o teste de estresse com injeção de falha proposital.

---

## 📐 As 6 Dimensões da Qualidade de Dados

| Dimensão | Pergunta Fundamental | O que Testa no Banco de Dados | Implementação no Nosso Projeto |
| :--- | :--- | :--- | :--- |
| **1. Completude (*Completeness*)** | *Faltam valores obrigatórios?* | Presença de nulos (`IS NULL`) ou strings vazias em colunas essenciais. | `silver.produtos.categoria` não pode ser nula; `silver.conteudos.titulo` obrigatório. |
| **2. Unicidade (*Uniqueness*)** | *Há duplicatas indesejadas?* | Registros repetidos pela chave primária ou chave de negócio. | `silver.produtos.codigo` é único; `silver.conteudos.conteudo_id` único. |
| **3. Validade (*Validity*)** | *Os dados respeitam as regras e formatos?* | Faixas numéricas válidas, regex de e-mail/CPF, domínios fechados (*enum*). | `silver.produtos.preco > 0`; `carga_horaria_min BETWEEN 1 AND 5000`. |
| **4. Consistência (*Consistency*)** | *Os dados concordam entre tabelas e fontes?* | Integridade referencial (FKs), chaves órfãs, dados cruzados. | Todo `sk_produto` em `gold.fato_vendas` deve existir em `gold.dim_produto`. |
| **5. Atualidade (*Freshness*)** | *O dado está recente e pronto a tempo?* | Intervalo de tempo entre a ocorrência do fato no mundo real e a carga no banco. | `fato_vendas` e `staging.conteudos` com carimbo de carga nas últimas 24 horas. |
| **6. Acurácia (*Accuracy*)** | *O dado reflete fielmente a realidade?* | Verificação contra fontes de verdade externas (cartórios, auditoria humana, Data Steward). | Verificação semântica: "R$ 4.599,90 para um caderno de 50 folhas" é um valor tecnicamente válido (número positivo), mas *impreciso/errado* no mundo real. |

---

## 🧪 Quatro Testes de Qualidade em `silver.produtos` (Passo 4)

Conforme especificado no Mini-Lab, estruturamos os 4 testes canônicos no OpenMetadata e no PostgreSQL:

### Especificação dos Testes

1. **Teste 1 — Unicidade:**
   - **Alvo:** `silver.produtos.codigo`
   - **Regra:** `COUNT(*) - COUNT(DISTINCT codigo) == 0`
   - **OpenMetadata Test Definition:** `columnValuesToBeUnique`
2. **Teste 2 — Completude:**
   - **Alvo:** `silver.produtos.categoria`
   - **Regra:** `COUNT(*) FILTER (WHERE categoria IS NULL) == 0`
   - **OpenMetadata Test Definition:** `columnValuesToBeNotNull`
3. **Teste 3 — Validade (Faixa de Preço):**
   - **Alvo:** `silver.produtos.preco`
   - **Regra:** `preco >= 0.01` (preços estritamente positivos)
   - **OpenMetadata Test Definition:** `columnValuesToBeBetween` (`min: 0.01, max: 999999.99`)
4. **Teste 4 — Consistência de Volume:**
   - **Alvo:** Tabela `silver.produtos`
   - **Regra:** `COUNT(*) BETWEEN 1 AND 10000` (evita carga fantasma ou explosão cartesiana)
   - **OpenMetadata Test Definition:** `tableRowCountToBeBetween` (`min: 1, max: 10000`)

---

## 💥 Demonstração Prática: Provocando a Falha Proposital

Para demonstrar o funcionamento do sistema de alerta em vermelho do catálogo, simulamos uma anomalia real de ingestão:

### 1. Estado Inicial: Integridade Nominal (VERDE / PASSED)
Execução dos testes na base íntegra:
```text
[✔ PASSED] Teste 1 - Unicidade de Codigo: 0 duplicatas encontradas.
[✔ PASSED] Teste 2 - Nao-nulidade de Categoria: 0 nulos encontrados.
[✔ PASSED] Teste 3 - Faixa Valida de Preco: 0 valores <= 0.
[✔ PASSED] Teste 4 - Contagem de Linhas: 5 linhas (dentro da faixa 1-10.000).
Status Geral: 100% SUCESSO (4/4 PASS)
```

### 2. Injeção da Falha: Inserção de Preço Negativo
Simulamos um bug no ERP que exportou um produto com preço promocional invertido:
```sql
INSERT INTO silver.produtos (codigo, nome, preco, categoria, data_cadastro)
VALUES ('PROD-FALHA-TESTE', 'Cadeira Gamer com Preço Negativo Anômalo', -199.90, 'Móveis', CURRENT_DATE);
```

### 3. Reexecução do Teste: Alerta Crítico (VERMELHO / FAILED)
Ao reexecutar a suíte de qualidade:
```text
[✔ PASSED] Teste 1 - Unicidade de Codigo: 0 duplicatas.
[✔ PASSED] Teste 2 - Nao-nulidade de Categoria: 0 nulos.
[❌ FAILED] Teste 3 - Faixa Valida de Preco: 1 registro inválido detectado!
             Infrator: PROD-FALHA-TESTE (preco: -199.90)
             Esperado: preco >= 0.01 | Encontrado: -199.90
[✔ PASSED] Teste 4 - Contagem de Linhas: 6 linhas (dentro da faixa).
Status Geral: ALERTA CRÍTICO (1 FALHA DETECTADA)
```

### 4. Correção e Restauração da Integridade (VERDE / REHABILITATED)
Remoção do registro anômalo:
```sql
DELETE FROM silver.produtos WHERE codigo = 'PROD-FALHA-TESTE';
```
Reexecução imediata:
```text
[✔ PASSED] Teste 3 - Faixa Valida de Preco: 0 registros inválidos.
Status Geral: 100% SUCESSO (INTEGRIDADE TOTALMENTE RESTAURADA)
```

Essa demonstração comprova a eficácia de **Data Observability**: o problema é interceptado na camada Silver antes de poluir a camada Gold e contaminar os relatórios da diretoria.
