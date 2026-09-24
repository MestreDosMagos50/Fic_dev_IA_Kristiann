# 🎯 Guia das Dimensões da Qualidade de Dados e Data Observability

## 1. Por que Qualidade de Dados é Vital?

Em um ecossistema de dados moderno, a confiança nos dados é o ativo mais valioso de uma equipe. Quando um relatório da diretoria apresenta números incorretos, o problema raramente é o SQL final: na grande maioria dos casos, trata-se de **falhas silenciosas de qualidade** que ocorreram horas ou dias antes nas camadas de ingestão.

A disciplina de **Qualidade de Dados (*Data Quality*)** transforma a validação empírica em **regras automáticas e mensuráveis** que operam como testes unitários contínuos sobre os dados em produção.

---

## 2. As 6 Dimensões Canônicas da Qualidade (DAMA-DMBOK)

### 1. Completude (*Completeness*)
- **Conceito:** Proporção de dados presentes em relação ao total esperado.
- **Risco de quebra:** Campos nulos em chaves de junção geram perda de registros em `INNER JOIN` ou agrupamentos `(null)` em relatórios.
- **Exemplo de Teste:** `silver.produtos.categoria` deve ser preenchida obrigatoriamente (`columnValuesToBeNotNull`).

### 2. Unicidade (*Uniqueness*)
- **Conceito:** Ausência de registros repetidos representando a mesma entidade ou transação.
- **Risco de quebra:** Duplicatas de venda inflam faturamento; duplicatas de cliente geram contagem distorcida.
- **Exemplo de Teste:** `silver.produtos.codigo` não pode ter duplicatas (`columnValuesToBeUnique`).

### 3. Validade (*Validity*)
- **Conceito:** Conformidade dos dados em relação às regras de sintaxe, formato, domínio aceito e faixas de valores de negócio.
- **Risco de quebra:** Preços negativos, datas futuras de nascimento, notas fora da escala de 1 a 5.
- **Exemplo de Teste:** `silver.produtos.preco` deve ser estritamente maior que zero (`columnValuesToBeBetween(min=0.01)`).

### 4. Consistência (*Consistency*)
- **Conceito:** Harmonia e ausência de contradição entre dados armazenados em tabelas diferentes ou entre campos relacionados.
- **Risco de quebra:** Uma venda registrada para um produto cujo código não existe no catálogo de produtos (violação de integridade referencial).
- **Exemplo de Teste:** Todo `sk_produto` em `fato_vendas` deve existir em `gold.dim_produto`.

### 5. Atualidade / Frequência (*Freshness / Timeliness*)
- **Conceito:** O quão recente é o dado em relação ao momento da sua utilização.
- **Risco de quebra:** Um dashboard que exibe dados de 3 dias atrás sem que ninguém tenha percebido a interrupção do Airflow.
- **Exemplo de Teste:** `fato_vendas` deve receber novos registros a cada 24 horas (`tableRowInsertedCountToBeBetween`).

### 6. Acurácia (*Accuracy*)
- **Conceito:** Fidelidade entre o dado armazenado e o objeto real no mundo físico.
- **Por que é a mais difícil de automatizar?**
  Um valor numérico de `R$ 4.599,90` para um caderno universitário comum é tecnicamente válido (número positivo, não nulo, tipado como decimal), mas **inapropriado e impreciso** na vida real.
  Por essa razão, a acurácia depende de validações externas (ex: conciliação com extrato bancário) e da atuação ativa de **Data Stewards**.

---

## 3. Test Suites e Test Cases no OpenMetadata

O OpenMetadata adota o padrão de **Data Observability** integrado ao catálogo:

- **Data Profiler:** O catálogo perfila automaticamente as colunas, coletando estatísticas de nulos, valores distintos, médias, valores mínimos, máximos e distribuição de frequência.
- **Test Suite:** Uma coleção lógica de testes associada a uma tabela específica.
- **Test Case:** Uma regra individual vinculada a uma coluna ou tabela baseada em um `TestDefinition` (ex: `columnValuesToBeNotNull`).
- **Histórico e Tendências:** Os resultados das execuções periódicas são salvos com data e hora, permitindo à equipe de dados saber se uma anomalia "sempre existiu" ou "começou ontem às 03:00 da manhã".
