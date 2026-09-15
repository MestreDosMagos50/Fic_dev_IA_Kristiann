# Atividade Extra — Nuvem de Palavras sobre Tecnologia com Apache Superset

Este projeto implementa a **Atividade Extra da Aula 12**:
> *"Crie uma nuvem de palavras sobre o tema tecnologia e apresente no Apache Superset, esta nuvem de palavras deve ser atualizada automaticamente a cada 5 minutos."*

---

## 🏗️ Arquitetura e Funcionamento

O projeto é composto por 3 camadas integradas:

1. **Ingestão & Coletor Periódico (`backend/`)**:
   - `collector.py`: Coleta termos tecnológicos atuais e tópicos em alta de taxonomias e APIs tech (IA, LLMs, Engenharia de Dados, Superset, Docker, Cloud, Python, etc.), aplicando pesos dinâmicos e variações a cada ciclo.
   - `database.py`: Conecta-se ao banco PostgreSQL (`superset_data`), gerenciando a tabela `nuvem_palavras_tech`.
   - `worker.py`: Serviço agendador que executa a cada 5 minutos (`UPDATE_INTERVAL_SECONDS=300`), populando novos termos e frequências.
   - `setup_superset.py`: Script de automação que registra o Dataset, gera o gráfico **Word Cloud** e cria o Dashboard no Superset com auto-refresh de 5 minutos.

2. **Visualização no Apache Superset**:
   - **Dataset:** Consulta SQL agregada sobre `nuvem_palavras_tech` filtrando coletas recentes (`WHERE data_atualizacao >= NOW() - INTERVAL '30 minutes'`).
   - **Chart:** Tipo **Word Cloud** com dimensão `palavra` e métrica `SUM(frequencia)`.
   - **Dashboard:** Configurado com **Auto-refresh a cada 5 minutos (300 segundos)** nativo do Superset.

3. **Frontend Interativo do Cliente (`frontend/`)**:
   - Interface web dark mode com visualização interativa da nuvem de palavras, temporizador regressivo de 5 minutos, filtros por categoria de tecnologia, métricas ao vivo e pré-visualização embarcada do Superset via iframe.

---

## 📁 Estrutura de Pastas

```text
atividade_extra_nuvem_palavras/
├── .env.example              # Modelo de variáveis de ambiente
├── .env                      # Configuração com credenciais do PostgreSQL
├── .gitignore                # Regras de exclusão do Git
├── README.md                 # Documentação detalhada
├── requirements.txt          # Dependências Python
├── backend/
│   ├── collector.py          # Coletor e ponderador de termos tech
│   ├── database.py           # Camada de persistência PostgreSQL
│   ├── setup_superset.py     # Provisionamento automático no Superset
│   └── worker.py             # Daemon agendador (ciclo de 5 minutos)
├── frontend/
│   ├── app.js                # Lógica interativa e temporizador de 5min
│   ├── index.html            # Portal web da aplicação
│   └── style.css             # Design moderno com glassmorphism
└── scripts/
    ├── init_db.sql           # DDL da tabela nuvem_palavras_tech
    └── run_pipeline.sh       # Script de execução rápida
```

---

## 🚀 Como Executar o Projeto

### 1. Criar o Ambiente Virtual e Instalar as Dependências

No terminal, navegue até a pasta do projeto e crie o ambiente virtual Python:

```bash
cd /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-12-storytelling-sql-lab-funcionalidades-avancadas/atividade_extra_nuvem_palavras

# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Instalar as dependências
pip install -r requirements.txt
```

---

### 2. Inicializar a Tabela no PostgreSQL

Garanta que o contêiner do PostgreSQL e do Superset estejam em execução. Em seguida, popule a tabela executando o script SQL ou via Python:

```bash
# Opção A: Executar via psql ou docker exec
docker exec -i data_postgres psql -U superset_user -d superset_data < scripts/init_db.sql

# Opção B: Executar via script Python
python3 -c "from backend.database import init_tables; init_tables()"
```

---

### 3. Iniciar o Worker de Atualização Contínua (a cada 5 minutos)

Inicie o worker para manter os termos e frequências sempre atualizados no banco a cada 5 minutos:

```bash
python3 backend/worker.py
```

*O worker executará uma rodada imediatamente e programará as próximas rodadas a cada 300 segundos.*

---

### 4. Configurar no Apache Superset

#### Método Rápido (Automático):
Execute o script de automação:
```bash
python3 backend/setup_superset.py
```

#### Método Manual (Passo a Passo via Interface do Superset):
1. Acesse o Apache Superset em: [http://localhost:8088](http://localhost:8088)
2. Vá em **SQL Lab** -> **SQL Editor**.
3. Selecione o banco de dados `superset_data` (ou `PostgreSQL`) e schema `public`.
4. Cole a seguinte consulta agregada:
   ```sql
   SELECT
       palavra,
       categoria,
       SUM(frequencia) AS frequencia_total
   FROM nuvem_palavras_tech
   WHERE data_atualizacao >= CURRENT_TIMESTAMP - INTERVAL '30 minutes'
   GROUP BY palavra, categoria
   ORDER BY frequencia_total DESC;
   ```
5. Clique em **RUN** e em seguida **Save As** -> **Save as Dataset** com o nome `Nuvem de Palavras Tech`.
6. Clique em **Save & Explore**:
   - **Visualization Type:** `Word Cloud`
   - **Series:** `palavra`
   - **Metric:** `SUM(frequencia_total)`
   - Clique em **Create Chart** e salve como `Word Cloud Tecnologias`.
7. Adicione o gráfico ao seu Dashboard.
8. No canto superior direito do Dashboard, clique em **... -> Edit Dashboard**:
   - Clique na engrenagem ou menu de opções -> **Settings**.
   - Defina o campo **Auto-refresh** para: **5 minutes**.
   - Salve o Dashboard!

---

### 5. Abrir a Interface Web do Cliente (Frontend)

Para visualizar a nuvem interativa, temporizador regressivo e dashboard integrado, basta abrir o arquivo `frontend/index.html` em qualquer navegador:

```bash
# Abrir diretamente no navegador (se tiver xdg-open)
xdg-open frontend/index.html

# Ou servir via servidor HTTP simples do Python:
cd frontend
python3 -m http.server 3000
# Acesse no navegador: http://localhost:3000
```
