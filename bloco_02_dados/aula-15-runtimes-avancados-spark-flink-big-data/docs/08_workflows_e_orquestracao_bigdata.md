# 08 — Por Que Faz Total Sentido Fazer um Workflow no Apache Hop em Big Data?

> *"Um Pipeline move e transforma linhas de dados. Um Workflow governa o ciclo de vida, as dependências e o destino de toda a arquitetura."*

---

## 🎯 1. Pipeline (.hpl) vs. Workflow (.hwf): A Divisão Essencial

Para entender o porquê de um Workflow fazer tanto sentido, é fundamental revisitar o coração da filosofia do Apache Hop:

```
┌──────────────────────────────────────────────┐       ┌──────────────────────────────────────────────┐
│           PIPELINE (.hpl)                    │       │           WORKFLOW (.hwf)                    │
│           "Data-Flow"                        │       │           "Task-Flow / Job-Flow"             │
├──────────────────────────────────────────────┤       ├──────────────────────────────────────────────┤
│ • Processa LINHAS de dados                   │       │ • Processa TAREFAS e ETAPAS sequenciais      │
│ • Paralelo e contínuo (streaming)            │       │ • Sequencial e condicional (IF / ELSE)       │
│ • Lê CSV, converte tipos, filtra e agrega    │       │ • Checa se arquivo existe, roda pipelines    │
│ • Responde: "COMO os dados são tratados?"    │       │ • Responde: "QUANDO e EM QUE ORDEM rodar?"   │
└──────────────────────────────────────────────┘       └──────────────────────────────────────────────┘
```

---

## 🧩 2. Por Que um Pipeline Sozinho é Insuficiente na Aula 15?

Imagine que você só tenha os três pipelines `.hpl` da aula:
1. `converte_parquet.hpl` (lê CSV $\rightarrow$ gera Parquet)
2. `agrega_vendas_parquet.hpl` (lê Parquet $\rightarrow$ calcula métricas)
3. `responder_desafios_negocio.py` (gera partições e relatórios)

### Os Problemas da Vida Real:
1. **Dependência Temporal Obrigatória**: O pipeline 2 **não pode** rodar antes do pipeline 1 terminar! Se você executar os dois ao mesmo tempo, o pipeline 2 tentará ler um arquivo Parquet incompleto ou inexistente e **morrerá com erro de I/O**.
2. **Arquivos Faltantes**: E se o arquivo `vendas_grandes.csv` ainda não tiver pousado na pasta `dados/entrada/`? Um pipeline puro não sabe "esperar" nem sabe "gerar o arquivo automaticamente".
3. **Tratamento e Convergência de Erros**: Se a conversão falhar no meio (por falta de espaço em disco ou corrupção de dados), você não quer que as consultas de BI rodem sobre dados velhos. Você precisa **abortar** o processo e gravar um log de emergência.

É exatamente aqui que o **Workflow (.hwf)** se torna indispensável!

---

## 🏗️ 3. A Arquitetura do Nosso Workflow Mestre (`workflow_bigdata_mestre.hwf`)

Construímos o workflow [`workflow_bigdata_mestre.hwf`](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-15-runtimes-avancados-spark-flink-big-data/hop/workflows/workflow_bigdata_mestre.hwf) com a seguinte lógica de engenharia de missão crítica:

```
                                  [ START ]
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │ Check: CSV de Entrada Existe? │
                      └───────────────┬───────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
        [ SIM / SUCESSO ]                         [ NÃO / FALHA ]
                 │                                         │
                 │                                         ▼
                 │                         ┌───────────────────────────────┐
                 │                         │ Shell: Gera Vendas se Ausente │
                 │                         └───────────────┬───────────────┘
                 │                                         │
                 └────────────────────┬────────────────────┘
                                      ▼
                      ┌───────────────────────────────┐
                      │ Pipeline: Converte para       │
                      │           Parquet (Snappy)    │
                      └───────────────┬───────────────┘
                                      │
                        [ SUCESSO ]   │   [ FALHA ]
                 ┌────────────────────┴────────────────────┐
                 │                                         │
                 ▼                                         ▼
  ┌─────────────────────────────┐           ┌─────────────────────────────┐
  │ Pipeline: Agrega Vendas     │           │ Log: Erro Convergente       │
  │           Parquet           │           └──────────────┬──────────────┘
  └──────────────┬──────────────┘                          │
                 │                                         ▼
   [ SUCESSO ]   │   [ FALHA ]                      [ ABORT WORKFLOW ]
   ┌─────────────┴─────────────┐
   │                           │
   ▼                           │
┌────────────────────────────┐ │
│ Shell: Responde Desafios   │ │
│        e Particiona Mes    │ │
└──────────────┬─────────────┘ │
               │               │
 [ SUCESSO ]   │   [ FALHA ]   │
 ┌─────────────┴───────────────┘
 │
 ▼
┌────────────────────────────┐
│ Log: Sucesso na            │
│      Orquestração          │
└──────────────┬─────────────┘
               │
               ▼
          [ SUCCESS ]
```

---

## 💡 4. Os 4 Grandes Benefícios Deste Workflow

1. **Auto-Cura / Resiliência (*Self-Healing*)**:
   - A ação `FILE_EXISTS` testa a presença de `vendas_grandes.csv`.
   - Se ele não existir, o workflow desvia para o nó de geração sintética em Python, gera a base e continua o fluxo sem intervenção humana.

2. **Garantia de Ordem de Execução**:
   - Assegura que o arquivo `.parquet` esteja 100% gravado e fechado antes de disparar os nós analíticos de agregação e particionamento Hive.

3. **Convergência de Falhas (Caminho Vermelho)**:
   - Qualquer quebra no pipeline de conversão, na agregação ou no particionamento desvia para um **Log de Erro Unificado** e executa um nó `ABORT`, impedindo corrupção silenciosa de dados.

4. **Pronto para Produção e Agendamento Automático**:
   - Pode ser disparado diretamente via terminal ou Crontab:
   ```bash
   ./scripts/executar_workflow_hop.sh
   ```
   ou via Hop Run:
   ```bash
   hop-run.sh -j default -f hop/workflows/workflow_bigdata_mestre.hwf -r local
   ```

---

## 🎯 Conclusão
Em projetos sérios de Big Data, **Pipelines isolados nunca vão para produção sozinhos**. Eles são sempre envelopados e orquestrados por **Workflows**, que garantem integridade, pré-condições, governança e recuperação de falhas.
