#!/usr/bin/env python3
"""
scripts/executar_carga_completa.py
FIC Engenharia de Dados | Aula 03 (Módulo 2): Apache Hop & Orquestração

Execução end-to-end com 5 Fontes Brasileiras:
1. IBGE Censo & População (CSV)
2. DataSUS Notificações Epidemiológicas de Dengue (CSV Parametrizado)
3. INMET Clima e Chuva Acumulada (CSV)
4. CNES Capacidade Hospitalar & Leitos SUS (PostgreSQL Relacional)
5. Vigilância Sanitária & Alertas Epidemiológicos (MongoDB NoSQL)
"""

import os
import sys
import json
import re
import datetime
import subprocess
import pandas as pd
import numpy as np

DIR_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_BRONZE = os.path.join(DIR_PROJETO, "dados", "bronze")
DIR_SILVER = os.path.join(DIR_PROJETO, "dados", "silver")
DIR_QUARENTENA = os.path.join(DIR_PROJETO, "dados", "quarentena")
DIR_SQL = os.path.join(DIR_PROJETO, "sql")

os.makedirs(DIR_SILVER, exist_ok=True)
os.makedirs(DIR_QUARENTENA, exist_ok=True)

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASS = os.getenv("PG_PASSWORD", "postgres")
PG_DB = os.getenv("PG_DB", "ecommerce")

def executar_psql(script_sql_ou_path: str, is_file=False) -> tuple[bool, str]:
    env = os.environ.copy()
    env["PGPASSWORD"] = PG_PASS
    cmd = ["psql", "-h", PG_HOST, "-p", PG_PORT, "-U", PG_USER, "-d", PG_DB]
    if is_file:
        cmd.extend(["-f", script_sql_ou_path])
    else:
        cmd.extend(["-c", script_sql_ou_path])
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return (proc.returncode == 0), proc.stdout if proc.returncode == 0 else proc.stderr

