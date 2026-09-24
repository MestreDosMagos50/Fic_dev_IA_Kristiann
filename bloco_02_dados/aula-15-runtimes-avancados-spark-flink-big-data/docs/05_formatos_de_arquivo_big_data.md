# 05 — Formatos de Arquivo para Big Data: O Fim do CSV e a Supremacia do Parquet

> *"Em Big Data, CSV e JSON não sobrevivem. Tentar rodar analytics em terabytes de CSV é o equivalente a carregar água com uma peneira."*

---

## 🚫 1. Por Que CSV e JSON Falham em Escala?

1. **Armazenamento Baseado em Linha (*Row-Oriented*)**: Para calcular a soma de uma única coluna (ex: `receita`), a máquina é forçada a ler o arquivo inteiro do início ao fim, puxando todas as outras 40 colunas inúteis para a memória.
2. **Parsing de Texto Caríssimo**: Cada linha de CSV precisa ser decodificada caractere por caractere em busca de vírgulas e quebras de linha `\n`. Converter strings de texto `"2026-08-15"` ou `"199.90"` para inteiros ou floats em runtime consome até 80% do tempo de CPU!
3. **Sem Schema Embutido**: CSVs não guardam se a coluna é `INT`, `FLOAT` ou `STRING`. As ferramentas precisam adivinhar (*schema inference*), gerando erros de tipagem e lentidão.
4. **Pobre Compressão**: Como linhas misturam texto, números e datas, os algoritmos de compressão genéricos (GZIP/ZIP) encontram pouca repetitividade entre bytes adjacentes.

---

## 🏛️ 2. A Revolução do Formato Colunar: Apache Parquet

Desenvolvido pelo Twitter e Cloudera com base no paper *Dremel* do Google (2010), o **Apache Parquet** revolucionou o armazenamento analítico.

```
FORMATO BASEADO EM LINHA (CSV):          FORMATO COLUNAR (PARQUET):
Linha 1: [ID1, "Teclado", 150.00, "Sul"]    Coluna ID:        [ID1, ID2, ID3]
Linha 2: [ID2, "Mouse",    80.00, "Sul"]    Coluna Produto:   ["Teclado", "Mouse", "Monitor"]
Linha 3: [ID3, "Monitor", 900.00, "Norte"]  Coluna Preço:     [150.00, 80.00, 900.00]
                                            Coluna Região:    ["Sul", "Sul", "Norte"]
```

### Por Que Colunar é Infinitamente Superior para Consultas?

#### 1. Projeção de Colunas (*Column Projection*)
Se você rodar:
```sql
SELECT SUM(preco) FROM vendas;
```
O motor de consulta **lê apenas os bytes da coluna Preço**. As colunas ID, Produto e Região sequer são lidas do disco SSD ou da rede do S3/Blob Storage!

#### 2. Compressão Extrema (Snappy / ZSTD)
Quando dados do mesmo tipo ficam juntos, a repetitividade é gigantesca:
- A coluna `regiao` terá milhões de valores repetidos ("Sul", "Sul", "Sul").
- O Parquet aplica técnicas avançadas:
  - **Dictionary Encoding**: Substitui strings repetidas por inteiros minúsculos (0, 1, 2);
  - **Run-Length Encoding (RLE)**: Guarda `"Sul" x 50.000 vezes` em apenas 2 bytes!
  - **Bit Packing**: Reduz o tamanho de inteiros na granularidade de bits.
- **Resultado Prático**: **1 GB de CSV vira tipicamente entre 100 MB e 200 MB** de Parquet (redução de até 85% do espaço em disco).

#### 3. Pulo de Blocos por Estatísticas (*Predicate Pushdown*)
O arquivo Parquet é organizado internamente em blocos chamados **Row Groups** (normalmente 128 MB cada). No rodapé do arquivo (*File Footer*), o Parquet guarda os valores **MÍNIMO** e **MÁXIMO** de cada coluna naquele bloco.

Se sua consulta tiver o filtro `WHERE data_venda >= '2026-08-01'` e o Row Group 1 contiver dados de `2026-01-01` a `2026-03-31`, o motor **simplesmente pula o bloco inteiro sem ler um único byte**!

---

## 🔬 3. Anatomia Interna de um Arquivo Parquet

```
┌───────────────────────────────────────────────────────────┐
│                      ARQUIVO PARQUET                      │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ ROW GROUP 1 (~100.000 a 1.000.000 linhas)           │  │
│  │  - Column Chunk: id_venda (Pages de dados + dict)   │  │
│  │  - Column Chunk: produto                           │  │
│  │  - Column Chunk: receita                           │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ ROW GROUP 2                                         │  │
│  │  - Column Chunk: id_venda                           │  │
│  │  - Column Chunk: produto                           │  │
│  │  - Column Chunk: receita                           │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ FILE FOOTER (Metadados do Arquivo)                  │  │
│  │  - Schema Completo (tipos primitivos e nulos)       │  │
│  │  - Estatísticas por Row Group (Min, Max, NullCount) │  │
│  │  - Ponteiros de início de cada coluna               │  │
│  └─────────────────────────────────────────────────────┘  │
│  MAGIC NUMBER: "PAR1" (4 bytes no início e no final)      │
└───────────────────────────────────────────────────────────┘
```

---

## 📊 4. Matriz Comparativa: Parquet vs. CSV vs. Avro vs. ORC

| Formato | Orientação | Compressão | Schema | Ponto Forte Principal | Melhor Caso de Uso |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CSV / JSON** | Linha | Muito fraca | Inexistente (texto) | Legível para humanos | Exportações pontuais e amostras |
| **Apache Parquet** | **Colunar** | **Excelente (Snappy/ZSTD)** | **Embutido e tipado** | **Leitura analítica seletiva e OLAP** | **Data Lakehouses, Spark, DuckDB, Hop** |
| **Apache Avro** | Linha | Média | JSON Schema evolutivo | Gravação rápida linha-a-linha | **Apache Kafka e Mensageria Streaming** |
| **Apache ORC** | Colunar | Excelente | Embutido | Otimizado para Apache Hive | Clusters legados do Hadoop/Hive |

> 🎯 **Regra Prática**:
> - Streaming de mensagens em tempo real no Kafka $\rightarrow$ **Avro**
> - Armazenamento analítico no Data Lake / Lakehouse $\rightarrow$ **Parquet**
> - Leitura e escrita no Apache Hop $\rightarrow$ Suporta **Parquet nativamente**
