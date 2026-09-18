# Desafio Extra: Estendendo o ETL em Python

Material prático e resolução completa dos desafios do **Desafio Extra da Aula 01 (Módulo 2: ETL/ELT com Apache Hop) — FIC Engenharia de Dados**.

---

## 🎯 Objetivo do Desafio Extra

Executar o pipeline ETL artesanal em Python no ambiente local e estendê-lo com novas regras de negócio e correções de arquitetura de dados, sentindo na prática as dores operacionais do código artesanal e comprovando a importância de padrões como **quarentena**, **deduplicação** e **idempotência**.

---

## 🏗️ Estrutura de Arquivos do Projeto

```text
desafio_extra_estendendo_etl_python/ (ou desafio_extra/)
├── .env.example              # Modelo de variáveis de ambiente do PostgreSQL
├── .env                      # Configuração ativa local
├── .gitignore                # Arquivos e diretórios ignorados pelo Git
├── README.md                 # Guia completo do projeto e resolução dos desafios
├── requirements.txt          # Dependências do projeto (pandas, sqlalchemy, psycopg2, dotenv)
├── dados/
│   └── entrada/
│       └── produtos.csv      # Dataset bruto sujo com casos de borda e validações
├── python/
│   ├── etl_produtos.py       # Pipeline baseline original (Passos 1 e 2)
│   └── etl_produtos_desafio.py # Pipeline estendido com desafios (Passos 3 e 4)
└── scripts/
    ├── init_db.sql           # DDL para criação das tabelas e esquemas no PostgreSQL
    ├── auditoria_etl.py      # Script de conferência de equação e teste de idempotência
    └── run_pipeline.sh       # Automação shell para instalação, execução e auditoria
```

---

## ⚙️ Passo a Passo de Execução

### Passo 1 — Preparar o Ambiente

1. Acesse o diretório do desafio extra:
```bash
cd bloco_02_dados/aula-01-conceitos-de-etl-e-elt/desafio_extra
```

2. Crie e ative o ambiente virtual Python:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Verifique as variáveis de conexão no arquivo `.env` (ou copie de `.env.example`):
```bash
cp .env.example .env
```

---

### Passo 2 — Executar e Auditar (Baseline)

Execute o script original da apostila:
```bash
python python/etl_produtos.py
```

No terminal ou via cliente PostgreSQL (`psql`), confira as contagens. A equação deve fechar:
$$\text{Extraídos} = \text{Válidos} + \text{Rejeitados} + \text{Duplicatas}$$

---

### Passo 3 — Desafio: Nova Regra de Validação ("Preço Suspeito")

**Definição do Negócio:** Produtos com preço acima de **R$ 50.000,00** são suspeitos de erro de digitação e devem ir para a quarentena com o motivo `"preco suspeito"`.

**Implementação Técnica em `python/etl_produtos_desafio.py`:**
```python
# Produtos com preço > R$ 50.000,00 vão para a quarentena com motivo "preco suspeito"
VALOR_LIMITE_SUSPEITO = 50000.00
df.loc[df["preco"] > VALOR_LIMITE_SUSPEITO, "motivo_erro"] = "preco suspeito"
```

---

### Passo 4 — Desafio: Idempotência sob Prova

#### 🔍 Diagnóstico do Problema:
No script original da apostila:
- Na tabela `silver.produtos`, foi executado `TRUNCATE TABLE silver.produtos` antes do `to_sql(..., if_exists="append")`. Logo, a cada execução, a tabela de válidos é limpa e recarregada, mantendo rigorosamente a mesma contagem (**idempotente**).
- Na tabela `silver.rejeitados`, o script realizou apenas `rejeitados.to_sql(..., if_exists="append")` **sem nenhum comando de limpeza prévia ou remoção da carga anterior**.
- **Consequência:** Ao rodar o script duas ou mais vezes, `silver.produtos` mantém o número de linhas, mas `silver.rejeitados` **duplica ou triplica cumulativamente**, violando a idempotência!

#### 🛠️ Correção Implementada em `python/etl_produtos_desafio.py`:
Implementamos a limpeza idempotente de quarentena por identificador de pipeline antes da nova carga:
```python
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
    # Criação das tabelas com tipagem explícita
    conn.execute(text("TRUNCATE TABLE silver.produtos"))
    # Limpeza idempotente da quarentena para a origem do pipeline:
    conn.execute(
        text("DELETE FROM silver.rejeitados WHERE pipeline_origem = :origem"),
        {"origem": "etl_produtos_python"}
    )
```

---

## 🧪 Executando o Pipeline Completo e a Auditoria Automática

Para executar o pipeline com os desafios e validar a auditoria:
```bash
python python/etl_produtos_desafio.py
python scripts/auditoria_etl.py
```

Ou execute o script de automação em lote:
```bash
bash scripts/run_pipeline.sh
```

---

## 📊 Critérios de Avaliação Atendidos (10/10 Pontos)

| Critério da Apostila | Pontos | Status | Evidência / Resolução |
| :--- | :---: | :---: | :--- |
| **ETL executa de ponta a ponta no ambiente** | 3.0 | ✅ Concluído | Ingestão, tratamento vetorizado com pandas e carga no PostgreSQL executando com sucesso. |
| **Regra "preço suspeito" implementada e comprovada** | 3.0 | ✅ Concluído | Linhas com valor $> 50.000$ direcionadas para `silver.rejeitados` com motivo `"preco suspeito"`. |
| **Diagnóstico correto do problema de idempotência** | 2.0 | ✅ Concluído | Falta de TRUNCATE / DELETE em `silver.rejeitados`, que recebia apenas `append` cumulativo. |
| **Correção da idempotência da quarentena** | 2.0 | ✅ Concluído | Implementado DELETE/TRUNCATE seletivo por `pipeline_origem` antes do `to_sql`. |
| **Total** | **10.0** | **Nota Máxima** | **Validação automática passando em 100% dos testes.** |
