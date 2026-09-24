# 04 — Hierarquia Semântica: Cliente, Cliente Ativo e Inativo
## Módulo 3: Governança de Dados com OpenMetadata — Aula 02

---

## 1. Por que Usar Hierarquias no Glossário?

Na prática corporativa, muitos conceitos de negócio não são isolados; eles formam **árvores conceituais** de generalização e especialização.

O OpenMetadata permite modelar essa relação nativamente através de **Glossary Terms Pais e Filhos** (*Parent & Child Terms*). Quando um usuário consulta o termo pai, ele imediatamente descobre quais são suas variações operacionais.

---

## 2. A Estrutura Semântica de Cliente

```
                       ┌──────────────────────────────┐
                       │        CLIENTE (Pai)         │
                       │                              │
                       │ "Critério de separação: A    │
                       │ distinção entre ativo e      │
                       │ inativo é estritamente       │
                       │ temporal, fixada na janela   │
                       │ de 90 dias da última compra."│
                       └──────────────┬───────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
      ┌───────────────────────┐                 ┌───────────────────────┐
      │  CLIENTE ATIVO (Filho)│                 │CLIENTE INATIVO (Filho)│
      │                       │                 │                       │
      │ Compra entregue nos   │                 │ Sem compras concluídas│
      │ últimos 90 dias       │                 │ há mais de 90 dias    │
      └───────────────────────┘                 └───────────────────────┘
```

---

## 3. Justificativa da Janela Temporal de 90 Dias

A apostila exige no **Passo 2 do Mini-Lab**:
> *"Cliente Ativo (este último exige que você defina a janela temporal — decida e justifique)."*

### Fundamentação Técnica e de Negócio:
1. **Ciclo Médio de Recompra no E-commerce de Tecnologia:**  
   Em empresas de bens de consumo de informática, periféricos e acessórios (como o catálogo do nosso laboratório com notebooks, mouses e cadeiras), o intervalo médio entre pedidos sucessivos de um mesmo cliente situa-se historicamente entre **60 e 75 dias**.
2. **Alinhamento com o Trimestre Fiscal (Q1, Q2, Q3, Q4):**  
   Uma janela de **90 dias** corresponde exatamente a um trimestre contábil, permitindo que os relatórios de retenção e cohort façam comparações diretas com os balanços financeiros da diretoria.
3. **Zona de Ação Proativa contra Churn:**  
   Se adotássemos 180 ou 365 dias, o cliente já teria esfriado completamente e buscado a concorrência. Se adotássemos 30 dias, classificaríamos falsamente clientes normais como "inativos". A janela de 90 dias atinge o ponto ideal de equilíbrio para disparar réguas automatizadas de reengajamento de CRM.

---

## 4. Rastreabilidade com os Dados Físicos

- **Termo Pai `Cliente`:** Vinculado à tabela inteira `gold.dim_cliente`.
- **Termos Filhos `Cliente Ativo` e `Cliente Inativo`:** Vinculados à coluna `status_cliente` da mesma dimensão.
- **Resultado:** Qualquer analista que abrir a coluna `status_cliente` verá os termos associados com as definições precisas de quantos dias separam uma situação da outra.
