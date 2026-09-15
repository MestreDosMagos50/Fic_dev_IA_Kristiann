"""
Módulo Coletor e Processador de Termos de Tecnologia
Responsável por extrair termos tecnológicos atuais, calcular pesos de relevância
e categorizar cada palavra-chave para a nuvem do Apache Superset.
"""

import random
import re
import requests
from datetime import datetime

# Dicionário de termos tecnológicos organizados por categoria
TAXONOMIA_TECH = {
    "IA & Machine Learning": [
        "Inteligência Artificial", "Machine Learning", "Deep Learning", "LLMs",
        "OpenAI", "ChatGPT", "Transformers", "PyTorch", "TensorFlow", "Hugging Face",
        "Visão Computacional", "NLP", "LangChain", "RAG", "Prompt Engineering",
        "Fine-Tuning", "Embeddings", "Agentes Autônomos", "Gemini", "Claude"
    ],
    "Engenharia de Dados": [
        "Apache Superset", "SQL Lab", "Data Warehouse", "Apache Kafka", "Apache Spark",
        "Airflow", "ETL", "ELT", "Data Lake", "Delta Lake", "dbt", "PostgreSQL",
        "Snowflake", "Databricks", "Modelagem Dimensional", "Data Mesh", "Storytelling com Dados",
        "Data Observability", "Parquet", "DuckDB"
    ],
    "Cloud & DevOps": [
        "Docker", "Kubernetes", "AWS", "Google Cloud", "Azure", "Terraform",
        "CI/CD", "GitHub Actions", "Linux", "Microserviços", "Serverless",
        "Observabilidade", "Grafana", "Prometheus", "Helm", "Ansible", "DevOps",
        "Cloud Native", "GitOps", "Containers"
    ],
    "Linguagens & Frameworks": [
        "Python", "JavaScript", "TypeScript", "FastAPI", "React", "Next.js",
        "Go", "Rust", "Node.js", "Django", "Flask", "GraphQL", "REST API",
        "TailwindCSS", "SQL", "Pandas", "NumPy", "C++", "Java", "Kotlin"
    ],
    "Bancos de Dados & Storage": [
        "PostgreSQL", "Redis", "MongoDB", "Elasticsearch", "ChromaDB", "Qdrant",
        "Cassandra", "Neo4j", "MySQL", "DynamoDB", "ClickHouse", "TimescaleDB",
        "Supabase", "Row-Level Security", "Vector Search", "Índices HNSW"
    ]
}

def coletar_noticias_hacker_news(limite=15):
    """
    Tenta consultar títulos de notícias recentes da API pública do Hacker News.
    Caso esteja offline ou indisponível, retorna lista vazia para utilizar o gerador de tendências.
    """
    titulos = []
    try:
        url_top = "https://hacker-news.firebaseio.com/v0/topstories.json"
        resp = requests.get(url_top, timeout=4)
        if resp.status_code == 200:
            top_ids = resp.json()[:limite]
            for item_id in top_ids:
                url_item = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
                r = requests.get(url_item, timeout=2)
                if r.status_code == 200:
                    dados = r.json()
                    if dados and "title" in dados:
                        titulos.append(dados["title"])
    except Exception as e:
        # Modo offline silencioso
        pass
    return titulos

def extrair_termos_com_frequencia():
    """
    Gera uma rodada de termos tecnológicos com pesos de frequência dinâmicos,
    simulando tendências de mercado e integrando termos em destaque a cada 5 minutos.
    """
    resultado = []
    
    # 1. Analisar títulos reais se disponíveis
    titulos_reais = coletar_noticias_hacker_news()
    texto_combinado = " ".join(titulos_reais).lower()
    
    # 2. Sortear e ponderar palavras-chave das categorias
    for categoria, termos in TAXONOMIA_TECH.items():
        # Seleciona de 4 a 8 termos por categoria a cada rodada
        quantidade_selecionar = random.randint(5, min(8, len(termos)))
        termos_selecionados = random.sample(termos, quantidade_selecionar)
        
        for termo in termos_selecionados:
            # Frequência base entre 40 e 95
            peso_base = random.randint(45, 98)
            
            # Bonificação se o termo apareceu em notícias reais
            if termo.lower() in texto_combinado:
                peso_base += random.randint(25, 50)
                
            # Adicionar pequenas variações temporais
            variacao = random.randint(-5, 10)
            frequencia_final = max(20, peso_base + variacao)
            
            resultado.append({
                "palavra": termo,
                "categoria": categoria,
                "frequencia": frequencia_final,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    # Destaque especial para os temas da Aula 12
    temas_aula_12 = [
        ("Storytelling com Dados", "Engenharia de Dados", random.randint(90, 110)),
        ("SQL Lab", "Engenharia de Dados", random.randint(85, 105)),
        ("Apache Superset", "Engenharia de Dados", random.randint(95, 115)),
        ("Row-Level Security", "Bancos de Dados & Storage", random.randint(80, 98)),
        ("Alerts & Reports", "Engenharia de Dados", random.randint(82, 99))
    ]
    for termo, cat, freq in temas_aula_12:
        resultado.append({
            "palavra": termo,
            "categoria": cat,
            "frequencia": freq,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return resultado
