# Aula 12 — Storytelling com Dados, SQL Lab e Funcionalidades Avançadas

Material prático e teórico completo da **Aula 12 de Engenharia de Dados**.

---

## 🎯 Objetivos e Conteúdo da Aula

1. **Storytelling com Dados**:
   - Transformar análises e visualizações em narrativas de impacto.
   - Os 4 passos fundamentais: **Contexto & Problema**, **Exploração & Visualização**, **Insight Principal** e **Chamada para Ação (Call to Action)**.
   - Estruturação narrativa: Início (Cenário), Meio (Desenvolvimento) e Fim (Recomendação estratégica).

2. **SQL Lab no Apache Superset**:
   - Exploração de esquemas, tabelas e tipagem de dados sem ferramentas externas.
   - Criação de Datasets a partir de consultas SQL com agregações, joins e filtros.
   - Histórico de execuções para rastreabilidade analítica.

3. **Funcionalidades Avançadas do Superset**:
   - **Alertas & Relatórios (Alerts & Reports)**: Disparos automáticos baseados em limites de métricas de negócio.
   - **Row-Level Security (RLS)**: Governança e isolamento de linhas de dados por papel/perfil de usuário.
   - **Mecanismos de Cache**: Otimização de performance com Redis e retenção de queries.
   - **Plugins & Extensibilidade**: Ampliação das capacidades gráficas da plataforma.

4. **Atividade Extra (Projeto Integrado)**:
   - Nuvem de Palavras sobre tecnologia atualizada dinamicamente a cada 5 minutos no Apache Superset.

---

## 📂 Organização dos Arquivos da Aula

### 🔹 Módulos e Scripts Práticos (Raiz)
- [01_preparar_dados_vendas_detalhe.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/01_preparar_dados_vendas_detalhe.sql): Script DDL e carga de dados para a tabela `vendas_detalhe` e `produtos_master`.
- [02_dataset_faturamento_diario.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/02_dataset_faturamento_diario.sql): Consulta de agregação do faturamento diário por região para criação de Dataset no SQL Lab.
- [03_configuracao_alerta_faturamento.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/03_configuracao_alerta_faturamento.sql): Especificação e regras do alerta de faturamento baixo no Sudeste.
- [04_exercicio_joins_produtos.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/04_exercicio_joins_produtos.sql): Consulta prática unindo `vendas_detalhe` com `produtos_master` (Exercício 4.4.4 - Item 2).
- [05_exercicio_rls_filtros.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/05_exercicio_rls_filtros.sql): Regras e filtros SQL para Row-Level Security (Exercício 4.4.4 - Item 3).
- [06_exercicio_alerta_ticket_medio.sql](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/06_exercicio_alerta_ticket_medio.sql): Métrica e condição para monitoramento do Ticket Médio crítico (Exercício 4.4.4 - Item 4).
- [07_executar_setup_postgres.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/07_executar_setup_postgres.py): Script de automação para popular os dados no banco PostgreSQL com um único comando.

### 🔹 Projeto da Atividade Extra (`atividade_extra_nuvem_palavras/` e `mini_lab/`)
Subpasta com a implementação completa da **Nuvem de Palavras Tech** com backend coletor, worker com ciclo de 5 minutos, frontend interativo e scripts para o Superset.
Consulte o [README.md do Desafio Extra](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/atividade_extra_nuvem_palavras/README.md) para detalhes completos de execução.
