# Guia de Classificação, Tags e Categorização de Dados
## Módulo 3: Governança de Dados com OpenMetadata — Aula 02

---

## 1. O que é uma Classification e uma Tag no OpenMetadata?

No OpenMetadata:
- **Classification** é o **agrupador conceitual** ou taxonomia (ex: `Camada`, `Dominio`, `Certificacao`, `PII`).
- **Tag** é o **rótulo individual** aplicável a tabelas e colunas (ex: `Camada.Gold`, `Dominio.Vendas`, `Certificacao.Deprecado`).

As classificações podem ser configuradas como:
- **Mutuamente Exclusivas:** Uma tabela só pode receber uma tag daquele grupo (ex: uma tabela é ou `Bronze`, ou `Silver`, ou `Gold`).
- **Múltiplas:** Uma tabela pode pertencer a múltiplos domínios ou níveis de sensibilidade simultaneamente.

---

## 2. A Distinção Fundamental: Tag vs. Termo de Glossário

Esta é a distinção que mais confunde engenheiros de dados e analistas no início da jornada de governança:

| Dimensão | Tag (Classificação Técnica / Operacional) | Termo de Glossário (Conceito de Negócio) |
| :--- | :--- | :--- |
| **Natureza** | Rótulo curto e sintético de marcação e filtro | Conceito corporativo rico com metodologia e fórmula |
| **Pergunta que Responde** | *"Que tipo de dado é este?"* ou *"Qual a sua maturidade?"* | *"O que significa isto para a tomada de decisão da empresa?"* |
| **Exemplos Práticos** | `Camada.Gold`, `PII.Sensitive`, `Certificacao.Deprecado` | `Ticket Médio`, `Cliente Ativo`, `Margem de Contribuição` |
| **Possui Definição Longa?** | Não (geralmente uma descrição de 1 linha) | **Sim (é a sua essência: as quatro partes da definição)** |
| **Possui Hierarquia Semântica?** | Apenas de classificação (Família $\rightarrow$ Rótulo) | **Sim (Conceitos Pai $\rightarrow$ Filhos, Sinônimos e Relacionados)** |
| **Quem é o Autor?** | Engenharia de Dados e Governança Técnica | **Áreas de Negócio (Comercial, Finanças, Marketing)** |

> **Regra Prática de Ouro (Seção 3 da Apostila):**  
> - Se você aplicaria o rótulo a dezenas de colunas em 2 segundos sem pensar, **é TAG**.  
> - Se precisou de uma reunião com três diretores para definir o que a palavra significa, **é TERMO DE GLOSSÁRIO**.

---

## 3. O Poder da Tag `Certificacao.Deprecado`

Uma das lições mais importantes de engenharia de dados: **nunca apague uma tabela que outros departamentos possam estar usando em produção**.

Quando uma nova tabela `gold.fato_vendas_v2` for construída para substituir a versão antiga:
1. Apagar a tabela antiga quebra dashboards silenciosamente e gera chamados urgentes.
2. Manter a tabela antiga sem aviso faz analistas continuarem consultando números desatualizados.
3. **A Solução de Governança:** Aplicar a tag `Certificacao.Deprecado` no catálogo.
   - O OpenMetadata exibe um alerta visual proeminente em vermelho.
   - Qualquer analista que pesquisar a tabela no catálogo saberá na hora que ela está obsoleta e verá o link para o novo ativo oficial.
