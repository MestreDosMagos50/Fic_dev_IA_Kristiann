# 02 — Tags vs. Termos de Glossário: A Distinção que Confunde Todo Mundo
## Módulo 3: Governança de Dados com OpenMetadata — Aula 02

---

## 1. Por que Existe essa Diferenciação?

Tanto tags quanto termos de glossário aparecem como "etiquetas" que você pode colar em uma tabela ou coluna na interface do OpenMetadata. Por causa dessa semelhança visual, muitos iniciantes acreditam que são a mesma coisa.

No entanto, em governança de dados corporativa, **eles desempenham funções diametralmente opostas**:
- **Tag é Classificação Operacional e Técnica:** Serve para agrupar, filtrar e controlar segurança em escala.
- **Termo de Glossário é Semântica de Negócio:** Serve para dar significado formal, documentar regras matemáticas e eliminar ambiguidades conceituais.

---

## 2. A Tabela Comparativa Definitiva (Seção 3 da Apostila)

| Critério | Tag | Termo de Glossário |
| :--- | :--- | :--- |
| **Natureza** | Rótulo curto de classificação e categorização | Conceito de negócio rico com definição e regras |
| **Pergunta que Responde** | *"Que tipo de dado é este?"* ou *"Qual o seu estágio?"* | *"O que este conceito significa para a empresa?"* |
| **Exemplo no Projeto** | `Camada.Gold`, `PII.Sensitive`, `Certificacao.Certificado` | `Ticket Médio`, `Cliente Ativo`, `Margem de Contribuição` |
| **Tem definição longa?** | Não (geralmente uma descrição genérica de 1 linha) | **Sim — a definição detalhada é a sua própria essência** |
| **Tem hierarquia?** | Hierarquia rasa (apenas dentro da própria Classificação) | **Sim — hierarquia semântica rica (Termos Pai e Filhos)** |
| **Quem cria e mantém?** | Engenharia de Dados, Segurança e Governança Técnica | **Áreas de Negócio (Comercial/Finanças) com Governança** |

---

## 3. A Regra Prática de Decisão

```
                                  [ Preciso categorizar um dado ]
                                                 │
                                                 ▼
                             ┌───────────────────────────────────────┐
                             │ Aplicaria este rótulo a dezenas de    │
                             │ tabelas/colunas em segundos sem pensar│
                             │ e sem precisar discutir o significado?│
                             └───────────────────┬───────────────────┘
                                                 │
                                 ┌───────────────┴───────────────┐
                                 │ SIM                           │ NÃO
                                 ▼                               ▼
                      ┌───────────────────────┐       ┌───────────────────────┐
                      │        É TAG          │       │  É TERMO DE GLOSSÁRIO │
                      │  (Ex: Gold, Silver,   │       │(Ex: Ticket Médio,     │
                      │   PII, Certificado)   │       │ Cliente Ativo, Margem)│
                      └───────────────────────┘       └───────────────────────┘
```

> **Exemplo Clássico:**  
> - Se você quer marcar que uma tabela pertence à camada analítica definitiva, você cria e aplica a tag `Camada.Gold`.  
> - Se você precisa explicar que a coluna `valor_liquido` daquela tabela representa o faturamento deduzindo cupom promocional e que os pedidos cancelados não entram na conta, você cria e vincula o termo de glossário `Receita Líquida`.
