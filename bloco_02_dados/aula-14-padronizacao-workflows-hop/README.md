# Aula 03 (Módulo 2) — Padronização, Workflows, Orquestração e Tratamento de Erros

**FIC Engenharia de Dados**  
**Módulo 2: ETL / ELT com Apache Hop**

---

## 🎯 Objetivos Concluídos

1. **Arquitetura Medallion Completa**:
   - **Bronze (Staging)**: 5 fontes integradas pousando brutas no schema `staging` do PostgreSQL (`produtos`, `vendas`, `avaliacoes`). Regra de ouro atendida: *"Transformações nunca destroem o bronze"*.
   - **Silver**: Dados higienizados, deduplicados e tipados (`silver.produtos`, `silver.vendas`, `silver.avaliacoes`).
   - **Quarentena**: Registros defeituosos desviados formalmente para `silver.rejeitados` via *Error Handling* de transforms no Hop (com diagnóstico de erro, data e pipeline de origem).
   - **Gold / ELT**: Modelagem analítica de alta performance rodando transformações em SQL nativo no PostgreSQL (`silver.avaliacoes_elt`).

2. **Pipelines Apache Hop (.hpl)**:
   - `hop/pipelines/exemplo03_padroniza_produtos.hpl`: Padronização com trim, initcap, limpeza de moeda e data com máscara explícita + Error Handling para quarentena.
   - `hop/pipelines/padroniza_vendas.hpl`: Tratamento de datas mistas, validação de quantidade $\le 0$ para quarentena e deduplicação por chave.
   - `hop/pipelines/padroniza_avaliacoes.hpl`: Trim de comentários e validação de nota regulamentar (1 a 5) com desvio de notas anômalas para quarentena.

3. **Workflows Apache Hop (.hwf) e Orquestração**:
   - `hop/workflows/exemplo04_carga_produtos.hwf`: Orquestração de DDL idempotente, carga e padronização com convergência de erro.
   - `hop/workflows/carga_diaria.hwf` (**Workflow Mestre**): Truncate de staging $\rightarrow$ 5 extrações $\rightarrow$ 3 padronizações Silver $\rightarrow$ Execução ELT $\rightarrow$ Log de Sucesso; qualquer falha converge para **Log de Erro Convergente $\rightarrow$ Abort**. Parametrizado com `${MES_REF}`.

4. **Passo 3 — Desafio: Teste de Fogo**:
   - Comprovado via `scripts/teste_de_fogo_mongo.py`:
     - **Caminho Vermelho**: Simulação de queda do MongoDB aciona o desvio de erro e executa o nó Abort. Log gravado em `dados/teste_de_fogo_log_falha.txt`.
     - **Caminho Verde**: Com o serviço ativo, a orquestração segue o fluxo de sucesso até a conclusão total. Log gravado em `dados/teste_de_fogo_log_sucesso.txt`.

5. **Passo 4 — Desafio: Produção Simulada e Crontab**:
   - Execução via CLI headless comprovada via `./scripts/executar_hop_run.sh 2026-08`.
   - Documentação minuciosa campo a campo da expressão `0 3 * * *` em `crontab_agendamento.md`.

6. **Passo 5 — Desafio ELT**:
   - Implementado em `sql/03_elt_silver_avaliacoes.sql` (`silver.avaliacoes_elt`).
   - Comparação conceitual:
     > *"No pipeline ETL o Hop lê cada avaliação, consome recursos na JVM para aplicar trim e validar notas antes de desovar no banco; no padrão ELT, o dado já pousou na staging e o PostgreSQL utiliza seus índices e engine C otimizada para filtrar e transformar apenas a fatia válida em milissegundos."*

7. **Dashboard Web Interativo (Padrão Aula 13)**:
   - `index.html` (e `dashboard_orquestracao_silver.html`): Interface moderna em Dark Theme com funil Medallion, tabela com busca e filtros de Quarentena, comparativo de código e performance ETL vs ELT e simulador visual do Teste de Fogo.

---

## 📂 Estrutura de Arquivos

```text
bloco_02_dados/aula-14-padronizacao-workflows-hop/
├── dados/
│   ├── bronze/                      # Arquivos brutos com dados corrompidos
│   ├── silver/                      # Dados limpos em CSV
│   ├── quarentena/                  # Rejeitados com diagnóstico detalhado
│   ├── metricas_execucao.json       # Métricas consolidadas
│   ├── teste_de_fogo_log_falha.txt  # Comprovação do caminho vermelho
│   └── teste_de_fogo_log_sucesso.txt# Comprovação do caminho verde
├── hop/
│   ├── pipelines/                   # Arquivos .hpl
│   └── workflows/                   # Arquivos .hwf (carga_diaria e exemplo04)
├── sql/
│   ├── 01_prepara_schemas.sql       # DDL idempotente
│   ├── 02_elt_silver_produtos.sql   # ELT produtos
│   └── 03_elt_silver_avaliacoes.sql # ELT avaliações (Passo 5)
├── scripts/
│   ├── gerar_pipelines_hop.py       # Gerador dos XMLs do Hop
│   ├── executar_carga_completa.py   # Execução end-to-end do pipeline
│   ├── teste_de_fogo_mongo.py       # Teste do caminho vermelho e verde
│   ├── executar_hop_run.sh          # Execução via CLI com parâmetros
│   └── gerar_dashboard.py           # Construtor do Dashboard Web
├── index.html                       # Dashboard Web da aula
├── crontab_agendamento.md           # Explicação detalhada da crontab
└── README.md                        # Este documento
```

---

## 🚀 Como Executar

### 1. Regenerar os Pipelines e Workflows XML do Hop:
```bash
python3 scripts/gerar_pipelines_hop.py
```

### 2. Executar a Carga Completa End-to-End:
```bash
python3 scripts/executar_carga_completa.py
```

### 3. Executar o Teste de Fogo (Caminho Vermelho vs Verde):
```bash
python3 scripts/teste_de_fogo_mongo.py
```

### 4. Executar via Hop CLI (Produção Simulada):
```bash
./scripts/executar_hop_run.sh 2026-08
```

### 5. Abrir o Dashboard Web:
Abra o arquivo [index.html](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-14-padronizacao-workflows-hop/index.html) diretamente no seu navegador.