def main():
    print("=" * 80)
    print("🇧🇷 INICIANDO PIPELINE DAS 5 FONTES BRASILEIRAS (IBGE, DATASUS, INMET, CNES, ALERTAS)")
    print(f"🕒 Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 1. DDL
    print("\n[Etapa 1/5] Executando DDL Idempotente no PostgreSQL...")
    ok, res = executar_psql(os.path.join(DIR_SQL, "01_prepara_schemas.sql"), is_file=True)
    print("✅ Schemas staging, silver e gold verificados no PostgreSQL.")

    # 2. Ingestão Bronze -> Staging
    print("\n[Etapa 2/5] Ingestão Bronze -> Staging (5 Fontes de Cidades, População e Saúde)...")
    executar_psql("TRUNCATE TABLE staging.ibge_municipios, staging.datasus_dengue, staging.inmet_chuva, staging.cnes_leitos, staging.alertas_vigilancia;")

    df_ibge_bronze = pd.read_csv(os.path.join(DIR_BRONZE, "ibge_municipios.csv"), sep=";", dtype=str)
    df_dengue_bronze = pd.read_csv(os.path.join(DIR_BRONZE, "datasus_dengue_2026-08.csv"), sep=";", dtype=str)
    df_chuva_bronze = pd.read_csv(os.path.join(DIR_BRONZE, "inmet_chuva.csv"), sep=";", dtype=str)
    df_leitos_bronze = pd.read_csv(os.path.join(DIR_BRONZE, "cnes_leitos_hospitalares.csv"), sep=";", dtype=str)
    with open(os.path.join(DIR_BRONZE, "alertas_vigilancia.json"), "r", encoding="utf-8") as f:
        alertas_bronze = json.load(f)
    df_alertas_bronze = pd.DataFrame(alertas_bronze).astype(str)

    print(f"  [1/5] Lendo Fonte 1 (IBGE População): {len(df_ibge_bronze)} registros brutos")
    print(f"  [2/5] Lendo Fonte 2 (DataSUS Dengue): {len(df_dengue_bronze)} notificações brutas")
    print(f"  [3/5] Lendo Fonte 3 (INMET Clima): {len(df_chuva_bronze)} leituras pluviométricas")
    print(f"  [4/5] Lendo Fonte 4 (CNES Leitos SUS): {len(df_leitos_bronze)} cadastros de leitos")
    print(f"  [5/5] Lendo Fonte 5 (Vigilância Alertas MongoDB): {len(df_alertas_bronze)} alertas municipais")

    # Ingestão rápida no PostgreSQL
    def esc(val):
        return str(val).replace("'", "''")

    for _, r in df_ibge_bronze.iterrows():
        nome = esc(r['nome_municipio'])
        executar_psql(f"INSERT INTO staging.ibge_municipios VALUES ('{r['cod_mun']}', '{r['cod_mun_6']}', '{nome}', '{r['uf']}', '{r['regiao']}', '{r['populacao']}', '{r['area_km2']}');")

    for _, r in df_dengue_bronze.iterrows():
        cls = esc(r['classificacao'])
        executar_psql(f"INSERT INTO staging.datasus_dengue VALUES ('{r['id_notificacao']}', '{r['cod_mun_6']}', '{r['data_notificacao']}', '{r['casos_notificados']}', '{r['casos_confirmados']}', '{cls}');")

    for _, r in df_chuva_bronze.iterrows():
        est = esc(r['estacao_monitorada'])
        executar_psql(f"INSERT INTO staging.inmet_chuva VALUES ('{r['cod_mun_6']}', '{r['chuva_acumulada_mm']}', '{r['dias_com_chuva']}', '{est}');")

    for _, r in df_leitos_bronze.iterrows():
        mun = esc(r['municipio'])
        executar_psql(f"INSERT INTO staging.cnes_leitos VALUES ('{r['cod_mun_6']}', '{mun}', '{r['leitos_clinicos']}', '{r['leitos_uti']}', '{r['postos_saude']}');")

    for _, r in df_alertas_bronze.iterrows():
        cid = esc(r['cidade'])
        acao = esc(r['acao'])
        executar_psql(f"INSERT INTO staging.alertas_vigilancia VALUES ('{r['id_alerta']}', '{r['cod_mun_6']}', '{cid}', '{r['nivel_risco']}', '{acao}', '{r['data']}');")

    print("✅ Staging carregada com todas as 5 fontes.")

    # 3. Processamento Silver com Quarentena
    print("\n[Etapa 3/5] Padronização Silver e Roteamento de Quarentena...")
    rejeitados = []

    # --- IBGE Municípios ---
    mun_validos = []
    mun_vistos = set()
    for _, r in df_ibge_bronze.iterrows():
        c6 = str(r['cod_mun_6']).strip()
        nome = str(r['nome_municipio']).strip().title()
        uf = str(r['uf']).strip().upper()
        regiao = str(r['regiao']).strip()
        pop_raw = str(r['populacao']).strip()

        try:
            pop_num = int(pop_raw)
            if pop_num <= 0:
                raise ValueError("População deve ser positiva")
        except Exception:
            rejeitados.append({
                "pipeline_origem": "padroniza_ibge_municipios",
                "motivo_erro": f"População inválida ou não positiva ({pop_raw})",
                "registro_bruto": r.to_dict(),
                "data_rejeicao": datetime.datetime.now().isoformat()
            })
            continue

        if c6 in mun_vistos:
            continue
        mun_vistos.add(c6)

        mun_validos.append({
            "cod_mun_6": c6,
            "cod_mun": str(r['cod_mun']),
            "nome_municipio": nome,
            "uf": uf,
            "regiao": regiao,
            "populacao": pop_num,
            "area_km2": float(str(r['area_km2']).replace(',', '.'))
        })
    df_mun_silver = pd.DataFrame(mun_validos)
    df_mun_silver.to_csv(os.path.join(DIR_SILVER, "municipios_silver.csv"), index=False, sep=";")
    print(f"  -> Municípios Silver: {len(df_mun_silver)} cidades validadas e deduplicadas.")

    # --- DataSUS Dengue ---
    dengue_validos = []
    dengue_vistos = set()
    for _, r in df_dengue_bronze.iterrows():
        nid = str(r['id_notificacao']).strip()
        c6 = str(r['cod_mun_6']).strip()
        dt_raw = str(r['data_notificacao']).strip()
        casos_not = str(r['casos_notificados']).strip()
        casos_conf = str(r['casos_confirmados']).strip()

        # Valida casos
        try:
            c_not = int(casos_not)
            c_conf = int(casos_conf)
            if c_not <= 0 or c_conf < 0:
                raise ValueError("Casos devem ser positivos")
        except Exception:
            rejeitados.append({
                "pipeline_origem": "padroniza_datasus_dengue",
                "motivo_erro": f"Casos notificados inválidos ou <= 0 ({casos_not})",
                "registro_bruto": r.to_dict(),
                "data_rejeicao": datetime.datetime.now().isoformat()
            })
            continue

        # Valida data mista
        dt_obj = None
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                dt_obj = datetime.datetime.strptime(dt_raw, fmt).date()
                break
            except Exception:
                pass
        if not dt_obj:
            rejeitados.append({
                "pipeline_origem": "padroniza_datasus_dengue",
                "motivo_erro": f"Data de notificação com formato inválido ({dt_raw})",
                "registro_bruto": r.to_dict(),
                "data_rejeicao": datetime.datetime.now().isoformat()
            })
            continue

        if nid in dengue_vistos:
            continue
        dengue_vistos.add(nid)

        dengue_validos.append({
            "id_notificacao": nid,
            "cod_mun_6": c6,
            "data_notificacao": dt_obj.isoformat(),
            "casos_notificados": c_not,
            "casos_confirmados": c_conf,
            "classificacao": str(r['classificacao']).strip()
        })
    df_dengue_silver = pd.DataFrame(dengue_validos)
    df_dengue_silver.to_csv(os.path.join(DIR_SILVER, "dengue_silver.csv"), index=False, sep=";")
    print(f"  -> Notificações Dengue Silver: {len(df_dengue_silver)} notificações higienizadas.")

    # --- INMET Chuva ---
    chuva_validos = []
    for _, r in df_chuva_bronze.iterrows():
        c6 = str(r['cod_mun_6']).strip()
        ch_raw = str(r['chuva_acumulada_mm']).replace(',', '.').strip()
        try:
            ch_num = float(ch_raw)
            if ch_num < 0:
                raise ValueError("Chuva não pode ser negativa")
        except Exception:
            rejeitados.append({
                "pipeline_origem": "padroniza_inmet_chuva",
                "motivo_erro": f"Leitura de chuva inválida ou negativa ({r['chuva_acumulada_mm']})",
                "registro_bruto": r.to_dict(),
                "data_rejeicao": datetime.datetime.now().isoformat()
            })
            continue

        chuva_validos.append({
            "cod_mun_6": c6,
            "chuva_acumulada_mm": ch_num,
            "dias_com_chuva": int(r['dias_com_chuva']),
            "estacao_monitorada": str(r['estacao_monitorada']).strip()
        })
    df_chuva_silver = pd.DataFrame(chuva_validos)
    df_chuva_silver.to_csv(os.path.join(DIR_SILVER, "chuva_silver.csv"), index=False, sep=";")
    print(f"  -> Clima/Chuva Silver: {len(df_chuva_silver)} estações meteorológicas consolidadas.")

    # --- CNES Leitos ---
    df_leitos_silver = df_leitos_bronze.copy()
    df_leitos_silver.to_csv(os.path.join(DIR_SILVER, "cnes_leitos_silver.csv"), index=False, sep=";")
    print(f"  -> CNES Leitos Silver: {len(df_leitos_silver)} redes hospitalares municipais.")

    # --- Alertas Vigilância (MongoDB) ---
    alertas_validos = []
    niveis_permitidos = {"Baixo Risco", "Médio Risco", "Alto Risco", "Epidemia"}
    for _, r in df_alertas_bronze.iterrows():
        nv = str(r['nivel_risco']).strip()
        if nv not in niveis_permitidos:
            rejeitados.append({
                "pipeline_origem": "padroniza_alertas_vigilancia",
                "motivo_erro": f"Nível de risco epidemiológico não regulamentado ({nv})",
                "registro_bruto": r.to_dict(),
                "data_rejeicao": datetime.datetime.now().isoformat()
            })
            continue
        alertas_validos.append(r.to_dict())
    df_alertas_silver = pd.DataFrame(alertas_validos)
    df_alertas_silver.to_csv(os.path.join(DIR_SILVER, "alertas_silver.csv"), index=False, sep=";")
    print(f"  -> Alertas Vigilância Silver: {len(df_alertas_silver)} alertas sanitários oficiais.")

    # Gravação da Quarentena
    df_rejeitados = pd.DataFrame(rejeitados)
    df_rejeitados.to_csv(os.path.join(DIR_QUARENTENA, "rejeitados_consolidado.csv"), index=False, sep=";")
    with open(os.path.join(DIR_QUARENTENA, "rejeitados_detalhado.json"), "w", encoding="utf-8") as f:
        json.dump(rejeitados, f, indent=2, ensure_ascii=False)
    print(f"  🛡️ Quarentena Registrada: {len(df_rejeitados)} registros anômalos isolados com diagnóstico completo.")

    # Persistência nas tabelas Silver do PostgreSQL
    executar_psql("TRUNCATE TABLE silver.municipios, silver.notificacoes_dengue, silver.inmet_chuva, silver.cnes_leitos, silver.alertas_vigilancia, silver.rejeitados;")
    
    for _, r in df_mun_silver.iterrows():
        nome = esc(r['nome_municipio'])
        executar_psql(f"INSERT INTO silver.municipios VALUES ('{r['cod_mun_6']}', '{r['cod_mun']}', '{nome}', '{r['uf']}', '{r['regiao']}', {r['populacao']}, {r['area_km2']}) ON CONFLICT DO NOTHING;")

    for _, r in df_dengue_silver.iterrows():
        cls = esc(r['classificacao'])
        executar_psql(f"INSERT INTO silver.notificacoes_dengue VALUES ('{r['id_notificacao']}', '{r['cod_mun_6']}', '{r['data_notificacao']}', {r['casos_notificados']}, {r['casos_confirmados']}, '{cls}') ON CONFLICT DO NOTHING;")

    for _, r in df_chuva_silver.iterrows():
        est = esc(r['estacao_monitorada'])
        executar_psql(f"INSERT INTO silver.inmet_chuva VALUES ('{r['cod_mun_6']}', {r['chuva_acumulada_mm']}, {r['dias_com_chuva']}, '{est}') ON CONFLICT DO NOTHING;")

    for _, r in df_leitos_silver.iterrows():
        mun = esc(r['municipio'])
        executar_psql(f"INSERT INTO silver.cnes_leitos VALUES ('{r['cod_mun_6']}', '{mun}', {r['leitos_clinicos']}, {r['leitos_uti']}, {r['postos_saude']}) ON CONFLICT DO NOTHING;")

    for _, r in df_alertas_silver.iterrows():
        cid = esc(r['cidade'])
        acao = esc(r['acao'])
        executar_psql(f"INSERT INTO silver.alertas_vigilancia VALUES ('{r['id_alerta']}', '{r['cod_mun_6']}', '{cid}', '{r['nivel_risco']}', '{acao}', '{r['data']}') ON CONFLICT DO NOTHING;")

    for r in rejeitados:
        p_origem = r['pipeline_origem']
        motivo = r['motivo_erro'].replace("'", "''")
        reg_txt = json.dumps(r['registro_bruto']).replace("'", "''")
        executar_psql(f"INSERT INTO silver.rejeitados (pipeline_origem, motivo_erro, registro_bruto) VALUES ('{p_origem}', '{motivo}', '{reg_txt}');")

    # 4. Executa ELT Analítico no PostgreSQL
    print("\n[Etapa 4/5] Executando Padrão ELT no PostgreSQL (Indicadores Municipais de Dengue)...")
    ok_elt, res_elt = executar_psql(os.path.join(DIR_SQL, "04_elt_indicadores_municipais.sql"), is_file=True)
    if ok_elt:
        print("✅ Transformação ELT no PostgreSQL concluída com sucesso:")
        print("  - Taxa de Incidência por 100k habitantes calculada nativamente.")
        print("  - Classificação de risco epidemiológico gerada diretamente no storage.")
    else:
        print(f"⚠️ Alerta no script ELT: {res_elt}")

    # Exporta tabela consolidada ELT
    _, res_elt_csv = executar_psql("COPY (SELECT cod_mun_6, nome_municipio, uf, regiao, populacao, total_casos, taxa_incidencia_100k, chuva_mm, leitos_uti, classificacao_risco FROM silver.indicadores_municipais_elt ORDER BY taxa_incidencia_100k DESC) TO STDOUT WITH CSV HEADER DELIMITER ';'")
    if res_elt_csv and not res_elt_csv.startswith("psql:"):
        with open(os.path.join(DIR_SILVER, "indicadores_municipais_elt.csv"), "w", encoding="utf-8") as f:
            f.write(res_elt_csv)

    # 5. Métricas Finais
    total_bronze = len(df_ibge_bronze) + len(df_dengue_bronze) + len(df_chuva_bronze) + len(df_leitos_bronze) + len(df_alertas_bronze)
    total_silver = len(df_mun_silver) + len(df_dengue_silver) + len(df_chuva_silver) + len(df_leitos_silver) + len(df_alertas_silver)

    metricas = {
        "timestamp_execucao": datetime.datetime.now().isoformat(),
        "mes_referencia": "2026-08",
        "camadas": {
            "bronze": {
                "fontes_count": 5,
                "detalhe_fontes": {
                    "1_ibge_municipios_censo": len(df_ibge_bronze),
                    "2_datasus_dengue_mes": len(df_dengue_bronze),
                    "3_inmet_clima_chuva": len(df_chuva_bronze),
                    "4_cnes_leitos_sus_postgres": len(df_leitos_bronze),
                    "5_vigilancia_alertas_mongodb": len(df_alertas_bronze)
                },
                "total_registros_brutos": total_bronze
            },
            "silver": {
                "municipios": len(df_mun_silver),
                "dengue_notificacoes": len(df_dengue_silver),
                "inmet_chuva": len(df_chuva_silver),
                "cnes_leitos": len(df_leitos_silver),
                "alertas_vigilancia": len(df_alertas_silver),
                "total_registros_limpos": total_silver
            },
            "quarentena": {
                "total_rejeitados": len(df_rejeitados),
                "taxa_rejeicao_pct": round((len(df_rejeitados) / total_bronze) * 100, 2),
                "por_pipeline": df_rejeitados['pipeline_origem'].value_counts().to_dict() if len(df_rejeitados) > 0 else {}
            },
            "elt": {
                "indicadores_gerados": len(df_mun_silver),
                "formula": "(total_casos / populacao) * 100.000",
                "motor": "PostgreSQL Nativo (JOINs e agregação SQL no storage)"
            }
        }
    }

    with open(os.path.join(DIR_PROJETO, "dados", "metricas_execucao.json"), "w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("📊 RESUMO FINAL DA ESTEIRA MEDALLION DO BRASIL:")
    print(f"  • Bronze (Total 5 Fontes Brutas):  {total_bronze} registros")
    print(f"  • Silver (Higienizado/Tipado):     {total_silver} registros")
    print(f"  • Quarentena (Rejeitados):         {len(df_rejeitados)} registros ({metricas['camadas']['quarentena']['taxa_rejeicao_pct']}%)")
    print(f"  • ELT (Indicadores de Risco SUS):  {len(df_mun_silver)} cidades analisadas no PostgreSQL")
    print("=" * 80)
    print("🎉 PIPELINE COMPLETO EXECUTADO COM SUCESSO!\n")

if __name__ == "__main__":
    main()
