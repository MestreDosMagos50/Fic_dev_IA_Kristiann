# Aula 01 — Conceitos de ETL e ELT: do Python à Ferramenta

Material didático completo, scripts conceituais e projeto prático da **Aula 01 (Módulo 2: ETL/ELT com Apache Hop) de FIC Engenharia de Dados**.

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula, o aluno é capaz de:
- **Explicar as etapas do ETL** (*Extract, Transform, Load*) e do **ELT** (*Extract, Load, Transform*);
- **Associar o ETL ao Business Intelligence tradicional**, no qual todos os dados analisados passam pelo pipeline de transformação antes da carga (*schema-on-write*);
- **Associar o ELT ao contexto Big Data**, em que os dados são carregados brutos e apenas a fatia de interesse é transformada sob demanda (*schema-on-read*);
- **Diferenciar schema-on-write de schema-on-read**;
- **Definir staging area, carga incremental vs completa e idempotência**;
- **Implementar um pipeline ETL completo em Python** com pandas e SQLAlchemy, incluindo quarentena de registros inválidos;
- **Apontar as limitações de um ETL artesanal** que justificam ferramentas dedicadas como o Apache Hop.

---

## 📂 Organização dos Arquivos da Aula

### 🔹 Módulos e Scripts Práticos (Raiz da Aula)
- [01_padrao_etl.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-01-conceitos-de-etl-e-elt/01_padrao_etl.py): Demonstração didática das etapas sequenciais do ETL clássico, limpeza em memória e carga modelada (*schema-on-write*).
- [02_padrao_elt.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-01-conceitos-de-etl-e-elt/02_padrao_elt.py): Demonstração didática do padrão ELT, carga imediata de dados brutos e transformação delegada ao banco via SQL (*schema-on-read*).
- [03_etl_bi_vs_elt_bigdata.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-01-conceitos-de-etl-e-elt/03_etl_bi_vs_elt_bigdata.py): Matriz comparativa aprofundada, analogia da cozinha (restaurante buffet vs despensa crua) e simulação de custos computacionais.
- [04_staging_incremental_idempotencia.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-01-conceitos-de-etl-e-elt/04_staging_incremental_idempotencia.py): Conceitos operacionais essenciais (Staging Area, Carga Completa vs Incremental com CDC/Timestamp e Idempotência).
- [05_etl_produtos_artesanal.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-01-conceitos-de-etl-e-elt/05_etl_produtos_artesanal.py): Código-fonte completo em Python puro apresentado na Seção 5 da apostila.
- [06_limitacoes_etl_artesanal.py](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-01-conceitos-de-etl-e-elt/06_limitacoes_etl_artesanal.py): Análise dos 5 gargalos operacionais de scripts manuais (agendamento às 3h, quedas no meio da carga, falta de logs, reprocessamento) e introdução à necessidade do Apache Hop.

---

### 🔹 Projeto Integrado: Desafio Extra (`desafio_extra_estendendo_etl_python/` e `desafio_extra/`)

Subpasta contendo o desafio prático de extensão do ETL artesanal em Python, com dados sujos, regras de quarentena, implementação da regra `"preco suspeito"` e correção de idempotência.

Estrutura interna:
```text
desafio_extra/
├── dados/entrada/produtos.csv  # Base com casos de borda e validações
├── python/etl_produtos.py      # Script baseline da aula (Passos 1 e 2)
├── python/etl_produtos_desafio.py # Script estendido com os desafios (Passos 3 e 4)
├── scripts/init_db.sql         # DDL de tabelas e esquemas no PostgreSQL
├── scripts/auditoria_etl.py    # Auditoria da equação de integridade e prova de idempotência
├── scripts/run_pipeline.sh     # Execução automatizada de ponta a ponta
├── .env.example / .env         # Configuração de conexão com o banco
├── requirements.txt            # Dependências do projeto
└── README.md                   # Documentação detalhada e critérios de avaliação
```

Consulte o [README.md do Desafio Extra](file:///home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-01-conceitos-de-etl-e-elt/desafio_extra_estendendo_etl_python/README.md) para detalhes completos.
