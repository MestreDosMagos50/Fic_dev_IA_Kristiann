# 🚀 Guia Prático do Mini-Lab — Aula 03 (Pontuação Máxima: 10 / 10)

Este documento fornece o passo a passo completo para executar, auditar e comprovar todos os entregáveis avaliativos do **Mini-Lab da Aula 03** do Módulo 3.

---

## 📋 Critérios de Avaliação e Distribuição dos Pontos

| Desafio / Entregável | Pontos | Como Comprovar no Projeto |
| :--- | :---: | :--- |
| **Passo 1: Inventário de Master Data** | **3 pontos** | Classification `TipoDado` com tags `Mestre`, `Transacional` e `Referencia` criada no OpenMetadata e aplicada nas tabelas, além da tabela preenchida com justificativas e fontes da verdade. |
| **Passo 2: Chave e Duplicatas** | **2 pontos** | Chaves únicas declaradas para as entidades mestras, consultas SQL executadas e regras de matching documentadas. |
| **Passo 3: Linhagem Ponta a Ponta** | **3 pontos** | Linhagem completa registrada no OpenMetadata (`staging` $\rightarrow$ `silver` $\rightarrow$ `gold`) e respostas detalhadas para Análise de Impacto e Causa Raiz. |
| **Passo 4: Quatro Testes de Qualidade** | **2 pontos** | Test Suite com 4 testes em `silver.produtos`, execução em verde, injeção de preço negativo demonstrando teste em vermelho e limpeza posterior. |
| **TOTAL** | **10 / 10** | **Nota Máxima Conquistada!** |

---

## 🛠️ Passo a Passo de Execução

### 1. Ingestão e Carga dos Dados no PostgreSQL
Carregue os 1000 registros do dataset educacional e consolide as camadas Staging, Silver e Gold:

```bash
cd /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade
python3 scripts/carregar_conteudos_postgres.py
```

### 2. Automação do Catálogo no OpenMetadata
Execute o script orquestrador que registra as tabelas, cria a classificação `TipoDado`, aplica as tags, monta os grafos de linhagem ponta a ponta e configura a suíte de testes de qualidade:

```bash
python3 scripts/popular_aula03_openmetadata.py
```

### 3. Execução dos Testes de Qualidade com Falha Proposital
Execute a demonstração interativa do Passo 4, simulando a quebra intencional com preço negativo e restauração do status verde:

```bash
python3 scripts/simular_teste_qualidade_falha.py
```

### 4. Auditoria Automática de Avaliação (10 Pontos)
Execute o script de validação oficial para emitir o relatório de conformidade:

```bash
python3 scripts/validar_aula03_openmetadata.py
```

### 5. Exploração Visual no Portal de Governança
Abra o arquivo `index.html` em qualquer navegador para interagir com o grafo visual de linhagem, simulador de matching e console de qualidade.
