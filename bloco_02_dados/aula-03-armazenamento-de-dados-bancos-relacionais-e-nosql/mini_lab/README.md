# Mini-lab: Explorando JSONB no PostgreSQL e Banco de Documentos (MongoDB)

Este repositório contém o código prático da Aula 03. O roteiro demonstra a criação e consulta de dados semi-estruturados usando `JSONB` no PostgreSQL e as operações básicas de inserção e consulta no MongoDB.

## Arquivos do Projeto

- `01_install_mongodb.sh`: Script em shell com as instruções da apostila para instalar o MongoDB no Ubuntu.
- `02_postgres_jsonb.sql`: Comandos SQL para criar a tabela com coluna JSONB, inserir dados e fazer as consultas do roteiro.
- `03_mongodb_queries.js`: Comandos JavaScript para executar no `mongosh` (shell do MongoDB) para criar banco, coleção, documentos e realizar consultas.

## Como Executar

### 1. PostgreSQL (JSONB)
1. Conecte-se ao seu PostgreSQL no terminal:
   ```bash
   psql -U postgres -d meu_banco_de_dados
   ```
2. Copie e cole os comandos do arquivo `02_postgres_jsonb.sql` ou execute o arquivo:
   ```bash
   psql -U postgres -d meu_banco_de_dados -f 02_postgres_jsonb.sql
   ```

### 2. MongoDB
1. Caso não tenha o MongoDB instalado no seu Ubuntu, execute o script:
   ```bash
   chmod +x 01_install_mongodb.sh
   ./01_install_mongodb.sh
   ```
2. Acesse o shell do MongoDB:
   ```bash
   mongosh
   ```
3. Copie e cole os comandos do arquivo `03_mongodb_queries.js` dentro do terminal interativo sequencialmente.

### 3. Ambiente Virtual (Opcional)
Se você for estender a aula criando scripts Python (ex: para inserir dados via código):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
