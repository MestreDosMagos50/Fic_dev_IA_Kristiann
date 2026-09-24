#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 01: Conceitos de Documentação, Metadados e Governança de Dados
Arquivo: scripts/popular_metadados_openmetadata.py
Objetivo: Popular automaticamente todo o acervo das 5 tabelas no OpenMetadata
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


def get_admin_user(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BASE_URL}/users/name/admin", headers=headers)
    resp.raise_for_status()
    u = resp.json()
    return {
        "id": u["id"],
        "type": "user",
        "name": u["name"],
        "fullyQualifiedName": u.get("fullyQualifiedName", "admin"),
        "displayName": u.get("displayName", "admin"),
        "deleted": False
    }


def update_table(token, admin_user, table_meta):
    fqn = table_meta["fqn"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Obter estado atual da tabela
    resp = requests.get(
        f"{BASE_URL}/tables/name/{fqn}?fields=columns,owners,tags",
        headers=headers
    )
    if resp.status_code == 404:
        print(f"[-] Tabela {fqn} não encontrada no OpenMetadata.")
        return False
    resp.raise_for_status()
    current = resp.json()
    table_id = current["id"]

    patch_operations = []

    # 2. Descrição da tabela
    new_desc = table_meta["descricao"] + " Granularidade: " + table_meta["granularidade"]
    if current.get("description") != new_desc:
        op = "replace" if "description" in current else "add"
        patch_operations.append({"op": op, "path": "/description", "value": new_desc})

    # 3. Dono (Owner)
    current_owners = current.get("owners", [])
    if not current_owners:
        patch_operations.append({"op": "add", "path": "/owners", "value": [admin_user]})

    # 4. Tier Tag
    tier_tag = table_meta["tier"]  # Ex: "Tier.Tier1"
    existing_tier = [t for t in current.get("tags", []) if t.get("tagFQN", "").startswith("Tier.")]
    if not existing_tier or existing_tier[0].get("tagFQN") != tier_tag:
        tier_obj = {
            "tagFQN": tier_tag,
            "source": "Classification",
            "labelType": "Manual",
            "state": "Confirmed"
        }
        other_tags = [t for t in current.get("tags", []) if not t.get("tagFQN", "").startswith("Tier.")]
        patch_operations.append({
            "op": "replace" if "tags" in current else "add",
            "path": "/tags",
            "value": other_tags + [tier_obj]
        })

    # 5. Colunas
    current_cols = current.get("columns", [])
    meta_cols_dict = {c["nome"]: c for c in table_meta.get("colunas", [])}

    for idx, c in enumerate(current_cols):
        c_name = c["name"]
        if c_name in meta_cols_dict:
            m_col = meta_cols_dict[c_name]
            desc_val = m_col["descricao"]
            if "regras_calculo" in table_meta and c_name in table_meta["regras_calculo"]:
                desc_val += f" [Fórmula: {table_meta['regras_calculo'][c_name]}]"
            
            if c.get("description") != desc_val:
                op = "replace" if "description" in c else "add"
                patch_operations.append({
                    "op": op,
                    "path": f"/columns/{idx}/description",
                    "value": desc_val
                })

    if not patch_operations:
        print(f"[✔] Tabela {fqn} já estava 100% atualizada.")
        return True

    # 6. Executar JSON Patch
    patch_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json-patch+json"
    }
    patch_resp = requests.patch(
        f"{BASE_URL}/tables/{table_id}",
        headers=patch_headers,
        json=patch_operations
    )
    patch_resp.raise_for_status()
    print(f"[✔ SUCESSO] Tabela {fqn} atualizada ({len(patch_operations)} campos aplicados).")
    return True


def main():
    print("======================================================================")
    print("   POPULANDO ACERVO DE GOVERNANÇA COMPLETO NO OPENMETADATA")
    print("======================================================================")

    with open("/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_03_governanca/aula-01-documentacao-metadados-openmetadata/metadados/catalogo_metadados.json") as f:
        catalogo = json.load(f)

    token = get_token()
    admin_user = get_admin_user(token)
    print(f"[*] Autenticado com sucesso como: {admin_user['name']}")

    for tbl in catalogo["tabelas"]:
        update_table(token, admin_user, tbl)

    print("\n======================================================================")
    print("✔ TODAS AS 5 TABELAS FORAM FORMALMENTE CATALOGADAS NO OPENMETADATA!")
    print("======================================================================")


if __name__ == "__main__":
    main()
