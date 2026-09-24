# 03 — Apache Flink e o Streaming Verdadeiro: Baixa Latência em Escala

> *"Se o Spark nasceu para processar lotes massivos e adaptou-se para streaming como uma sequência de pequenos lotes (micro-batches), o Apache Flink foi desenhado desde o primeiro dia como uma engine de streaming verdadeiro evento-a-evento."*

---

## ⚡ 1. Micro-Lotes (Spark) vs. Streaming Verdadeiro (Flink)

| Dimensão | Apache Spark (Structured Streaming) | Apache Flink |
| :--- | :--- | :--- |
| **Modelo Conceitual** | Micro-lotes (*Micro-batching*) | Evento a Evento (*Continuous Streaming*) |
| **Latência Típica** | 100 milissegundos a vários segundos | **1 a 10 milissegundos** (tempo real estrito) |
| **Throughput** | Altíssimo para lotes pesados | Altíssimo mantendo latência microscópica |
| **Tratamento de Lote** | Lote é o cidadão de primeira classe | Lote é visto como um stream finito de dados |
| **Caso de Uso Ideal** | Dashboards periódicos, ETL contínuo de 5 min | **Detecção de fraude em milissegundos**, IoT crítico |

```
SPARK STREAMING (Micro-lote):
Eventos chegam ──> [ Espera 2 segundos acumular ] ──> [ Processa Lote 1 ] ──> Saída

FLINK (Streaming Verdadeiro):
Evento 1 ──> [ Processa Imediatamente ] ──> Saída (1 ms)
Evento 2 ──> [ Processa Imediatamente ] ──> Saída (1 ms)
```

---

## 🪟 2. O Conceito Fundamental de Janelas de Tempo (Windows)

Em um stream sem fim (*unbounded data*), não existe "final de arquivo". Para calcular agregações (médias, contagens, somas), agrupamos eventos em **Janelas de Tempo**:

```
1. JANELAS TUMBLING (Fixas / Não Sobrepostas):
   Janela 1 (00:00 - 00:05)   Janela 2 (00:05 - 00:10)
   [ e1, e2, e3 ]             [ e4, e5, e6 ]

2. JANELAS SLIDING (Deslizantes / Com Sobreposição):
   Janela 1 (Duração 10 min, desliza a cada 5 min):
   [ e1, e2, e3, e4 ]
          Janela 2 (Duração 10 min):
          [ e3, e4, e5, e6 ]

3. JANELAS SESSION (Por Inatividade):
   [ e1, e2, e3 ] ──(Silêncio de 15 min)──> [ e4, e5 ]
   (Sessão de Usuário 1)                    (Sessão de Usuário 2)
```

1. **Tumbling Window (Fixa)**: Janelas consecutivas e contíguas de tamanho fixo (ex: faturamento a cada 5 minutos exatos).
2. **Sliding Window (Deslizante)**: Possuem tamanho fixo, mas avançam em um intervalo menor que o tamanho da janela (ex: média de requisições dos últimos 10 minutos, recalculada a cada 1 minuto).
3. **Session Window (Sessão)**: Agrupam eventos separados por um intervalo de inatividade (*gap*). Ideal para navegação de e-commerce (se o usuário parar por 30 minutos, a sessão é fechada).

---

## ⏰ 3. Event Time vs. Processing Time e os Watermarks

No mundo real de redes móveis e sensores, **a ordem de chegada no servidor não é a ordem em que o evento ocorreu**!

- **Event Time (Tempo do Evento)**: O timestamp gravado no dispositivo no exato momento da transação (ex: 14:02:00).
- **Processing Time (Tempo de Processamento)**: O relógio da máquina do cluster no momento em que a mensagem é processada (ex: 14:02:15, devido a lag na rede 4G).
- **Watermarks (Marcadores de Água)**: Mecanismo engenhoso do Flink para dizer à janela: *"Considere que todos os eventos até o timestamp T já chegaram; pode fechar a janela e emitir o resultado"*.

```
Dispositivo IoT       Rede Móvel (Lag)       Cluster Flink (Event Time Window 14:00 - 14:05)
(14:01:00) ────────── [ Rápido ] ─────────> Entra na janela 14:00 - 14:05
(14:03:00) ────────── [ Atrasou 4 min ] ──> Chega às 14:07:00, mas o Watermark
                                           reconhece que pertence à janela 14:00 - 14:05!
```

---

## 💾 4. Estado (State) e Tolerância a Falhas com Checkpoints

Pipelines de streaming precisam se lembrar de informações do passado (ex: *"quantas compras o cliente X fez na última hora?"*). Isso é chamado de **Stateful Processing**.

Se um servidor cai, como não perder esse estado?
- O Flink implementa uma variação do algoritmo distribuído **Chandy-Lamport**;
- Periodicamente (ex: a cada 500 ms), o Flink insere **barreiras de checkpoint** no fluxo de dados;
- Quando todos os nós processam a barreira, o estado exato é persistido de forma assíncrona em armazenamento durável (Amazon S3, HDFS ou MinIO);
- Se um nó queimar, o Flink reinicia o pipeline exatamente do último checkpoint aprovado, garantindo semântica **Exactly-Once** (exatamente uma vez)!

---

## 🏛️ 5. Padrão Arquitetural de Mercado: Kafka + Flink + Lakehouse

O ecossistema corporativo de streaming moderno converge para a seguinte topologia padrão:

```
[ Produtores ] ──> [ Apache KAFKA ] ──> [ Apache FLINK ] ──┬──> [ Alertas em Tempo Real ]
- Cliques Web       (Buffer durável       (Processamento      │    (Detecção de Fraude)
- Apps Mobile        distribuído)          contínuo e         │
- Microsserviços                           janelas)           └──> [ Lakehouse / Parquet ]
                                                                   (Delta Lake / Iceberg)
```

1. **Kafka (O Broker)**: Desacopla produtores de consumidores, absorve picos brutais de tráfego (*backpressure*) e retém o log de eventos para permitir reprocessamento histórico.
2. **Flink (O Motor Analítico)**: Consome as mensagens do Kafka, avalia regras de fraude em milissegundos e enriquece os dados com estado.
3. **Destinos**: Emite alertas instantâneos para APIs de checkout e grava os eventos limpos em arquivos colunares Parquet no Data Lakehouse.
