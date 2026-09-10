# Pipeline Inteligente de Triagem e Roteamento de Demandas da Ouvidoria Municipal

Este projeto simula um pipeline de dados para uma ouvidoria municipal (Central 156 / Fala.BR).

## Problema
Todos os dias, secretarias e ouvidorias públicas recebem milhares de manifestações (reclamações, solicitações e elogios) em texto livre dos cidadãos. Grande parte do tempo dos servidores é desperdiçada em triagem manual.

## Solução
Um pipeline em Python e PostgreSQL que:
1. Armazena as competências das secretarias (com embeddings).
2. Ingere relatos brutos em formato JSON (JSONB).
3. Processa e classifica a prioridade (baseado em palavras-chave e severidade).
4. Realiza roteamento semântico (usando `pgvector`) para recomendar a secretaria mais adequada para o chamado.

## Estrutura
- `schema_governo.sql`: Scripts para criar as tabelas do banco de dados PostgreSQL.
- `servicos_municipais.csv`: Dados das secretarias e seus serviços.
- `manifestacoes_cidadao.json`: Exemplos de chamados reais da população.
- `pipeline_ouvidoria.py`: O script Python que faz a ingestão, processamento e simula os embeddings para o roteamento.
- `01_roteamento_semantico.sql`: Exemplo de query de similaridade vetorial via SQL.
- `02_mapa_demandas.sql`: Exemplo de query para um gestor monitorar demandas críticas por bairro e secretaria.
- `requirements.txt`: Dependências do Python.

## Como Executar

1. Crie o banco de dados e instale a extensão `pgvector`.
2. Execute o arquivo `schema_governo.sql` no banco de dados.
3. Configure as credenciais no arquivo `pipeline_ouvidoria.py` (ou crie um arquivo `.env`).
4. Crie um ambiente virtual e instale as dependências:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. Execute o script principal:
   ```bash
   python pipeline_ouvidoria.py
   ```
6. Conecte-se ao banco de dados e verifique os dados gravados, ou execute as queries de consultas (SQL).
