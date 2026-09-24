# 01 — Os Quatro Pilares da Governança de Dados
## Módulo 3: Governança de Dados com OpenMetadata — Aula 01

---

## 1. O que é Governança de Dados?

> **Definição Essencial:**  
> Governança de dados é o conjunto articulado de **pessoas, processos e tecnologias** que garante que os ativos de dados de uma organização sejam **encontráveis, compreensíveis, confiáveis e usados em estrita conformidade com a legislação**.

A governança não é uma barreira burocrática; ela é o diferencial competitivo entre um analista levar **5 minutos** ou gastar **3 dias** para responder a perguntas elementares como *"qual foi a receita do trimestre?"*.

### O Fenômeno do *Data Swamp* (Pântano de Dados)
Sem governança, um *Data Lake* inevitavelmente degenera em um *Data Swamp*:
- Milhares de tabelas criadas sem donos, sem descrição e sem regras de expiração;
- Pipelines órfãos que consomem processamento sem que ninguém saiba se o resultado ainda é utilizado;
- Três relatórios executivos apresentando três faturamentos distintos para o mesmo mês fiscal, minando a credibilidade de toda a equipe de dados.

Governança **não é sobre ter mais dados; é sobre garantir uma Única Versão Confiável da Verdade (Single Source of Truth)**.

---

## 2. A Matriz dos Quatro Pilares Operacionais

A governança corporativa moderna se sustenta sobre quatro pilares fundamentais, cada qual respondendo a uma indagação crítica do negócio:

| Pilar | Pergunta que Responde | Sintoma da Ausência | Como Aparece no Módulo 3 (OpenMetadata) |
| :--- | :--- | :--- | :--- |
| 🔍 **Descoberta** | *Que dados existem e onde estão armazenados?* | Analistas passam dias perguntando no Slack onde está a tabela certa ou recriam pipelines duplicados. | **Catálogo de Dados e Busca Semântica** (Aulas 1 e 2). Indexação elástica de serviços, schemas, tabelas e colunas. |
| 📖 **Entendimento** | *O que este campo significa exatamente?* | Dúvidas recorrentes sobre cálculos (ex: se "margem" desconta imposto) e uso indevido de campos em relatórios de diretoria. | **Documentação Formal, Dicionários e Glossário de Negócios** (Aulas 1 e 2). Definição explícita de granularidade, donos e regras. |
| 🛡️ **Confiança** | *Posso acreditar neste número? De onde ele veio?* | Desconfiança generalizada nos números; erros em produção descobertos apenas pelo cliente final. | **Linhagem Ponta a Ponta e Testes de Qualidade de Dados** (Aula 3). Rastreabilidade de transformações e alertas de anomalias. |
| ⚖️ **Conformidade** | *Tenho autorização legal para usar este dado?* | Risco iminente de multas gravíssimas da ANPD por violação da LGPD e vazamento de dados sensíveis. | **Tags PII, Políticas de Acesso e Anonimização** (Aula 4). Governança de privacidade e auditoria de consumo. |

---

## 3. Aplicação Prática no Acervo do E-commerce

Ao término do Módulo 2, construímos pipelines complexos conectando cinco fontes de dados e distribuindo registros entre camadas Staging, Silver e Gold. No entanto, o código SQL por si só é incapaz de responder a questões fundamentais de governança:

1. **Margem de Lucro (`fato_vendas`):**  
   - *Sem Governança:* O analista precisa inspecionar 200 linhas de código SQL ou Python para descobrir se o campo desconta tributos.  
   - *Com Governança:* O catálogo documenta formalmente: *"Margem de contribuição líquida calculada como `valor_liquido - custo_produto - impostos`, deduzindo 18% de alíquota tributária (ICMS/PIS/COFINS) e o custo de reposição CMV."*

2. **Campo `regiao` (`dim_cliente` vs entrega):**  
   - *Sem Governança:* O cientista de dados não sabe se o cliente foi classificado pela residência fiscal ou pelo destino de um frete temporário.  
   - *Com Governança:* O catálogo estipula que a procedência é exclusivamente o cadastro fixo de `silver.clientes`.

3. **Impacto de Dependência (Blast Radius):**  
   - *Sem Governança:* Ao refatorar `dim_cliente`, o engenheiro derruba sem aviso 3 dashboards executivos de vendas regionais.  
   - *Com Governança:* A linhagem do OpenMetadata aponta graficamente quais ativos a jusante (*downstream*) dependem daquela entidade antes de qualquer modificação.
