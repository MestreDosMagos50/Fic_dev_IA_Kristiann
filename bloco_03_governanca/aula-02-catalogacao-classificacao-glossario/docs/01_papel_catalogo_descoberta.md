# 01 — O Catálogo como Ferramenta de Descoberta e Autosserviço
## Módulo 3: Governança de Dados com OpenMetadata — Aula 02

---

## 1. As Três Perguntas do Autosserviço

Um catálogo de dados moderno e maduro transforma analistas e cientistas de dados em agentes autônomos. Ele responde instantaneamente a três perguntas críticas sem que ninguém precise interromper o time de engenharia:

1. **Existe um dado sobre isso?** (Busca textual semântica com OpenSearch).
2. **Onde ele está armazenado?** (Navegação hierárquica por Serviço, Database, Schema e Tabela).
3. **Posso confiar nele para tomada de decisão?** (Classificação de Camada, Tier de Criticidade, Linhagem e Status de Certificação).

---

## 2. O Teste de Busca (Dica da Página 2 da Apostila)

> *"Antes de criar qualquer coisa, faça o teste de busca: procure por 'vendas' no seu catálogo. Se o resultado não deixa óbvio qual tabela usar, o problema não é da ferramenta — é da documentação. Catálogo bom é o que dispensa o 'pergunta pro fulano'."*

### Como o OpenMetadata Indexa o Acervo:
Quando você digita um termo na barra de busca superior do OpenMetadata, o mecanismo varre múltiplos atributos simultaneamente:
- Nome físico da tabela e schema (`fato_vendas`);
- Descrições ricas da tabela e de cada uma das colunas;
- Tags atribuídas (`Camada.Gold`, `Dominio.Vendas`);
- Termos de glossário vinculados (`Ticket Médio`, `Receita Líquida`);
- Sinônimos configurados nos termos (`AOV`, `Net Sales`).

Essa indexação multidimensional assegura que mesmo que um usuário não conheça o nome técnico da tabela no PostgreSQL, ele encontre os dados buscando pelos conceitos do dia a dia do seu departamento.
