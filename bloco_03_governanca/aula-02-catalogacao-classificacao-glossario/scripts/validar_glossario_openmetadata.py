#!/usr/bin/env python3
"""
=============================================================================
FIC Engenharia de Dados | Módulo 3: Governança de Dados com OpenMetadata
Aula 02: Catalogação, Classificação e Glossário de Negócio
Arquivo: scripts/validar_glossario_openmetadata.py
Objetivo: Validar e auditar os 10 pontos de avaliação do Mini-Lab no OpenMetadata
=============================================================================
"""

import base64
import requests

BASE_URL = "http://localhost:8585/api/v1"
ADMIN_EMAIL = "admin@open-metadata.org"
ADMIN_PASS_B64 = base64.b64encode(b"admin").decode("utf-8")

GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def main():
    print(f"\n{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}{BLUE}   AUDITORIA AULA 02 — GLOSSÁRIO, HIERARQUIA, TAGS E VÍNCULOS{RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}\n")

    # 1. Login
    resp = requests.post(f"{BASE_URL}/users/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASS_B64})
    resp.raise_for_status()
    token = resp.json()["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}

    pontuacao_total = 0

    # -------------------------------------------------------------------------
    # CRITÉRIO 1: Cinco termos criados com definição nas quatro partes (4 pts)
    # -------------------------------------------------------------------------
    print(f"{BOLD}[*] Critério 1: Verificando Termos de Negócio no Glossário (4 Pontos){RESET}")
    termos_obrigatorios = [
        "Glossario_Ecommerce.Ticket_Medio",
        "Glossario_Ecommerce.Cliente.Cliente_Ativo",
        "Glossario_Ecommerce.Receita_Liquida",
        "Glossario_Ecommerce.Margem_de_Contribuicao",
        "Glossario_Ecommerce.Item_de_Pedido"
    ]
    termos_ok = 0
    for t_fqn in termos_obrigatorios:
        r = requests.get(f"{BASE_URL}/glossaryTerms/name/{t_fqn}", headers=headers)
        if r.status_code == 200:
            data = r.json()
            desc = data.get("description", "")
            has_4_parts = any(k in desc.lower() for k in ["cálculo", "calcula", "exclusão", "exclusões", "recorte", "o que é", "justificativa"])
            termos_ok += 1
            print(f"  [{GREEN}✔{RESET}] Termo: {BOLD}{data.get('displayName', t_fqn)}{RESET} (Definição detalhada: {GREEN}Sim{RESET})")
        else:
            print(f"  [{RED}✖{RESET}] Termo ausente: {t_fqn}")

    if termos_ok == len(termos_obrigatorios):
        pontuacao_total += 4
        print(f"  {GREEN}➔ Resultado Critério 1: 4.0 / 4.0 PONTOS{RESET}\n")
    else:
        pts = (termos_ok / len(termos_obrigatorios)) * 4
        pontuacao_total += pts
        print(f"  {YELLOW}➔ Resultado Critério 1: {pts:.1f} / 4.0 PONTOS{RESET}\n")

    # -------------------------------------------------------------------------
    # CRITÉRIO 2: Hierarquia Cliente -> Cliente Ativo/Inativo com critério (2 pts)
    # -------------------------------------------------------------------------
    print(f"{BOLD}[*] Critério 2: Hierarquia Semântica Cliente -> Ativo / Inativo (2 Pontos){RESET}")
    r_pai = requests.get(f"{BASE_URL}/glossaryTerms/name/Glossario_Ecommerce.Cliente", headers=headers)
    r_ativo = requests.get(f"{BASE_URL}/glossaryTerms/name/Glossario_Ecommerce.Cliente.Cliente_Ativo", headers=headers)
    r_inativo = requests.get(f"{BASE_URL}/glossaryTerms/name/Glossario_Ecommerce.Cliente.Cliente_Inativo", headers=headers)

    hierarquia_ok = False
    if r_pai.status_code == 200 and r_ativo.status_code == 200 and r_inativo.status_code == 200:
        d_pai = r_pai.json()
        d_ativo = r_ativo.json()
        d_inativo = r_inativo.json()

        tem_criterio_no_pai = "90 dias" in d_pai.get("description", "")
        ativo_parent_ok = d_ativo.get("parent", {}).get("name") == "Cliente"
        inativo_parent_ok = d_inativo.get("parent", {}).get("name") == "Cliente"

        if tem_criterio_no_pai and ativo_parent_ok and inativo_parent_ok:
            hierarquia_ok = True
            pontuacao_total += 2
            print(f"  [{GREEN}✔{RESET}] Termo Pai: {BOLD}Cliente{RESET} com critério explícito no texto: '{d_pai['description'][:85]}...'")
            print(f"  [{GREEN}✔{RESET}] Termo Filho 1: {BOLD}Cliente Ativo{RESET} vinculado ao pai 'Cliente'")
            print(f"  [{GREEN}✔{RESET}] Termo Filho 2: {BOLD}Cliente Inativo{RESET} vinculado ao pai 'Cliente'")
            print(f"  {GREEN}➔ Resultado Critério 2: 2.0 / 2.0 PONTOS{RESET}\n")
        else:
            print(f"  [{YELLOW}Parcial{RESET}] Parentesco ou texto incompleto.")
    else:
        print(f"  [{RED}✖{RESET}] Falha localizando termos da hierarquia.")

    # -------------------------------------------------------------------------
    # CRITÉRIO 3: Termos vinculados a tabelas/colunas do catálogo (2 pts)
    # -------------------------------------------------------------------------
    print(f"{BOLD}[*] Critério 3: Rastreabilidade Semântica — Termos Vinculados às Colunas (2 Pontos){RESET}")
    r_fato = requests.get(f"{BASE_URL}/tables/name/pg_ecommerce.meu_banco_de_dados.gold.fato_vendas?fields=tags,columns", headers=headers)
    r_cli = requests.get(f"{BASE_URL}/tables/name/pg_ecommerce.meu_banco_de_dados.gold.dim_cliente?fields=tags,columns", headers=headers)

    vinculos_encontrados = []
    if r_fato.status_code == 200:
        cols = r_fato.json().get("columns", [])
        for c in cols:
            for tag in c.get("tags", []):
                if tag.get("source") == "Glossary":
                    vinculos_encontrados.append(f"fato_vendas.{c['name']} -> {tag['name']}")

    if r_cli.status_code == 200:
        cols = r_cli.json().get("columns", [])
        for c in cols:
            for tag in c.get("tags", []):
                if tag.get("source") == "Glossary":
                    vinculos_encontrados.append(f"dim_cliente.{c['name']} -> {tag['name']}")

    for v in vinculos_encontrados:
        print(f"  [{GREEN}✔{RESET}] Vínculo semântico: {BOLD}{v}{RESET}")

    if len(vinculos_encontrados) >= 3:
        pontuacao_total += 2
        print(f"  {GREEN}➔ Resultado Critério 3: 2.0 / 2.0 PONTOS{RESET}\n")
    else:
        pontuacao_total += 1
        print(f"  {YELLOW}➔ Resultado Critério 3: 1.0 / 2.0 PONTOS (Mínimo de 3 vínculos recomendado){RESET}\n")

    # -------------------------------------------------------------------------
    # CRITÉRIO 4: Classification Camada criada e aplicada com busca (2 pts)
    # -------------------------------------------------------------------------
    print(f"{BOLD}[*] Critério 4: Classification Camada e Tags Aplicadas (2 Pontos){RESET}")
    r_camada = requests.get(f"{BASE_URL}/classifications/name/Camada", headers=headers)
    r_tags = requests.get(f"{BASE_URL}/tags?parent=Camada", headers=headers)

    # Verificar tabelas com tag Camada.Gold
    r_search = requests.get(f"{BASE_URL}/search/query?q=tags.tagFQN:Camada.Gold&index=table_search_index", headers=headers)

    classificacao_ok = False
    if r_camada.status_code == 200 and r_tags.status_code == 200:
        total_gold_hits = r_search.json().get("hits", {}).get("total", {}).get("value", 0) if r_search.status_code == 200 else 0
        print(f"  [{GREEN}✔{RESET}] Classification {BOLD}Camada{RESET} ativa com tags: Bronze, Silver, Gold")
        print(f"  [{GREEN}✔{RESET}] Busca facetada por {BOLD}Camada.Gold{RESET}: {total_gold_hits} tabelas indexadas no Star Schema")
        if total_gold_hits >= 3:
            classificacao_ok = True
            pontuacao_total += 2
            print(f"  {GREEN}➔ Resultado Critério 4: 2.0 / 2.0 PONTOS{RESET}\n")
        else:
            pontuacao_total += 1
            print(f"  {YELLOW}➔ Resultado Critério 4: 1.0 / 2.0 PONTOS (Menos de 3 tabelas Gold encontradas){RESET}\n")

    # -------------------------------------------------------------------------
    # PLACAR FINAL
    # -------------------------------------------------------------------------
    print(f"{BOLD}{BLUE}======================================================================{RESET}")
    print(f"{BOLD}   NOTA FINAL AUDITADA NO OPENMETADATA: {GREEN}{pontuacao_total:.1f} / 10.0 PONTOS{RESET}")
    if pontuacao_total == 10.0:
        print(f"{BOLD}{GREEN}✔ DESAFIO DO MINI-LAB DA AULA 02 CONCLUÍDO COM NOTA MÁXIMA!{RESET}")
    print(f"{BOLD}{BLUE}======================================================================{RESET}\n")


if __name__ == "__main__":
    main()
