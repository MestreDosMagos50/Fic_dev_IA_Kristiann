# 02 — Apache Spark em Detalhes: O Motor do Processamento em Lote Massivo

> *"O Apache Spark unificou a computação distribuída ao transformar processamento em disco do Hadoop MapReduce em computação resiliente em memória."*

---

## 🏗️ 1. Arquitetura de Execução: Driver e Executors

O Apache Spark opera em um modelo mestre-trabalhador (*Master-Worker*):

```
                        ┌─────────────────────────┐
                        │      SPARK DRIVER       │
                        │  - SparkSession / DAG   │
                        │  - Catalyst Optimizer   │
                        │  - Coordenação Central  │
                        └────────────┬────────────┘
                                     │
                   ┌─────────────────┴─────────────────┐
                   ▼                                   ▼
        ┌─────────────────────┐             ┌─────────────────────┐
        │     EXECUTOR 1      │             │     EXECUTOR 2      │
        │  - JVM Worker       │             │  - JVM Worker       │
        │  - Tarefas (Tasks)  │             │  - Tarefas (Tasks)  │
        │  - Cache em Memória │             │  - Cache em Memória │
        │  - Partições A e B  │             │  - Partições C e D  │
        └─────────────────────┘             └─────────────────────┘
```

### O Spark Driver (O Cérebro)
- Executa a função `main()` do seu programa Python (`pyspark`) ou Scala/Java;
- Cria e gerencia a `SparkSession`;
- Converte o código do usuário em um grafo de execução lógica e física (**DAG**);
- Agenda as tarefas (*tasks*) e as distribui entre os *Executors*;
- Monitora a saúde do cluster e responde a falhas de nós.

### Os Spark Executors (Os Músculos)
- Processos JVM residentes nos nós de trabalho (*Worker Nodes*);
- Executam as tarefas computacionais atribuídas pelo Driver;
- Armazenam em cache (*RAM/Disco*) as partições de dados quando solicitado;
- Devolvem métricas e resultados para o Driver.

---

## 📊 2. DataFrame Distribuído: Da CPU Local para o Cluster

Se você já usou `pandas`, a sintaxe do `pyspark.sql.DataFrame` é deliberadamente similar. Porém, a anatomia interna é completamente diferente:

| Característica | `pandas.DataFrame` | `pyspark.sql.DataFrame` |
| :--- | :--- | :--- |
| **Localização** | 100% na memória RAM de **uma máquina** | Fatiado em **dezenas/milhares de partições** no cluster |
| **Capacidade Máxima** | Limitada pela RAM local (ex: 16 GB) | Petabytes (soma da RAM de centenas de nós) |
| **Execução** | Imediata (*Eager Execution*) | Tardia (*Lazy Evaluation*) com otimização global |
| **Engine de Otimização** | Nenhuma (executa cada instrução na hora) | **Catalyst Optimizer** (reorganiza o plano físico) |

---

## ⏳ 3. Lazy Evaluation: Transformations vs. Actions

No Spark, seu código não executa no momento em que você digita uma transformação. Ele apenas constrói um **Plano Lógico**!

### A. Transformações (Lazy / Preguiçosas)
Apenas declaram como derivar um novo DataFrame a partir de outro. Não leem 1 byte de disco!
- Exemplos: `.filter()`, `.select()`, `.withColumn()`, `.groupBy()`, `.join()`, `.dropDuplicates()`.

### B. Ações (Eager / Executáveis)
Gatilham a compilação de todo o pipeline pelo Catalyst Optimizer e disparam a execução física nos nós:
- Exemplos: `.count()`, `.show()`, `.collect()`, `.write.parquet()`, `.take()`.

```python
# O Spark não lê o arquivo aqui (apenas valida schema):
df = spark.read.parquet("vendas.parquet")

# O Spark não filtra nem agrupa nada aqui:
df_filtrado = df.filter(df.quantidade > 0)
df_agregado = df_filtrado.groupBy("categoria").sum("receita")

# AQUI E SOMENTE AQUI o Spark compila o DAG e processa os nós:
df_agregado.write.parquet("resultado_agregado.parquet")
```

### Por que a Lazy Evaluation é Revolucionária?
Se você fizesse `.select("categoria", "receita").filter(df.ano == 2026)`, o **Catalyst Optimizer** faz:
1. **Predicate Pushdown**: Desce o filtro `ano == 2026` para a leitura direta do arquivo no disco (lê apenas os row groups necessários);
2. **Projection Pruning**: Descarta todas as outras 20 colunas do arquivo na leitura, economizando 80% de I/O de rede e disco.

---

## 🔀 4. O Custo do Shuffle: Dependências Estreitas vs. Amplas

Na computação distribuída, o gargalo raramente é CPU; é **I/O de rede e transferência entre nós**.

```
    DEPENDÊNCIA ESTREITA (Narrow)          DEPENDÊNCIA AMPLA (Wide - Shuffle)
        Sem troca de dados pela rede                 Dados redistribuídos pela rede
    
     [P1: SP] ──filter──> [P1: SP]               [P1: SP, RJ] ─┐   ┌─> [P1: só SP]
     [P2: RJ] ──filter──> [P2: RJ]               [P2: SP, MG] ──┼─┼──> [P2: só RJ]
     [P3: MG] ──filter──> [P3: MG]               [P3: RJ, MG] ─┘   └─> [P3: só MG]
      (Ultra-rápido, in-memory)                 (Altíssimo custo de rede e disco)
```

### Dependências Estreitas (*Narrow Dependencies*)
Cada partição de saída depende de exatamente **uma** partição de entrada. Os dados permanecem na mesma máquina e no mesmo núcleo.
- *Exemplos*: `map()`, `filter()`, `select()`.

### Dependências Amplas (*Wide Dependencies*) e o **SHUFFLE**
Para calcular um `groupBy("categoria")` ou um `join` entre duas tabelas, registros com a mesma chave (ex: todas as vendas de "Eletrônicos") que estavam espalhados nos executores 1, 2 e 3 precisam ser **reunidos na mesma máquina** para serem somados.
- **O Shuffle envolve**:
  1. Serialização dos dados em disco local no nó de origem;
  2. Envio dos bytes através do switch de rede do datacenter;
  3. Deserialização e agrupamento no nó de destino.
- **Impacto**: O Shuffle é o principal causador de lentidão e estouro de memória (*Out of Memory - OOM*) em Big Data.

---

## 💡 5. Regras de Ouro do Engenheiro Spark

1. **Evite `.collect()` em datasets grandes**: Ele puxa todos os dados do cluster para a memória RAM do *Driver*. Se os dados tiverem 100 GB e seu Driver tiver 4 GB, o processo morre instantaneamente com OOM.
2. **Filtre o mais cedo possível**: Permita que o Catalyst utilize *Predicate Pushdown*.
3. **Cuidado com data skew (assimetria de partições)**: Se 90% das suas vendas forem de São Paulo, o nó que processar a partição de SP levará 1 hora enquanto todos os outros nós ficarão ociosos após 2 minutos.
