# Mini-lab: Ingestão de Dados com Python e PostgreSQL

Este projeto demonstra a ingestão de dados em formatos CSV e JSON para um banco de dados PostgreSQL.

## Configuração do Ambiente

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # no Linux/Mac
   venv\Scripts\activate  # no Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados PostgreSQL local e atualize as credenciais no código (ou use variáveis de ambiente se optar por modificar os scripts baseando-se no `.env.example`).

4. Execute os scripts:
   ```bash
   python ingest_csv.py
   python ingest_json.py
   ```
