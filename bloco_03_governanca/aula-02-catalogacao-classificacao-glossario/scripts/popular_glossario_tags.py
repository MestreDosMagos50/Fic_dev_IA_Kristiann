#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 02: Catalogação, Classificação e Glossário de Negócio
Arquivo: scripts/popular_glossario_tags.py
Objetivo: Criar e aplicar Classifications, Tags, Glossário e Termos com Hierarquia
=============================================================================
"""

import json
import base64
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


def setup_classifications_and_tags(token):
    print("\n[*] 1. Configurando Classifications e Tags...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    with open("/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-02-catalogacao-classificacao-glossario/classificacao/tags_classificacao.json") as f:
        config = json.load(f)

    for c in config["classificacoes"]:
        # Criar Classification se não existir
        c_name = c["name"]
        resp = requests.get(f"{BASE_URL}/classifications/name/{c_name}", headers=headers)
        if resp.status_code == 404:
            c_payload = {
                "name": c_name,
                "displayName": c.get("displayName", c_name),
                "description": c.get("description", ""),
                "mutuallyExclusive": c.get("mutuallyExclusive", False)
            }
            resp_c = requests.post(f"{BASE_URL}/classifications", headers=headers, json=c_payload)
            resp_c.raise_for_status()
            print(f"  [+] Classification '{c_name}' criada com sucesso.")
        else:
            print(f"  [✔] Classification '{c_name}' já existe.")

        # Criar Tags da Classification
        for t in c.get("tags", []):
            t_name = t["name"]
            tag_fqn = f"{c_name}.{t_name}"
            resp_t = requests.get(f"{BASE_URL}/tags/name/{tag_fqn}", headers=headers)
            if resp_t.status_code == 404:
                t_payload = {
                    "classification": c_name,
                    "name": t_name,
                    "displayName": t.get("displayName", t_name),
                    "description": t.get("description", "")
                }
                resp_create_tag = requests.post(f"{BASE_URL}/tags", headers=headers, json=t_payload)
                resp_create_tag.raise_for_status()
                print(f"    [+] Tag '{tag_fqn}' criada.")
            else:
                print(f"    [✔] Tag '{tag_fqn}' já existe.")

    return config


def setup_glossary_and_terms(token):
    print("\n[*] 2. Configurando Glossário e Termos Semânticos...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    with open("/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-02-catalogacao-classificacao-glossario/glossario/glossario_ecommerce.json") as f:
        glossario_data = json.load(f)

    g_info = glossario_data["glossario"]
    g_name = g_info["name"]

    # 2.1 Criar Glossário se não existir
    resp_g = requests.get(f"{BASE_URL}/glossaries/name/{g_name}", headers=headers)
    if resp_g.status_code == 404:
        g_payload = {
            "name": g_name,
            "displayName": g_info.get("displayName", g_name),
            "description": g_info.get("description", "")
        }
        resp_create = requests.post(f"{BASE_URL}/glossaries", headers=headers, json=g_payload)
        resp_create.raise_for_status()
        print(f"  [+] Glossário '{g_name}' criado com sucesso.")
    else:
        print(f"  [✔] Glossário '{g_name}' já existe.")

    # 2.2 Criar Termos
    def create_or_update_term(term_dict, parent_fqn=None):
        t_name = term_dict["name"]
        fqn = f"{parent_fqn}.{t_name}" if parent_fqn else f"{g_name}.{t_name}"
        resp_t = requests.get(f"{BASE_URL}/glossaryTerms/name/{fqn}", headers=headers)

        payload = {
            "glossary": g_name,
            "name": t_name,
            "displayName": term_dict.get("displayName", t_name),
            "description": term_dict.get("description", ""),
            "synonyms": term_dict.get("synonyms", [])
        }
        if parent_fqn:
            payload["parent"] = parent_fqn

        if resp_t.status_code == 404:
            resp_create = requests.post(f"{BASE_URL}/glossaryTerms", headers=headers, json=payload)
            if not resp_create.ok:
                print(f"      [!] Falha criando {fqn}: {resp_create.text}")
            resp_create.raise_for_status()
            print(f"    [+] Termo '{fqn}' criado.")
        else:
            print(f"    [✔] Termo '{fqn}' já existe.")

        # Processar filhos recursivamente
        for filho in term_dict.get("filhos", []):
            create_or_update_term(filho, parent_fqn=fqn)

    for termo in glossario_data["termos"]:
        create_or_update_term(termo)

    return glossario_data


def apply_tags_and_glossary_links(token, config_classificacao, glossario_data):
    print("\n[*] 3. Vinculando Tags e Termos de Glossário às Tabelas e Colunas...")
    headers = {"Authorization": f"Bearer {token}"}
    patch_headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json-patch+json"}

    # 3.1 Aplicar Tags de Tabela (Camada, Domínio, Certificação)
    for table_fqn, tags_to_add in config_classificacao.get("aplicacao_nas_tabelas", {}).items():
        resp = requests.get(f"{BASE_URL}/tables/name/{table_fqn}?fields=tags,columns", headers=headers)
        if resp.status_code == 404:
            continue
        resp.raise_for_status()
        table_obj = resp.json()
        table_id = table_obj["id"]

        current_tags = table_obj.get("tags", [])
        current_tag_fqns = {t["tagFQN"] for t in current_tags}

        patches = []
        for tag in tags_to_add:
            if tag not in current_tag_fqns:
                tag_item = {
                    "tagFQN": tag,
                    "source": "Classification",
                    "labelType": "Manual",
                    "state": "Confirmed"
                }
                patches.append({"op": "add", "path": "/tags/-", "value": tag_item})
                current_tag_fqns.add(tag)

        if patches:
            p_resp = requests.patch(f"{BASE_URL}/tables/{table_id}", headers=patch_headers, json=patches)
            p_resp.raise_for_status()
            print(f"  [+] Tags {tags_to_add} aplicadas na tabela '{table_fqn}'.")
        else:
            print(f"  [✔] Tabela '{table_fqn}' já possui todas as tags de classificação.")

    # 3.2 Aplicar Termos de Glossário
    termos_map = {
        "pg_ecommerce.meu_banco_de_dados.gold.fato_vendas": {
            "table_terms": [],
            "column_terms": {
                "valor_liquido": ["Glossario_Ecommerce.Ticket_Medio", "Glossario_Ecommerce.Receita_Liquida"],
                "margem_lucro": ["Glossario_Ecommerce.Margem_de_Contribuicao"],
                "sk_venda": ["Glossario_Ecommerce.Item_de_Pedido"]
            }
        },
        "pg_ecommerce.meu_banco_de_dados.gold.dim_cliente": {
            "table_terms": ["Glossario_Ecommerce.Cliente"],
            "column_terms": {
                "status_cliente": ["Glossario_Ecommerce.Cliente.Cliente_Ativo", "Glossario_Ecommerce.Cliente.Cliente_Inativo"]
            }
        }
    }

    for table_fqn, mapping in termos_map.items():
        resp = requests.get(f"{BASE_URL}/tables/name/{table_fqn}?fields=tags,columns", headers=headers)
        if resp.status_code == 404:
            continue
        resp.raise_for_status()
        table_obj = resp.json()
        table_id = table_obj["id"]

        patches = []

        # Termos em nível de tabela
        current_tags = {t["tagFQN"] for t in table_obj.get("tags", [])}
        for term_fqn in mapping.get("table_terms", []):
            if term_fqn not in current_tags:
                patches.append({
                    "op": "add",
                    "path": "/tags/-",
                    "value": {
                        "tagFQN": term_fqn,
                        "source": "Glossary",
                        "labelType": "Manual",
                        "state": "Confirmed"
                    }
                })

        # Termos em colunas
        columns = table_obj.get("columns", [])
        for col_idx, col in enumerate(columns):
            c_name = col["name"]
            if c_name in mapping.get("column_terms", []):
                col_tags = {t["tagFQN"] for t in col.get("tags", [])}
                for term_fqn in mapping["column_terms"][c_name]:
                    if term_fqn not in col_tags:
                        patches.append({
                            "op": "add",
                            "path": f"/columns/{col_idx}/tags/-",
                            "value": {
                                "tagFQN": term_fqn,
                                "source": "Glossary",
                                "labelType": "Manual",
                                "state": "Confirmed"
                            }
                        })
                        col_tags.add(term_fqn)

        if patches:
            p_resp = requests.patch(f"{BASE_URL}/tables/{table_id}", headers=patch_headers, json=patches)
            p_resp.raise_for_status()
            print(f"  [+] Termos de Glossário vinculados à tabela/colunas de '{table_fqn}'.")
        else:
            print(f"  [✔] Termos de Glossário já estavam vinculados a '{table_fqn}'.")


def main():
    print("======================================================================")
    print("   AUTOMAÇÃO AULA 02 — CLASSIFICAÇÃO, TAGS E GLOSSÁRIO NO OPENMETADATA")
    print("======================================================================")

    token = get_token()
    print("[*] Autenticado no OpenMetadata com sucesso.")

    config_classificacao = setup_classifications_and_tags(token)
    glossario_data = setup_glossary_and_terms(token)
    apply_tags_and_glossary_links(token, config_classificacao, glossario_data)

    print("\n======================================================================")
    print("✔ TUDO PRONTO! CLASSIFICAÇÕES, GLOSSÁRIO E VÍNCULOS CRIADOS COM SUCESSO!")
    print("======================================================================\n")


if __name__ == "__main__":
    main()
