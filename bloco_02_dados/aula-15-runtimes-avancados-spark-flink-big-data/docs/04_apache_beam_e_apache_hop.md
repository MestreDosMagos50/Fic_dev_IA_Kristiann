# 04 — Apache Beam e Apache Hop: Escreva uma Vez, Execute em Qualquer Lugar

> *"A maior dor da engenharia de dados histórica era reescrever pipelines inteiros quando a empresa decidia migrar de uma máquina local para Spark, ou de Spark para Flink. O Apache Beam e o Apache Hop resolveram isso separando o desenho do pipeline do seu motor de execução."*

---

## 🌐 1. O Que É o Apache Beam?

O **Apache Beam** (abreviação de *Batch + strEAM*) é um modelo de programação unificado de código aberto para definir e executar fluxos de processamento de dados em paralelo:
- Você escreve seu pipeline usando abstrações agnósticas de motor;
- O Beam utiliza **Runners** (adaptadores) para traduzir seu pipeline para o motor físico de sua escolha: **Apache Spark**, **Apache Flink**, **Google Cloud Dataflow** ou o próprio **Direct Runner** local.

---

## 🤝 2. A Jogada Arquitetural do Apache Hop

O **Apache Hop** adota o modelo do Apache Beam no coração de sua arquitetura. Isso significa que um pipeline visual desenhado como `.hpl` não está acoplado ao motor monocelular da JVM local!

```
                    ┌────────────────────────────┐
                    │    PIPELINE APACHE HOP     │
                    │   (meu_pipeline.hpl)       │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │   CAMADA APACHE BEAM       │
                    │  (Abstração de Pipeline)   │
                    └─────────────┬──────────────┘
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│ BEAM DIRECT  │            │  BEAM SPARK  │            │  BEAM FLINK  │
│ Teste local  │            │ Lote massivo │            │ Streaming de │
│ sem cluster  │            │  em cluster  │            │baixa latência│
└──────────────┘            └──────────────┘            └──────────────┘
```

---

## ⚙️ 3. Os Quatro Runtimes no Apache Hop

Basta trocar o parâmetro na **Pipeline Run Configuration** para que o mesmo `.hpl` seja compilado para o motor adequado:

| Runtime | Quando Usar | Vantagens |
| :--- | :--- | :--- |
| **Local (Nativo Hop)** | Desenvolvimento diário e volumes pequenos/médios | Inicialização instantânea, depuração visual rica no Hop GUI |
| **Beam Direct** | Validação local do modelo Beam | Garante que os transforms são compatíveis com Beam antes de enviar ao cluster |
| **Beam Spark** | Lotes massivos (TB/PB) em cluster distribuído | Escala horizontal em infraestrutura Spark (EMR, Databricks, On-premise) |
| **Beam Flink** | Ingestão contínua e streaming com janelas | Baixa latência e processamento evento a evento |

---

## ⚠️ 4. Dica Crítica de Produção: Nem Todo Transform é Suportado no Beam

O motor nativo do Hop possui mais de 100 transforms específicos. Porém, o Apache Beam impõe um modelo estrito de transformações puras e particionáveis.
- **Transforms universais suportados no Beam**:
  - `Beam Input` / `Beam Output`
  - `Filter Rows`
  - `Select Values`
  - `Switch / Case`
  - `Stream Value Mapper`
  - `Parquet File Input` / `Parquet File Output`
  - `Memory Group By` / Agregações compatíveis
- **Transforms complexos acoplados à JVM local**:
  - Scripts Java arbitrários não serializáveis;
  - Operações com dependência de estado local sequencial não distribuível.

> 💡 **Regra de Ouro do Handout**:
> *"Todo o conhecimento da semana escala sem redesenho: o pipeline de padronização pode rodar no Spark trocando só a configuração de execução. Nem todo transform é suportado no Beam — **valide com o Beam Direct antes de ir ao cluster**."*

---

## 🚀 5. Como Configurar no Hop

Na pasta de metadados do projeto Hop (`metadata/pipeline-run-configuration/`), cada runtime é definido como um arquivo JSON declarando seu *engineRunConfiguration*. 

Por exemplo, ao executar via CLI:
```bash
hop-run.sh -j ecommerce -f hop/pipelines/converte_parquet.hpl -r spark-local
```
O Hop converte a topologia dos nós em um job Spark e envia as tarefas para os núcleos do processador ou nós do cluster!
