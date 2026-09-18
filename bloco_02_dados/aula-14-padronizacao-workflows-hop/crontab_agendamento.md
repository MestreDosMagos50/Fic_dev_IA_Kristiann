# ⏰ Documentação de Agendamento em Produção (Crontab)

> **FIC Engenharia de Dados | Módulo 2: ETL/ELT com Apache Hop**  
> **Aula 03: Padronização, Workflows, Orquestração e Tratamento de Erros**  
> **Passo 4 — Desafio: Produção Simulada e Agendamento Automático**

---

## 📌 Linha do Crontab para Carga Diária às 3h da Manhã

```bash
0 3 * * * /home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh --project ecommerce --file /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-14-padronizacao-workflows-hop/hop/workflows/carga_diaria.hwf --parameters MES_REF=$(date +\%Y-\%m) >> /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-14-padronizacao-workflows-hop/dados/execucao_cron.log 2>&1
```

---

## 🔍 Explicação Detalhada Campo a Campo da Expressão `0 3 * * *`

A tabela cron no Linux utiliza uma estrutura canônica de **5 campos temporais**, lidos da esquerda para a direita:

| Campo | Posição | Valor na Expressão | Significado | Faixa Válida |
| :--- | :---: | :---: | :--- | :---: |
| **Minuto** | 1º | `0` | Executa no minuto exato `00` da hora designada | `0 - 59` |
| **Hora** | 2º | `3` | Executa às `03h` da madrugada (horário de menor concorrência no banco) | `0 - 23` |
| **Dia do Mês** | 3º | `*` | Executa em **todos** os dias do mês (sem restrição de calendário) | `1 - 31` |
| **Mês do Ano** | 4º | `*` | Executa em **todos** os meses (Janeiro a Dezembro) | `1 - 12` |
| **Dia da Semana** | 5º | `*` | Executa em **todos** os dias da semana (Domingo a Sábado) | `0 - 7` (0 ou 7 = Domingo) |

### 🛠️ Parâmetros e Elementos Adicionais da Linha:

1. **Chamada do Executável**:
   - `/caminho/hop-run.sh`: Binário oficial do Apache Hop que executa workflows e pipelines em modo *headless* (sem GUI).
2. **`--project ecommerce` (`-j`)**:
   - Define o projeto de ciclo de vida configurado, garantindo isolamento de metadados, conexões de banco e caminhos relativos `${PROJECT_HOME}`.
3. **`--file .../carga_diaria.hwf` (`-f`)**:
   - Aponta para o arquivo do Workflow Mestre que gerencia os caminhos de sucesso e falha (Abort).
4. **`--parameters MES_REF=$(date +\%Y-\%m)` (`-p`)**:
   - Injeta dinamicamente a data de referência no formato `AAAA-MM` (ano e mês corrente), garantindo que pipelines parametrizados leiam os arquivos correspondentes (ex: `vendas_2026-08.csv`).
   - *Nota Técnica*: No cron, o caractere `%` possui significado especial (newline), por isso deve ser escapado como `\%`.
5. **Redirecionamento de Saída (`>> .../execucao_cron.log 2>&1`)**:
   - Redireciona tanto a saída padrão (`stdout - 1`) quanto a saída de erros (`stderr - 2`) para o arquivo de log para fins de auditoria e observabilidade DataOps.

---

## 🌐 Orquestração em Escala (Hop + Apache Airflow)

Em arquiteturas analíticas corporativas de larga escala:
- O **Apache Hop** atua como motor de execução (*Execution Engine*), realizando transformações de alto volume com quarentena.
- O **Apache Airflow / Prefect** atua como orquestrador maestro (*Master Orchestrator*), disparando o `hop-run.sh` via operadores (`BashOperator` ou `KubernetesPodOperator`), monitorando SLAs, linhagem de dados e alertas em canais de incidentes (Slack/PagerDuty).
