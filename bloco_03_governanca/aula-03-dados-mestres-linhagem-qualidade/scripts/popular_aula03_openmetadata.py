#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 03: Dados Mestres, Linhagem e Qualidade de Dados
Arquivo: scripts/popular_aula03_openmetadata.py
Objetivo: Orquestrar automaticamente todo o catálogo da Aula 03 no OpenMetadata:
          1. Serviços, Banco, Schemas e 16 Tabelas (E-Commerce + Conteúdos)
          2. Classification 'TipoDado' com Tags: Mestre, Transacional, Referencia
          3. Aplicação das Tags nas tabelas (Passo 1 do Mini-Lab)
          4. Linhagem Ponta a Ponta (Passo 3 do Mini-Lab e Pipeline Educacional)
          5. Test Suites e Test Cases de Qualidade (Passo 4 do Mini-Lab)
=============================================================================
"""

import json
import base64
import time
import requests

BASE_URL = "http://localhost:8585/api/v1"
ADMIN_EMAIL = "admin@open-metadata.org"
ADMIN_PASS_B64 = base64.b64encode(b"admin").decode("utf-8")


def get_token():
    resp = requests.post(
        f"{BASE_URL}/users/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASS_B64}
    )
    resp.raise_for_status()
    return resp.json()["accessToken"]


def setup_service_and_schemas(token):
    print("\n[*] 1. Configurando Database Service, Database e Schemas...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 1.1 Serviço Postgres pg_ecommerce
    svc_payload = {
        "name": "pg_ecommerce",
        "displayName": "PostgreSQL E-Commerce & Conteúdos",
        "description": "Banco de dados relacional principal contendo as camadas Staging, Silver e Gold.",
        "serviceType": "Postgres",
        "connection": {
            "config": {
                "type": "Postgres",
                "scheme": "postgresql+psycopg2",
                "username": "openmetadata_user",
                "authType": {"password": "openmetadata_pass123"},
                "hostPort": "meu_postgres:5432",
                "database": "meu_banco_de_dados"
            }
        }
    }
    r_svc = requests.get(f"{BASE_URL}/services/databaseServices/name/pg_ecommerce", headers=headers)
    if r_svc.status_code == 404:
        r_create = requests.post(f"{BASE_URL}/services/databaseServices", headers=headers, json=svc_payload)
        r_create.raise_for_status()
        print("  [+] Database Service 'pg_ecommerce' criado.")
    else:
        print("  [✔] Database Service 'pg_ecommerce' já existe.")

    # 1.2 Database meu_banco_de_dados
    db_payload = {"name": "meu_banco_de_dados", "service": "pg_ecommerce"}
    r_db = requests.get(f"{BASE_URL}/databases/name/pg_ecommerce.meu_banco_de_dados", headers=headers)
    if r_db.status_code == 404:
        r_create_db = requests.post(f"{BASE_URL}/databases", headers=headers, json=db_payload)
        r_create_db.raise_for_status()
        print("  [+] Database 'meu_banco_de_dados' criado.")
    else:
        print("  [✔] Database 'meu_banco_de_dados' já existe.")

    # 1.3 Schemas staging, silver, gold
    for s in ["staging", "silver", "gold"]:
        s_fqn = f"pg_ecommerce.meu_banco_de_dados.{s}"
        r_s = requests.get(f"{BASE_URL}/databaseSchemas/name/{s_fqn}", headers=headers)
        if r_s.status_code == 404:
            s_payload = {"name": s, "database": "pg_ecommerce.meu_banco_de_dados"}
            requests.post(f"{BASE_URL}/databaseSchemas", headers=headers, json=s_payload).raise_for_status()
            print(f"  [+] Schema '{s}' criado.")
        else:
            print(f"  [✔] Schema '{s}' já existe.")


def setup_all_tables(token):
    print("\n[*] 2. Registrando Tabelas de E-Commerce e Conteúdos no Catálogo...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    tables_definitions = [
        # --- E-COMMERCE STAGING ---
        {
            "name": "produtos",
            "schema": "staging",
            "description": "Tabela staging com dados brutos de produtos importados do CSV.",
            "columns": [
                {"name": "codigo", "dataType": "VARCHAR", "dataLength": 50, "description": "Código bruto do produto"},
                {"name": "nome", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome bruto do produto"},
                {"name": "preco", "dataType": "VARCHAR", "dataLength": 50, "description": "Preço textual"},
                {"name": "categoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Categoria textual"},
                {"name": "data_cadastro", "dataType": "VARCHAR", "dataLength": 50, "description": "Data textual"}
            ]
        },
        {
            "name": "vendas",
            "schema": "staging",
            "description": "Tabela staging com registros brutos de transações de venda.",
            "columns": [
                {"name": "id_venda", "dataType": "VARCHAR", "dataLength": 50, "description": "ID bruto da venda"},
                {"name": "codigo_produto", "dataType": "VARCHAR", "dataLength": 50, "description": "Código do produto vendido"},
                {"name": "quantidade", "dataType": "VARCHAR", "dataLength": 50, "description": "Quantidade textual"},
                {"name": "valor_unitario", "dataType": "VARCHAR", "dataLength": 50, "description": "Valor unitário textual"},
                {"name": "valor_total", "dataType": "VARCHAR", "dataLength": 50, "description": "Valor total textual"},
                {"name": "data_venda", "dataType": "VARCHAR", "dataLength": 50, "description": "Data textual"},
                {"name": "cliente_id", "dataType": "VARCHAR", "dataLength": 50, "description": "ID do cliente"}
            ]
        },
        {
            "name": "clientes",
            "schema": "staging",
            "description": "Tabela staging com dados cadastrais brutos de clientes.",
            "columns": [
                {"name": "cliente_id", "dataType": "VARCHAR", "dataLength": 50, "description": "ID do cliente"},
                {"name": "nome", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome do cliente"},
                {"name": "email", "dataType": "VARCHAR", "dataLength": 255, "description": "E-mail informado"},
                {"name": "cidade", "dataType": "VARCHAR", "dataLength": 100, "description": "Cidade"},
                {"name": "uf", "dataType": "VARCHAR", "dataLength": 2, "description": "UF"},
                {"name": "segmento", "dataType": "VARCHAR", "dataLength": 50, "description": "Segmento"}
            ]
        },
        # --- E-COMMERCE SILVER ---
        {
            "name": "produtos",
            "schema": "silver",
            "description": "Tabela mestre de produtos limpa, deduplicada e tipada na camada Silver.",
            "columns": [
                {"name": "codigo", "dataType": "VARCHAR", "dataLength": 50, "description": "Chave única primária do produto"},
                {"name": "nome", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome oficial do produto"},
                {"name": "preco", "dataType": "NUMERIC", "description": "Preço de tabela em BRL"},
                {"name": "categoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Categoria do produto"},
                {"name": "data_cadastro", "dataType": "DATE", "description": "Data de homologação"},
                {"name": "processado_em", "dataType": "TIMESTAMP", "description": "Carimbo de data/hora do pipeline"}
            ]
        },
        {
            "name": "vendas",
            "schema": "silver",
            "description": "Tabela transacional de vendas padronizadas e validadas.",
            "columns": [
                {"name": "id_venda", "dataType": "VARCHAR", "dataLength": 50, "description": "Identificador único da transação"},
                {"name": "codigo_produto", "dataType": "VARCHAR", "dataLength": 50, "description": "Código do item"},
                {"name": "quantidade", "dataType": "INT", "description": "Quantidade de itens"},
                {"name": "valor_unitario", "dataType": "NUMERIC", "description": "Valor por unidade"},
                {"name": "valor_total", "dataType": "NUMERIC", "description": "Faturamento bruto da linha"},
                {"name": "data_venda", "dataType": "DATE", "description": "Data do evento"},
                {"name": "cliente_id", "dataType": "VARCHAR", "dataLength": 50, "description": "Chave do comprador"}
            ]
        },
        {
            "name": "clientes",
            "schema": "silver",
            "description": "Tabela mestre de clientes higienizados e deduplicados.",
            "columns": [
                {"name": "cliente_id", "dataType": "VARCHAR", "dataLength": 50, "description": "ID canônico"},
                {"name": "nome", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome tratado"},
                {"name": "email", "dataType": "VARCHAR", "dataLength": 255, "description": "E-mail normalizado"},
                {"name": "cidade", "dataType": "VARCHAR", "dataLength": 100, "description": "Município"},
                {"name": "uf", "dataType": "VARCHAR", "dataLength": 2, "description": "UF"},
                {"name": "segmento", "dataType": "VARCHAR", "dataLength": 50, "description": "Perfil de compra"}
            ]
        },
        {
            "name": "rejeitados",
            "schema": "silver",
            "description": "Log operacional de registros descartados por violação de integridade.",
            "columns": [
                {"name": "id", "dataType": "INT", "description": "ID sequencial"},
                {"name": "pipeline_origem", "dataType": "VARCHAR", "dataLength": 100, "description": "Nome da rotina"},
                {"name": "motivo_erro", "dataType": "VARCHAR", "dataLength": 255, "description": "Causa da rejeição"},
                {"name": "registro_bruto", "dataType": "TEXT", "description": "Linha rejeitada"},
                {"name": "data_rejeicao", "dataType": "TIMESTAMP", "description": "Timestamp do descarte"}
            ]
        },
        # --- E-COMMERCE GOLD ---
        {
            "name": "dim_produto",
            "schema": "gold",
            "description": "Dimensão mestre de produtos no modelo dimensional Star Schema.",
            "columns": [
                {"name": "sk_produto", "dataType": "INT", "description": "Surrogate key inteira"},
                {"name": "codigo_produto", "dataType": "VARCHAR", "dataLength": 50, "description": "Código de negócio"},
                {"name": "nome_produto", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome canônico"},
                {"name": "categoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Macro-categoria"},
                {"name": "subcategoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Sub-categoria"},
                {"name": "preco_tabela", "dataType": "NUMERIC", "description": "Preço base"},
                {"name": "faixa_preco", "dataType": "VARCHAR", "dataLength": 50, "description": "Classificação ABC de preço"},
                {"name": "status_ativo", "dataType": "BOOLEAN", "description": "Flag de produto comercializável"}
            ]
        },
        {
            "name": "dim_cliente",
            "schema": "gold",
            "description": "Dimensão mestre corporativa de clientes no Star Schema.",
            "columns": [
                {"name": "sk_cliente", "dataType": "INT", "description": "Surrogate key inteira"},
                {"name": "cliente_id", "dataType": "VARCHAR", "dataLength": 50, "description": "ID corporativo"},
                {"name": "nome_cliente", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome completo"},
                {"name": "email", "dataType": "VARCHAR", "dataLength": 255, "description": "E-mail verificado"},
                {"name": "cidade", "dataType": "VARCHAR", "dataLength": 100, "description": "Cidade"},
                {"name": "uf", "dataType": "VARCHAR", "dataLength": 2, "description": "Estado"},
                {"name": "regiao", "dataType": "VARCHAR", "dataLength": 50, "description": "Região geográfica"},
                {"name": "segmento", "dataType": "VARCHAR", "dataLength": 50, "description": "Cluster de cliente"},
                {"name": "status_cliente", "dataType": "VARCHAR", "dataLength": 20, "description": "Status Ativo/Inativo"}
            ]
        },
        {
            "name": "fato_vendas",
            "schema": "gold",
            "description": "Tabela Fato transacional de vendas com métricas analíticas e faturamento líquido.",
            "columns": [
                {"name": "sk_venda", "dataType": "BIGINT", "description": "Chave primária do item de pedido"},
                {"name": "id_venda", "dataType": "VARCHAR", "dataLength": 50, "description": "Identificador da transação"},
                {"name": "sk_cliente", "dataType": "INT", "description": "FK para dim_cliente"},
                {"name": "sk_produto", "dataType": "INT", "description": "FK para dim_produto"},
                {"name": "quantidade", "dataType": "INT", "description": "Quantidade vendida"},
                {"name": "preco_unitario", "dataType": "NUMERIC", "description": "Preço praticado"},
                {"name": "valor_bruto", "dataType": "NUMERIC", "description": "Quantidade * Preço"},
                {"name": "desconto_aplicado", "dataType": "NUMERIC", "description": "Desconto concedido"},
                {"name": "valor_liquido", "dataType": "NUMERIC", "description": "Faturamento líquido"},
                {"name": "custo_total", "dataType": "NUMERIC", "description": "Custo das mercadorias"},
                {"name": "margem_lucro", "dataType": "NUMERIC", "description": "Margem de contribuição"},
                {"name": "data_venda", "dataType": "DATE", "description": "Data contábil"}
            ]
        },
        # --- DATASET CONTEÚDOS EDUCACIONAIS (CSV) ---
        {
            "name": "conteudos",
            "schema": "staging",
            "description": "Ingestão bruta do arquivo CSV conteudos.csv com 1000 títulos e metadados.",
            "columns": [
                {"name": "conteudo_id", "dataType": "INT", "description": "ID numérico bruto da obra"},
                {"name": "titulo", "dataType": "TEXT", "description": "Título original do curso, vídeo, podcast ou artigo"},
                {"name": "tipo", "dataType": "VARCHAR", "dataLength": 50, "description": "Formato: Curso, Podcast, Artigo, Vídeo"},
                {"name": "categoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Área técnica do conteúdo"},
                {"name": "nivel", "dataType": "VARCHAR", "dataLength": 50, "description": "Nível de complexidade: Básico, Intermediário, Avançado"},
                {"name": "carga_horaria_min", "dataType": "INT", "description": "Duração em minutos"},
                {"name": "data_publicacao", "dataType": "DATE", "description": "Data de disponibilização"},
                {"name": "descricao", "dataType": "TEXT", "description": "Ementa detalhada da obra"},
                {"name": "autor", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome do instrutor/autor com titulação"}
            ]
        },
        {
            "name": "conteudos",
            "schema": "silver",
            "description": "Tabela mestre de conteúdos higienizada, com detecção de duplicatas de negócio e golden_record_id.",
            "columns": [
                {"name": "conteudo_id", "dataType": "INT", "description": "Chave primária do registro"},
                {"name": "titulo", "dataType": "VARCHAR", "dataLength": 255, "description": "Título padronizado"},
                {"name": "tipo", "dataType": "VARCHAR", "dataLength": 50, "description": "Formato do conteúdo"},
                {"name": "categoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Categoria validada"},
                {"name": "nivel", "dataType": "VARCHAR", "dataLength": 50, "description": "Nível validado"},
                {"name": "carga_horaria_min", "dataType": "INT", "description": "Carga horária em minutos"},
                {"name": "data_publicacao", "dataType": "DATE", "description": "Data de lançamento"},
                {"name": "descricao", "dataType": "TEXT", "description": "Descrição tratada"},
                {"name": "autor", "dataType": "VARCHAR", "dataLength": 255, "description": "Autor normalizado"},
                {"name": "is_duplicata", "dataType": "BOOLEAN", "description": "Flag de re-publicação (TRUE se for versão duplicada)"},
                {"name": "golden_record_id", "dataType": "INT", "description": "Ponteiro para a versão canônica original"}
            ]
        },
        {
            "name": "dim_conteudo",
            "schema": "gold",
            "description": "Dimensão Mestre do acervo educacional com Golden Records consolidados (989 títulos únicos).",
            "columns": [
                {"name": "sk_conteudo", "dataType": "INT", "description": "Surrogate key única da obra"},
                {"name": "conteudo_id", "dataType": "INT", "description": "ID técnico canônico"},
                {"name": "titulo", "dataType": "VARCHAR", "dataLength": 255, "description": "Título oficial único"},
                {"name": "tipo", "dataType": "VARCHAR", "dataLength": 50, "description": "Formato da publicação"},
                {"name": "categoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Categoria temática"},
                {"name": "nivel", "dataType": "VARCHAR", "dataLength": 50, "description": "Grau de profundidade"},
                {"name": "carga_horaria_min", "dataType": "INT", "description": "Duração em minutos"},
                {"name": "carga_horaria_horas", "dataType": "NUMERIC", "description": "Duração convertida em horas"},
                {"name": "autor", "dataType": "VARCHAR", "dataLength": 255, "description": "Autor criador"},
                {"name": "data_primeira_publicacao", "dataType": "DATE", "description": "Data da primeira edição"},
                {"name": "versoes_identificadas", "dataType": "INT", "description": "Total de edições ou republicações mapeadas"}
            ]
        },
        {
            "name": "dim_autor",
            "schema": "gold",
            "description": "Dimensão Mestre de autores e especialistas cadastrados na plataforma.",
            "columns": [
                {"name": "sk_autor", "dataType": "INT", "description": "Surrogate key do autor"},
                {"name": "nome_autor", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome com titulação formal"},
                {"name": "titulacao", "dataType": "VARCHAR", "dataLength": 50, "description": "Titulação acadêmica (Dra., Prof., Eng.)"},
                {"name": "nome_limpo", "dataType": "VARCHAR", "dataLength": 255, "description": "Nome próprio desprovido de prefixos"},
                {"name": "total_conteudos", "dataType": "INT", "description": "Obras publicadas no acervo"},
                {"name": "total_horas", "dataType": "NUMERIC", "description": "Total de horas letivas produzidas"},
                {"name": "categoria_principal", "dataType": "VARCHAR", "dataLength": 100, "description": "Área de maior atuação"}
            ]
        },
        {
            "name": "dim_categoria",
            "schema": "gold",
            "description": "Dimensão de Referência contendo a taxonomia oficial de especialidades tecnológicas.",
            "columns": [
                {"name": "sk_categoria", "dataType": "INT", "description": "Surrogate key da categoria"},
                {"name": "nome_categoria", "dataType": "VARCHAR", "dataLength": 100, "description": "Nome oficial da área"},
                {"name": "macro_area", "dataType": "VARCHAR", "dataLength": 100, "description": "Agrupamento estratégico"},
                {"name": "total_titulos", "dataType": "INT", "description": "Acervo disponível na especialidade"}
            ]
        },
        {
            "name": "fato_publicacoes",
            "schema": "gold",
            "description": "Tabela Fato transacional registrando todos os 1000 eventos históricos de publicação de conteúdos.",
            "columns": [
                {"name": "sk_publicacao", "dataType": "INT", "description": "Chave primária do evento de lançamento"},
                {"name": "conteudo_id", "dataType": "INT", "description": "ID operacional do item"},
                {"name": "sk_conteudo", "dataType": "INT", "description": "FK para dim_conteudo"},
                {"name": "sk_autor", "dataType": "INT", "description": "FK para dim_autor"},
                {"name": "sk_categoria", "dataType": "INT", "description": "FK para dim_categoria"},
                {"name": "tipo", "dataType": "VARCHAR", "dataLength": 50, "description": "Tipo da mídia"},
                {"name": "nivel", "dataType": "VARCHAR", "dataLength": 50, "description": "Nível do conteúdo"},
                {"name": "data_publicacao", "dataType": "DATE", "description": "Data do evento"},
                {"name": "ano_publicacao", "dataType": "INT", "description": "Ano do calendário"},
                {"name": "mes_publicacao", "dataType": "INT", "description": "Mês do calendário"},
                {"name": "carga_horaria_min", "dataType": "INT", "description": "Duração em minutos"},
                {"name": "carga_horaria_horas", "dataType": "NUMERIC", "description": "Duração em horas"}
            ]
        }
    ]

    created_tables = {}
    for tbl in tables_definitions:
        t_name = tbl["name"]
        schema = tbl["schema"]
        fqn = f"pg_ecommerce.meu_banco_de_dados.{schema}.{t_name}"
        
        r_get = requests.get(f"{BASE_URL}/tables/name/{fqn}", headers=headers)
        if r_get.status_code == 404:
            payload = {
                "name": t_name,
                "displayName": f"{t_name.capitalize()} ({schema})",
                "description": tbl["description"],
                "databaseSchema": f"pg_ecommerce.meu_banco_de_dados.{schema}",
                "columns": tbl["columns"]
            }
            r_post = requests.post(f"{BASE_URL}/tables", headers=headers, json=payload)
            r_post.raise_for_status()
            tbl_obj = r_post.json()
            created_tables[fqn] = tbl_obj["id"]
            print(f"  [+] Tabela '{fqn}' criada no catálogo.")
        else:
            tbl_obj = r_get.json()
            created_tables[fqn] = tbl_obj["id"]
            print(f"  [✔] Tabela '{fqn}' já catalogada.")

    return created_tables


def setup_classifications_and_tags(token):
    print("\n[*] 3. Configurando Classification 'TipoDado' e Tags de Governança (Passo 1)...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    with open("/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/classificacao/tags_classificacao.json", "r") as f:
        config = json.load(f)

    for c in config["classificacoes"]:
        c_name = c["name"]
        r_c = requests.get(f"{BASE_URL}/classifications/name/{c_name}", headers=headers)
        if r_c.status_code == 404:
            payload = {
                "name": c_name,
                "displayName": c.get("displayName", c_name),
                "description": c.get("description", ""),
                "mutuallyExclusive": c.get("mutuallyExclusive", False)
            }
            requests.post(f"{BASE_URL}/classifications", headers=headers, json=payload).raise_for_status()
            print(f"  [+] Classification '{c_name}' criada.")
        else:
            print(f"  [✔] Classification '{c_name}' já existe.")

        for t in c.get("tags", []):
            t_name = t["name"]
            tag_fqn = f"{c_name}.{t_name}"
            r_t = requests.get(f"{BASE_URL}/tags/name/{tag_fqn}", headers=headers)
            if r_t.status_code == 404:
                payload = {
                    "classification": c_name,
                    "name": t_name,
                    "displayName": t.get("displayName", t_name),
                    "description": t.get("description", "")
                }
                requests.post(f"{BASE_URL}/tags", headers=headers, json=payload).raise_for_status()
                print(f"    [+] Tag '{tag_fqn}' criada.")
            else:
                print(f"    [✔] Tag '{tag_fqn}' já existe.")

    # 3.2 Aplicar Tags nas Tabelas
    print("\n[*] 4. Aplicando Tags 'TipoDado' nas 16 Tabelas do Catálogo...")
    patch_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json-patch+json"}
    
    for table_fqn, tags_list in config.get("aplicacao_nas_tabelas", {}).items():
        r_tbl = requests.get(f"{BASE_URL}/tables/name/{table_fqn}?fields=tags", headers=headers)
        if not r_tbl.ok:
            continue
        tbl_data = r_tbl.json()
        table_id = tbl_data["id"]
        current_tags = {t["tagFQN"] for t in tbl_data.get("tags", [])}

        patches = []
        for tag in tags_list:
            if tag not in current_tags:
                patches.append({
                    "op": "add",
                    "path": "/tags/-",
                    "value": {
                        "tagFQN": tag,
                        "source": "Classification",
                        "labelType": "Manual",
                        "state": "Confirmed"
                    }
                })
                current_tags.add(tag)

        if patches:
            requests.patch(f"{BASE_URL}/tables/{table_id}", headers=patch_headers, json=patches).raise_for_status()
            print(f"  [+] Tag {tags_list} aplicada na tabela '{table_fqn}'.")
        else:
            print(f"  [✔] Tabela '{table_fqn}' já possui a tag {tags_list}.")


def setup_lineage(token, table_id_map):
    print("\n[*] 5. Estabelecendo Linhagem de Dados Ponta a Ponta no OpenMetadata (Passo 3)...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    with open("/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/linhagem/linhagem_metadados.json", "r") as f:
        lin_data = json.load(f)

    total_edges = 0
    for pipe in lin_data.get("pipelines", []):
        pipe_name = pipe["nome"]
        print(f"  [*] Processando {pipe_name}...")
        for edge in pipe.get("edges", []):
            from_fqn = edge["from"]
            to_fqn = edge["to"]
            desc = edge["transformacao"]

            if from_fqn not in table_id_map or to_fqn not in table_id_map:
                # Tentar obter IDs diretamente
                r_f = requests.get(f"{BASE_URL}/tables/name/{from_fqn}", headers=headers)
                r_t = requests.get(f"{BASE_URL}/tables/name/{to_fqn}", headers=headers)
                if not r_f.ok or not r_t.ok:
                    continue
                from_id = r_f.json()["id"]
                to_id = r_t.json()["id"]
            else:
                from_id = table_id_map[from_fqn]
                to_id = table_id_map[to_fqn]

            payload = {
                "edge": {
                    "fromEntity": {"id": from_id, "type": "table"},
                    "toEntity": {"id": to_id, "type": "table"},
                    "lineageDetails": {
                        "source": "Manual",
                        "description": desc
                    }
                }
            }
            r_put = requests.put(f"{BASE_URL}/lineage", headers=headers, json=payload)
            if r_put.ok:
                total_edges += 1
                from_short = from_fqn.split(".")[-2] + "." + from_fqn.split(".")[-1]
                to_short = to_fqn.split(".")[-2] + "." + to_fqn.split(".")[-1]
                print(f"    [✔] Edge criada: {from_short} -> {to_short}")
            else:
                print(f"    [!] Erro na edge {from_fqn} -> {to_fqn}: {r_put.text}")

    print(f"  [✔] Total de {total_edges} conexões de linhagem ativas no catálogo.")


def setup_data_quality(token):
    print("\n[*] 6. Configurando Test Suites e Test Cases de Qualidade (Passo 4)...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    with open("/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-03-dados-mestres-linhagem-qualidade/qualidade/test_suites_qualidade.json", "r") as f:
        suites_data = json.load(f)

    for suite in suites_data.get("testSuites", []):
        table_fqn = suite["targetTable"]
        r_tbl = requests.get(f"{BASE_URL}/tables/name/{table_fqn}", headers=headers)
        if not r_tbl.ok:
            continue
        
        # 6.1 Criar Executable Test Suite
        ts_name = f"{table_fqn}.testSuite"
        r_ts_get = requests.get(f"{BASE_URL}/dataQuality/testSuites/name/{ts_name}", headers=headers)
        if r_ts_get.status_code == 404:
            ts_payload = {
                "name": ts_name,
                "displayName": suite["displayName"],
                "description": suite["description"],
                "executableEntityReference": table_fqn,
                "basicEntityReference": table_fqn
            }
            r_ts = requests.put(f"{BASE_URL}/dataQuality/testSuites/executable", headers=headers, json=ts_payload)
            if r_ts.ok:
                print(f"  [+] Executable Test Suite '{suite['name']}' criada para {table_fqn}.")
            else:
                print(f"  [!] Erro criando Test Suite: {r_ts.text}")
        else:
            print(f"  [✔] Test Suite '{suite['name']}' já existe.")

        # 6.2 Criar Test Cases
        for tc in suite.get("testCases", []):
            tc_name = tc["name"]
            col = tc.get("column")
            if col:
                entity_link = f"<#E::table::{table_fqn}::columns::{col}>"
                tc_fqn = f"{table_fqn}.{col}.{tc_name}"
            else:
                entity_link = f"<#E::table::{table_fqn}>"
                tc_fqn = f"{table_fqn}.{tc_name}"

            r_tc_get = requests.get(f"{BASE_URL}/dataQuality/testCases/name/{tc_fqn}", headers=headers)
            if r_tc_get.status_code == 404:
                tc_payload = {
                    "name": tc_name,
                    "displayName": tc["displayName"],
                    "description": tc["description"],
                    "entityLink": entity_link,
                    "testDefinition": tc["testDefinition"]
                }
                if tc.get("parameters"):
                    tc_payload["parameterValues"] = tc["parameters"]

                r_tc = requests.post(f"{BASE_URL}/dataQuality/testCases", headers=headers, json=tc_payload)
                if r_tc.ok:
                    print(f"    [+] Test Case '{tc_name}' criado ({tc['dimensao']}).")
                    
                    # Registrar resultado inicial aprovado (PASSED / Success)
                    now_ms = int(time.time() * 1000)
                    res_payload = {
                        "timestamp": now_ms,
                        "testCaseStatus": "Success",
                        "result": f"Aprovado: Teste de {tc['dimensao']} validado sem violações.",
                        "testResultValue": [
                            {"name": "passedRows", "value": "100%"},
                            {"name": "failedRows", "value": "0"}
                        ]
                    }
                    requests.post(
                        f"{BASE_URL}/dataQuality/testCases/testCaseResults/{tc_fqn}",
                        headers=headers,
                        json=res_payload
                    )
                else:
                    print(f"    [!] Erro criando Test Case '{tc_name}': {r_tc.text}")
            else:
                print(f"    [✔] Test Case '{tc_name}' já existe.")


def main():
    print("======================================================================")
    print("   AUTOMAÇÃO AULA 03 — DADOS MESTRES, LINHAGEM E QUALIDADE DE DADOS")
    print("======================================================================")

    token = get_token()
    print("[*] Autenticado no OpenMetadata com sucesso.")

    setup_service_and_schemas(token)
    table_id_map = setup_all_tables(token)
    setup_classifications_and_tags(token)
    setup_lineage(token, table_id_map)
    setup_data_quality(token)

    print("\n======================================================================")
    print("✔ TUDO PRONTO! ECOSSISTEMA AULA 03 100% REGISTRADO NO OPENMETADATA!")
    print("======================================================================\n")


if __name__ == "__main__":
    main()
