#!/usr/bin/env python3
"""
scripts/gerar_dashboard.py
FIC Engenharia de Dados | Aula 03 (Módulo 2): Apache Hop & Orquestração

Gera o Dashboard Web Interativo de Alta Fidelidade (index.html) no padrão da Aula 13,
centrado nas Fontes de Dados Brasileiras com suporte completo a:
- Medallion Architecture (Bronze -> Staging -> Silver -> Quarentena -> Gold/ELT)
- Reconciliação e Arbitragem de Fontes Concorrentes (INMET Terrestre vs CPTEC Satélite)
- Orquestrador e Teste de Fogo MongoDB (Simulação UP vs DOWN)
- Central de Quarentena com filtros por causa raiz
- Padrão ELT vs ETL em PostgreSQL
- Produção Headless & Crontab
"""

import os
import json
import pandas as pd

DIR_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_DADOS = os.path.join(DIR_PROJETO, "dados")
CAMINHO_HTML = os.path.join(DIR_PROJETO, "index.html")

def carregar_dados():
    p_mun = os.path.join(DIR_DADOS, "silver", "municipios_silver.csv")
    p_dengue = os.path.join(DIR_DADOS, "silver", "dengue_silver.csv")
    p_chuva = os.path.join(DIR_DADOS, "silver", "chuva_silver.csv")
    p_leitos = os.path.join(DIR_DADOS, "silver", "cnes_leitos_silver.csv")
    p_alertas = os.path.join(DIR_DADOS, "silver", "alertas_silver.csv")
    p_indicadores = os.path.join(DIR_DADOS, "silver", "indicadores_municipais_elt.csv")
    p_clima_rec = os.path.join(DIR_DADOS, "silver", "clima_reconciliado.csv")
    p_rejeitados = os.path.join(DIR_DADOS, "quarentena", "rejeitados_detalhado.json")
    p_metricas = os.path.join(DIR_DADOS, "metricas_execucao.json")
    p_log_falha = os.path.join(DIR_DADOS, "teste_de_fogo_log_falha.txt")
    p_log_sucesso = os.path.join(DIR_DADOS, "teste_de_fogo_log_sucesso.txt")

    df_mun = pd.read_csv(p_mun, sep=";") if os.path.exists(p_mun) else pd.DataFrame()
    df_dengue = pd.read_csv(p_dengue, sep=";") if os.path.exists(p_dengue) else pd.DataFrame()
    df_chuva = pd.read_csv(p_chuva, sep=";") if os.path.exists(p_chuva) else pd.DataFrame()
    df_leitos = pd.read_csv(p_leitos, sep=";") if os.path.exists(p_leitos) else pd.DataFrame()
    df_alertas = pd.read_csv(p_alertas, sep=";") if os.path.exists(p_alertas) else pd.DataFrame()
    df_indicadores = pd.read_csv(p_indicadores, sep=";") if os.path.exists(p_indicadores) else pd.DataFrame()
    df_clima_rec = pd.read_csv(p_clima_rec, sep=";") if os.path.exists(p_clima_rec) else pd.DataFrame()

    with open(p_rejeitados, "r", encoding="utf-8") as f:
        rejeitados = json.load(f) if os.path.exists(p_rejeitados) else []

    with open(p_metricas, "r", encoding="utf-8") as f:
        metricas = json.load(f) if os.path.exists(p_metricas) else {}

    log_falha = ""
    if os.path.exists(p_log_falha):
        with open(p_log_falha, "r", encoding="utf-8") as f:
            log_falha = f.read()

    log_sucesso = ""
    if os.path.exists(p_log_sucesso):
        with open(p_log_sucesso, "r", encoding="utf-8") as f:
            log_sucesso = f.read()

    return {
        "df_mun": df_mun,
        "df_dengue": df_dengue,
        "df_chuva": df_chuva,
        "df_leitos": df_leitos,
        "df_alertas": df_alertas,
        "df_indicadores": df_indicadores,
        "df_clima_rec": df_clima_rec,
        "rejeitados": rejeitados,
        "metricas": metricas,
        "log_falha": log_falha,
        "log_sucesso": log_sucesso
    }

def gerar_dashboard():
    print("🎨 Gerando Dashboard Web Interativo com Reconciliação de Fontes (index.html)...")
    dados = carregar_dados()
    df_ind = dados["df_indicadores"]
    df_clima_rec = dados["df_clima_rec"]
    rejeitados = dados["rejeitados"]
    metricas = dados["metricas"]

    # Estatísticas Consolidadas
    total_populacao = int(df_ind['populacao'].sum()) if 'populacao' in df_ind.columns else 0
    total_casos = int(df_ind['total_casos'].sum()) if 'total_casos' in df_ind.columns else 0
    total_leitos_uti = int(df_ind['leitos_uti'].sum()) if 'leitos_uti' in df_ind.columns else 0
    media_chuva_mm = round(float(df_ind['chuva_mm'].mean()), 1) if 'chuva_mm' in df_ind.columns else 0.0
    taxa_media_incidencia = round(float(df_ind['taxa_incidencia_100k'].mean()), 2) if 'taxa_incidencia_100k' in df_ind.columns else 0.0

    # Agrupamentos para Gráficos
    regioes_casos = df_ind.groupby('regiao')['total_casos'].sum().to_dict() if 'regiao' in df_ind.columns else {}

    # Estatísticas de Arbitragem
    total_reconciliados = len(df_clima_rec)
    inmet_eleito_count = len(df_clima_rec[df_clima_rec['fonte_eleita'] == 'INMET_TERRESTRE']) if 'fonte_eleita' in df_clima_rec.columns else 0
    cptec_eleito_count = len(df_clima_rec[df_clima_rec['fonte_eleita'] == 'CPTEC_SATELITE']) if 'fonte_eleita' in df_clima_rec.columns else 0

    # Motivos de Quarentena
    motivos_rejeicao = {}
    for r in rejeitados:
        m = r['motivo_erro'].split('(')[0].strip()
        motivos_rejeicao[m] = motivos_rejeicao.get(m, 0) + 1

    payload_json = {
        "metricas": metricas,
        "indicadores": df_ind.to_dict(orient="records"),
        "clima_reconciliado": df_clima_rec.to_dict(orient="records"),
        "rejeitados": rejeitados,
        "motivos_rejeicao": motivos_rejeicao,
        "regioes_casos": regioes_casos,
        "total_populacao": total_populacao,
        "total_casos": total_casos,
        "total_leitos_uti": total_leitos_uti,
        "media_chuva_mm": media_chuva_mm,
        "taxa_media_incidencia": taxa_media_incidencia,
        "total_reconciliados": total_reconciliados,
        "inmet_eleito_count": inmet_eleito_count,
        "cptec_eleito_count": cptec_eleito_count,
        "log_falha": dados["log_falha"],
        "log_sucesso": dados["log_sucesso"]
    }

    payload_js_str = json.dumps(payload_json, ensure_ascii=False)

    html_code = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Observatório Medallion &amp; Orquestração Hop | Dados do Brasil</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {{
      --bg-base: #080c14;
      --bg-surface: rgba(15, 23, 42, 0.85);
      --bg-surface-elevated: rgba(30, 41, 59, 0.95);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(56, 189, 248, 0.3);
      --primary: #38bdf8;
      --primary-glow: rgba(56, 189, 248, 0.25);
      --secondary: #818cf8;
      --accent: #22c55e;
      --accent-warning: #f59e0b;
      --accent-danger: #ef4444;
      --accent-purple: #c084fc;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --font-sans: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
      --shadow-glow: 0 0 25px -5px var(--primary-glow);
    }}

    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}

    body {{
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.5;
      min-height: 100vh;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 15% 10%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(129, 140, 248, 0.07) 0%, transparent 45%);
      background-attachment: fixed;
    }}

    header.top-bar {{
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      background: rgba(8, 12, 20, 0.85);
      border-bottom: 1px solid var(--border-subtle);
      padding: 14px 32px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .brand-logo {{
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }}

    .brand-text h1 {{
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #fff;
    }}

    .brand-text p {{
      font-size: 0.78rem;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }}

    .badge-status {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: rgba(34, 197, 94, 0.12);
      border: 1px solid rgba(34, 197, 94, 0.3);
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 600;
      color: #4ade80;
      font-family: var(--font-mono);
    }}

    .status-dot {{
      width: 8px;
      height: 8px;
      background-color: #22c55e;
      border-radius: 50%;
      box-shadow: 0 0 8px #22c55e;
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0% {{ transform: scale(0.95); opacity: 0.8; }}
      50% {{ transform: scale(1.2); opacity: 1; }}
      100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}

    .container {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 28px 32px 60px;
    }}

    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
      margin-bottom: 28px;
    }}

    .kpi-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      backdrop-filter: blur(12px);
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }}

    .kpi-card:hover {{
      transform: translateY(-3px);
      border-color: var(--border-accent);
      box-shadow: var(--shadow-glow);
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: linear-gradient(90deg, transparent, var(--primary), transparent);
      opacity: 0;
      transition: opacity 0.3s;
    }}

    .kpi-card:hover::before {{
      opacity: 1;
    }}

    .kpi-title {{
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .kpi-value {{
      font-size: 1.85rem;
      font-weight: 800;
      color: #fff;
      font-family: var(--font-mono);
      letter-spacing: -0.03em;
    }}

    .kpi-subtext {{
      font-size: 0.75rem;
      color: var(--text-dim);
      margin-top: 6px;
    }}

    .tab-bar {{
      display: flex;
      gap: 10px;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 26px;
      padding-bottom: 12px;
      overflow-x: auto;
    }}

    .tab-btn {{
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 600;
      padding: 10px 20px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }}

    .tab-btn:hover {{
      color: #fff;
      background: rgba(255, 255, 255, 0.04);
    }}

    .tab-btn.active {{
      color: var(--primary);
      background: rgba(56, 189, 248, 0.1);
      border-color: rgba(56, 189, 248, 0.3);
    }}

    .tab-content {{
      display: none;
    }}

    .tab-content.active {{
      display: block;
      animation: fadeIn 0.3s ease;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .panel {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 24px;
      backdrop-filter: blur(12px);
      margin-bottom: 24px;
    }}

    .panel-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border-subtle);
    }}

    .panel-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .medallion-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1024px) {{
      .medallion-grid {{ grid-template-columns: 1fr; }}
    }}

    .medallion-col {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 18px;
    }}

    .medallion-col.bronze {{ border-top: 3px solid #f97316; }}
    .medallion-col.staging {{ border-top: 3px solid #38bdf8; }}
    .medallion-col.silver {{ border-top: 3px solid #a855f7; }}
    .medallion-col.gold {{ border-top: 3px solid #22c55e; }}

    .medallion-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }}

    .medallion-badge {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 4px 10px;
      border-radius: 999px;
      font-family: var(--font-mono);
    }}

    .badge-bronze {{ background: rgba(249, 115, 22, 0.15); color: #fb923c; }}
    .badge-staging {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; }}
    .badge-silver {{ background: rgba(168, 85, 247, 0.15); color: #c084fc; }}
    .badge-gold {{ background: rgba(34, 197, 94, 0.15); color: #4ade80; }}

    .source-item {{
      background: rgba(30, 41, 59, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: var(--radius-sm);
      padding: 10px 12px;
      margin-bottom: 10px;
      font-size: 0.8rem;
    }}

    .source-item .title {{
      font-weight: 600;
      color: #fff;
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;
    }}

    .source-item .desc {{
      color: var(--text-dim);
      font-size: 0.74rem;
      font-family: var(--font-mono);
    }}

    /* Workflow Diagram & Fire Test Simulator */
    .workflow-container {{
      background: #050811;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 24px;
      position: relative;
    }}

    .workflow-controls {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
      padding: 14px 18px;
      background: rgba(30, 41, 59, 0.6);
      border-radius: var(--radius-sm);
      border: 1px solid rgba(255, 255, 255, 0.05);
    }}

    .switch-group {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}

    .toggle-btn {{
      padding: 8px 18px;
      border-radius: var(--radius-sm);
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      font-family: var(--font-mono);
    }}

    .toggle-btn.active-green {{
      background: rgba(34, 197, 94, 0.2);
      border-color: #22c55e;
      color: #4ade80;
      box-shadow: 0 0 12px rgba(34, 197, 94, 0.3);
    }}

    .toggle-btn.active-red {{
      background: rgba(239, 68, 68, 0.2);
      border-color: #ef4444;
      color: #f87171;
      box-shadow: 0 0 12px rgba(239, 68, 68, 0.3);
    }}

    .toggle-btn:not(.active-green):not(.active-red) {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-dim);
    }}

    .flow-steps {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 12px;
      padding: 24px 0;
    }}

    .flow-node {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 12px 16px;
      min-width: 140px;
      text-align: center;
      transition: all 0.3s;
    }}

    .flow-node.highlight-green {{
      border-color: #22c55e;
      box-shadow: 0 0 15px rgba(34, 197, 94, 0.3);
    }}

    .flow-node.highlight-red {{
      border-color: #ef4444;
      box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
    }}

    .flow-node.dimmed {{
      opacity: 0.35;
    }}

    .flow-arrow {{
      color: var(--text-dim);
      font-size: 1.2rem;
    }}

    .flow-arrow.green {{ color: #22c55e; font-weight: bold; }}
    .flow-arrow.red {{ color: #ef4444; font-weight: bold; }}

    .terminal-window {{
      background: #040711;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-sm);
      overflow: hidden;
      font-family: var(--font-mono);
      margin-top: 16px;
    }}

    .terminal-bar {{
      background: #0d1322;
      padding: 8px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      font-size: 0.74rem;
      color: var(--text-dim);
    }}

    .terminal-dots {{ display: flex; gap: 6px; }}
    .t-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
    .t-red {{ background: #ef4444; }}
    .t-yellow {{ background: #f59e0b; }}
    .t-green {{ background: #22c55e; }}

    .terminal-body {{
      padding: 16px;
      font-size: 0.78rem;
      color: #94a3b8;
      max-height: 280px;
      overflow-y: auto;
      white-space: pre-wrap;
      line-height: 1.45;
    }}

    .quarantine-filters {{
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}

    .q-filter-btn {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 0.75rem;
      cursor: pointer;
      font-family: var(--font-mono);
      transition: all 0.2s;
    }}

    .q-filter-btn:hover {{
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }}

    .q-filter-btn.active {{
      background: rgba(239, 68, 68, 0.15);
      border-color: rgba(239, 68, 68, 0.4);
      color: #fca5a5;
    }}

    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
      text-align: left;
    }}

    table.data-table th {{
      background: rgba(30, 41, 59, 0.6);
      color: var(--text-muted);
      font-weight: 600;
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
      font-family: var(--font-mono);
      font-size: 0.74rem;
      text-transform: uppercase;
    }}

    table.data-table td {{
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: #cbd5e1;
    }}

    table.data-table tr:hover td {{
      background: rgba(255, 255, 255, 0.02);
    }}

    .tag-risk {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }}

    .risk-baixo {{ background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }}
    .risk-medio {{ background: rgba(245, 158, 11, 0.15); color: #fcd34d; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .risk-alto {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }}

    .badge-inmet {{
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid rgba(56, 189, 248, 0.4);
      color: #38bdf8;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }}

    .badge-cptec {{
      background: rgba(168, 85, 247, 0.15);
      border: 1px solid rgba(168, 85, 247, 0.4);
      color: #c084fc;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      font-family: var(--font-mono);
    }}

    .charts-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}

    @media (max-width: 1024px) {{
      .charts-grid {{ grid-template-columns: 1fr; }}
    }}

    .chart-box {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      position: relative;
    }}

    .chart-title {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #fff;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .comparison-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 24px;
    }}

    @media (max-width: 800px) {{
      .comparison-grid {{ grid-template-columns: 1fr; }}
    }}

    .comparison-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 24px;
    }}

    .comparison-card.etl {{ border-left: 4px solid #f59e0b; }}
    .comparison-card.elt {{ border-left: 4px solid #22c55e; }}

    .comparison-card h3 {{
      font-size: 1.1rem;
      font-weight: 800;
      margin-bottom: 8px;
    }}

    .comparison-card p.subtitle {{
      color: var(--text-dim);
      font-size: 0.8rem;
      margin-bottom: 16px;
    }}

    .comp-item {{
      margin-bottom: 12px;
      font-size: 0.82rem;
    }}

    .comp-item strong {{
      color: #fff;
      display: block;
      margin-bottom: 2px;
    }}

    .code-snippet {{
      background: #050811;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: var(--radius-sm);
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: #38bdf8;
      position: relative;
      margin: 12px 0 20px;
    }}

    .copy-btn {{
      position: absolute;
      top: 10px;
      right: 10px;
      background: rgba(255, 255, 255, 0.08);
      border: none;
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.72rem;
    }}

    .copy-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }}
  </style>
</head>
<body>

  <!-- Top Bar -->
  <header class="top-bar">
    <div class="brand">
      <div class="brand-logo">🇧🇷</div>
      <div class="brand-text">
        <h1>Observatório Medallion &amp; Orquestração Hop</h1>
        <p>FIC Engenharia de Dados • Aula 03 (Módulo 2) • Dados Nacionais do Brasil</p>
      </div>
    </div>
    <div class="top-actions">
      <span class="badge-status">
        <span class="status-dot"></span>
        PIPELINE ATIVO &amp; HOMOLOGADO
      </span>
    </div>
  </header>

  <div class="container">

    <!-- KPI Ribbon -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">
          <span>População Monitorada</span>
          <span>👥</span>
        </div>
        <div class="kpi-value" id="kpi-populacao">{total_populacao:,}</div>
        <div class="kpi-subtext">20 Municípios Estratégicos (IBGE)</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Notificações Dengue</span>
          <span>🦟</span>
        </div>
        <div class="kpi-value" id="kpi-casos" style="color: #f87171;">{total_casos:,}</div>
        <div class="kpi-subtext">Período {metricas.get('mes_referencia', '2026-08')} (DataSUS)</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Fontes Concorrentes</span>
          <span>⚖️</span>
        </div>
        <div class="kpi-value" id="kpi-arbitragem" style="color: #38bdf8;">2 Fontes</div>
        <div class="kpi-subtext">INMET (Física) vs CPTEC (Satélite)</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Leitos UTI SUS</span>
          <span>🏥</span>
        </div>
        <div class="kpi-value" id="kpi-leitos" style="color: #22c55e;">{total_leitos_uti:,}</div>
        <div class="kpi-subtext">Rede Hospitalar (CNES SUS)</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-title">
          <span>Quarentena Isolada</span>
          <span>🛡️</span>
        </div>
        <div class="kpi-value" id="kpi-quarentena" style="color: #a855f7;">{len(rejeitados)} reg</div>
        <div class="kpi-subtext">Erros e Conflitos Isolados</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchTab('tab-visao-geral')">🌐 Visão Geral Medallion</button>
      <button class="tab-btn" onclick="switchTab('tab-arbitragem')">⚖️ Arbitragem de Fontes (INMET vs CPTEC)</button>
      <button class="tab-btn" onclick="switchTab('tab-orquestracao')">⚡ Orquestração Hop &amp; Teste de Fogo</button>
      <button class="tab-btn" onclick="switchTab('tab-quarentena')">🛡️ Quarentena de Erros ({len(rejeitados)})</button>
      <button class="tab-btn" onclick="switchTab('tab-analise-elt')">💡 Padrão ELT vs ETL</button>
      <button class="tab-btn" onclick="switchTab('tab-producao')">⚙️ Produção &amp; Crontab</button>
    </div>

    <!-- TAB 1: VISÃO GERAL MEDALLION -->
    <div id="tab-visao-geral" class="tab-content active">
      <div class="medallion-grid">
        <div class="medallion-col bronze">
          <div class="medallion-header">
            <span class="medallion-badge badge-bronze">1. Bronze (Raw)</span>
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #fb923c;">Multi-Fontes</span>
          </div>
          <div class="source-item">
            <div class="title"><span>IBGE Municípios</span><span>CSV</span></div>
            <div class="desc">23 cidades brasileiras brutas</div>
          </div>
          <div class="source-item">
            <div class="title"><span>DataSUS Dengue</span><span>CSV</span></div>
            <div class="desc">24 notificações ref: 2026-08</div>
          </div>
          <div class="source-item">
            <div class="title"><span>INMET Clima / Chuva</span><span>CSV</span></div>
            <div class="desc">22 leituras pluviométricas mm</div>
          </div>
          <div class="source-item">
            <div class="title"><span>CNES Leitos SUS</span><span>RDBMS</span></div>
            <div class="desc">20 hospitais e UTIs locais</div>
          </div>
          <div class="source-item">
            <div class="title"><span>Vigilância Alertas</span><span>NoSQL</span></div>
            <div class="desc">10 alertas epidemiológicos Mongo</div>
          </div>
        </div>

        <div class="medallion-col staging">
          <div class="medallion-header">
            <span class="medallion-badge badge-staging">2. Staging</span>
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #38bdf8;">Idempotente</span>
          </div>
          <div class="source-item">
            <div class="title"><span>TRUNCATE staging.*</span><span>SQL</span></div>
            <div class="desc">Garante reexecução sem duplicidade</div>
          </div>
          <div class="source-item">
            <div class="title"><span>Tabelas Intermediárias</span><span>PostgreSQL</span></div>
            <div class="desc">staging.ibge_municipios<br>staging.datasus_dengue<br>staging.inmet_temperatura<br>staging.cptec_temperatura</div>
          </div>
          <div class="source-item">
            <div class="title"><span>Tipagem Ampla</span><span>TEXT</span></div>
            <div class="desc">Recebe dados íntegros e anômalos</div>
          </div>
        </div>

        <div class="medallion-col silver">
          <div class="medallion-header">
            <span class="medallion-badge badge-silver">3. Silver &amp; Quarentena</span>
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #c084fc;">Higienizado</span>
          </div>
          <div class="source-item">
            <div class="title"><span>silver.municipios</span><span>20 reg</span></div>
            <div class="desc">Nome capitalizado, UF maiúscula</div>
          </div>
          <div class="source-item">
            <div class="title"><span>silver.clima_reconciliado</span><span>20 reg</span></div>
            <div class="desc">Golden Record INMET + CPTEC</div>
          </div>
          <div class="source-item">
            <div class="title"><span>silver.rejeitados</span><span>{len(rejeitados)} reg</span></div>
            <div class="desc">Quarentena isolada com rastreio</div>
          </div>
        </div>

        <div class="medallion-col gold">
          <div class="medallion-header">
            <span class="medallion-badge badge-gold">4. Gold (ELT Nativo)</span>
            <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #4ade80;">20 cidades</span>
          </div>
          <div class="source-item">
            <div class="title"><span>Taxa de Incidência</span><span>SQL</span></div>
            <div class="desc">(total_casos / populacao) * 100k</div>
          </div>
          <div class="source-item">
            <div class="title"><span>Classificação de Risco</span><span>CASE</span></div>
            <div class="desc">Muito Alto (&gt;300), Médio, Baixo</div>
          </div>
          <div class="source-item">
            <div class="title"><span>UPSERT Idempotente</span><span>ON CONFLICT</span></div>
            <div class="desc">Gravação atômica direta no banco</div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-grid">
        <div class="chart-box">
          <div class="chart-title">
            <span>Ranking de Incidência de Dengue por 100k Habitantes (Taxa Epidemiológica)</span>
            <span style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono);">ELT PostgreSQL</span>
          </div>
          <canvas id="chartIncidencia" height="150"></canvas>
        </div>

        <div class="chart-box">
          <div class="chart-title">
            <span>Casos por Região do Brasil</span>
            <span style="font-size: 0.75rem; color: var(--text-dim); font-family: var(--font-mono);">Distribuição</span>
          </div>
          <canvas id="chartRegioes" height="150"></canvas>
        </div>
      </div>

      <!-- Municipal Table -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span>Tabela Analítica Consolidada: Indicadores Municipais de Saúde e Clima</span>
          </div>
          <input type="text" id="filtroCidade" placeholder="🔍 Filtrar município ou UF..." onkeyup="filtrarTabelaCidades()" style="background: rgba(255,255,255,0.05); border: 1px solid var(--border-subtle); color: #fff; padding: 6px 14px; border-radius: var(--radius-sm); font-size: 0.8rem; font-family: var(--font-mono);">
        </div>
        <div style="overflow-x: auto;">
          <table class="data-table" id="tabelaCidades">
            <thead>
              <tr>
                <th>Cód IBGE</th>
                <th>Município</th>
                <th>UF</th>
                <th>Região</th>
                <th>População</th>
                <th>Casos Dengue</th>
                <th>Taxa / 100k</th>
                <th>Chuva (mm)</th>
                <th>Leitos UTI</th>
                <th>Classificação de Risco</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: ARBITRAGEM DE FONTES CONCORRENTES (NOVO WORKFLOW / MOTOR DE DECISÃO) -->
    <div id="tab-arbitragem" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span>Motor de Decisão &amp; Arbitragem: Duas Fontes de Temperatura (INMET vs CPTEC)</span>
          </div>
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #38bdf8;">Tabela: silver.clima_reconciliado</span>
        </div>

        <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 20px;">
          Neste fluxo, o sistema recebe simultaneamente duas medições de temperatura para o mesmo município: 
          <strong>Fonte A (INMET Terrestre)</strong> e <strong>Fonte B (CPTEC Satélite)</strong>. O workflow e a pipeline analisam a qualidade de cada leitura e decidem de forma determinística qual dado será promovido a <strong>Golden Record</strong>:
        </p>

        <!-- KPI da Arbitragem -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-bottom: 22px;">
          <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 14px;">
            <div style="font-size: 0.74rem; color: var(--text-muted); text-transform: uppercase;">Total Reconciliado</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #fff; font-family: var(--font-mono);">{total_reconciliados} cidades</div>
            <div style="font-size: 0.72rem; color: var(--text-dim);">Cobertura 100% dos municípios</div>
          </div>

          <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: var(--radius-sm); padding: 14px;">
            <div style="font-size: 0.74rem; color: #38bdf8; text-transform: uppercase;">INMET Eleito (Nominal)</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #38bdf8; font-family: var(--font-mono);">{inmet_eleito_count} cidades ({round(inmet_eleito_count/total_reconciliados*100 if total_reconciliados else 0)}%)</div>
            <div style="font-size: 0.72rem; color: var(--text-dim);">Sensor físico validado como primário</div>
          </div>

          <div style="background: rgba(168, 85, 247, 0.08); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: var(--radius-sm); padding: 14px;">
            <div style="font-size: 0.74rem; color: #c084fc; text-transform: uppercase;">CPTEC Eleito (Fallback)</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #c084fc; font-family: var(--font-mono);">{cptec_eleito_count} cidades ({round(cptec_eleito_count/total_reconciliados*100 if total_reconciliados else 0)}%)</div>
            <div style="font-size: 0.72rem; color: var(--text-dim);">Satélite acionado por falha do sensor de solo</div>
          </div>

          <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: var(--radius-sm); padding: 14px;">
            <div style="font-size: 0.74rem; color: #f87171; text-transform: uppercase;">Anomalias em Quarentena</div>
            <div style="font-size: 1.5rem; font-weight: 800; color: #f87171; font-family: var(--font-mono);">2 sensores</div>
            <div style="font-size: 0.72rem; color: var(--text-dim);">Salvador (99.9°C) e Campinas (-85.0°C)</div>
          </div>
        </div>

        <!-- Regras Explicadas -->
        <div style="background: #050811; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 16px; margin-bottom: 22px; font-size: 0.82rem;">
          <strong style="color: #fff;">Lógica de Decisão do Motor de Arbitragem:</strong>
          <ul style="margin-left: 20px; margin-top: 8px; color: var(--text-muted); line-height: 1.6;">
            <li><strong>Regra 1 (Prioridade Oficial):</strong> O sensor físico do INMET tem preferência. Se for válido (entre -10°C e 50°C), ele é adotado.</li>
            <li><strong>Regra 2 (Fallback Automático):</strong> Se o sensor INMET estiver nulo/offline (ex: Manaus e Porto Alegre), o CPTEC Satélite assume para evitar dado faltante.</li>
            <li><strong>Regra 3 (Isolamento de Anomalia):</strong> Se o sensor INMET registrar um valor absurdo (ex: Salvador marcando 99.9°C ou Campinas marcando -85.0°C), a medição doente vai para a <strong>Quarentena</strong> e o satélite do CPTEC é eleito para a cidade.</li>
          </ul>
        </div>

        <!-- Tabela Lado a Lado da Arbitragem -->
        <div class="panel-header" style="border: none; padding-bottom: 0;">
          <strong style="color: #fff; font-size: 0.95rem;">Comparativo Lado a Lado: INMET vs CPTEC e Decisão Final</strong>
          <input type="text" id="filtroArbitragem" placeholder="🔍 Filtrar cidade ou status..." onkeyup="filtrarTabelaArbitragem()" style="background: rgba(255,255,255,0.05); border: 1px solid var(--border-subtle); color: #fff; padding: 6px 14px; border-radius: var(--radius-sm); font-size: 0.8rem; font-family: var(--font-mono);">
        </div>

        <div style="overflow-x: auto; margin-top: 14px;">
          <table class="data-table" id="tabelaArbitragem">
            <thead>
              <tr>
                <th>Cód IBGE</th>
                <th>Município</th>
                <th>Temp. INMET (Terrestre)</th>
                <th>Temp. CPTEC (Satélite)</th>
                <th>Temperatura Eleita</th>
                <th>Fonte Vencedora</th>
                <th>Status Auditável da Decisão</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>

        <!-- Informação do Novo Workflow -->
        <div style="margin-top: 24px; padding: 16px; background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: var(--radius-sm);">
          <strong style="color: #38bdf8; font-size: 0.85rem;">📁 Novo Workflow Dedicado Criado no Hop:</strong>
          <p style="color: var(--text-muted); font-size: 0.78rem; margin-top: 4px; font-family: var(--font-mono);">
            Arquivo: hop/workflows/workflow_arbitragem_concorrente.hwf<br>
            Comando CLI: /home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh -j ecommerce -f ${{PROJECT_HOME}}/hop/workflows/workflow_arbitragem_concorrente.hwf -r local
          </p>
        </div>
      </div>
    </div>

    <!-- TAB 3: ORQUESTRAÇÃO HOP & TESTE DE FOGO -->
    <div id="tab-orquestracao" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span>Simulador Interativo do Workflow Mestre: Apache Hop 2.19 (carga_diaria.hwf)</span>
          </div>
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--primary);">Passo 2 &amp; 3 do Roteiro</span>
        </div>

        <div class="workflow-container">
          <div class="workflow-controls">
            <div>
              <strong style="color: #fff; font-size: 0.9rem;">Simulação do Teste de Fogo (Passo 3):</strong>
              <p style="color: var(--text-dim); font-size: 0.75rem;">Alterne a disponibilidade do MongoDB para visualizar a rota de desvio divergente no Hop.</p>
            </div>
            <div class="switch-group">
              <button id="btnMongoUp" class="toggle-btn active-green" onclick="simularFogo(true)">🟢 MongoDB UP (Normal)</button>
              <button id="btnMongoDown" class="toggle-btn" onclick="simularFogo(false)">🔴 MongoDB DOWN (Simular Queda)</button>
            </div>
          </div>

          <div class="flow-steps">
            <div class="flow-node highlight-green" id="node-start">
              <div style="font-size: 0.7rem; color: var(--text-muted);">SPECIAL</div>
              <strong style="font-size: 0.82rem;">Start</strong>
            </div>
            <div class="flow-arrow green" id="arr-1">➜</div>

            <div class="flow-node highlight-green" id="node-truncate">
              <div style="font-size: 0.7rem; color: var(--text-muted);">SQL ACTION</div>
              <strong style="font-size: 0.82rem;">Truncate Staging</strong>
            </div>
            <div class="flow-arrow green" id="arr-2">➜</div>

            <div class="flow-node highlight-green" id="node-ext">
              <div style="font-size: 0.7rem; color: var(--text-muted);">EXTRAÇÕES</div>
              <strong style="font-size: 0.82rem;">Fontes Bronze</strong>
            </div>
            <div class="flow-arrow green" id="arr-3">➜</div>

            <div class="flow-node highlight-green" id="node-mongo">
              <div style="font-size: 0.7rem; color: var(--text-muted);">SHELL PING</div>
              <strong style="font-size: 0.82rem;">Mongo Alertas (Fogo)</strong>
            </div>
            <div class="flow-arrow green" id="arr-4">➜</div>

            <div class="flow-node highlight-green" id="node-silver">
              <div style="font-size: 0.7rem; color: var(--text-muted);">PIPELINES</div>
              <strong style="font-size: 0.82rem;">Silver &amp; Quarentena</strong>
            </div>
            <div class="flow-arrow green" id="arr-5">➜</div>

            <div class="flow-node highlight-green" id="node-elt">
              <div style="font-size: 0.7rem; color: var(--text-muted);">SQL ACTION</div>
              <strong style="font-size: 0.82rem;">ELT Indicadores</strong>
            </div>
            <div class="flow-arrow green" id="arr-6">➜</div>

            <div class="flow-node highlight-green" id="node-success">
              <div style="font-size: 0.7rem; color: #4ade80;">LOG / SUCCESS</div>
              <strong style="font-size: 0.82rem;">Sucesso Completo</strong>
            </div>

            <div class="flow-node dimmed" id="node-abort" style="margin-top: 16px; border-color: #ef4444; width: 100%;">
              <div style="font-size: 0.7rem; color: #f87171;">FLUXO VERMELHO DE CONTINGÊNCIA</div>
              <strong style="font-size: 0.85rem; color: #fca5a5;">Log de Erro Convergente ➜ Action ABORT (Código != 0)</strong>
            </div>
          </div>

          <div class="terminal-window">
            <div class="terminal-bar">
              <div class="terminal-dots">
                <span class="t-dot t-red"></span>
                <span class="t-dot t-yellow"></span>
                <span class="t-dot t-green"></span>
              </div>
              <span id="terminal-title">Log Real do Apache Hop: Caminho Verde (Sucesso 100%)</span>
              <span style="font-family: var(--font-mono); font-size: 0.7rem;">hop-run.sh CLI</span>
            </div>
            <div class="terminal-body" id="terminal-log"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: QUARENTENA DE ERROS -->
    <div id="tab-quarentena" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span>Central de Isolamento de Dados Anômalos: Quarentena Silver (Passo 1 do Roteiro)</span>
          </div>
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #f87171;">Tabela: silver.rejeitados</span>
        </div>

        <p style="color: var(--text-muted); font-size: 0.82rem; margin-bottom: 16px;">
          Nenhum dado é descartado silenciosamente. Erros de contratação, formatação ou sensores implausíveis são isolados com auditoria completa.
        </p>

        <div class="quarantine-filters">
          <button class="q-filter-btn active" onclick="filtrarQuarentena('TODOS')">Todos ({len(rejeitados)})</button>
          <button class="q-filter-btn" onclick="filtrarQuarentena('reconciliacao_temperatura_arbitragem')">Sensores Arbitragem (2)</button>
          <button class="q-filter-btn" onclick="filtrarQuarentena('padroniza_datasus_dengue')">DataSUS Dengue (3)</button>
          <button class="q-filter-btn" onclick="filtrarQuarentena('padroniza_ibge_municipios')">IBGE Municípios (2)</button>
          <button class="q-filter-btn" onclick="filtrarQuarentena('padroniza_inmet_chuva')">INMET Chuva (2)</button>
          <button class="q-filter-btn" onclick="filtrarQuarentena('padroniza_alertas_vigilancia')">Alertas Mongo (1)</button>
        </div>

        <div style="overflow-x: auto;">
          <table class="data-table" id="tabelaQuarentena">
            <thead>
              <tr>
                <th>Pipeline Origem</th>
                <th>Motivo do Erro / Falha de Contrato</th>
                <th>Registro Bruto Isolado</th>
                <th>Data Rejeição</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 5: PADRÃO ELT VS ETL -->
    <div id="tab-analise-elt" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span>Comparativo Arquitetural: Padrão ETL Tradicional vs Padrão ELT Moderno</span>
          </div>
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #4ade80;">Passo 5: Desafio de Fixação</span>
        </div>

        <div class="comparison-grid">
          <div class="comparison-card etl">
            <h3 style="color: #fbbf24;">Padrão Tradicional (ETL)</h3>
            <p class="subtitle">Extract ➜ Transform (na Engine) ➜ Load</p>
            <div class="comp-item">
              <strong>Motor de Processamento:</strong>
              Memória do Apache Hop / servidor de ETL externo. Linha a linha.
            </div>
            <div class="comp-item">
              <strong>Gargalo Principal:</strong>
              Transferência contínua de grandes volumes pela rede (I/O) e limitações de RAM da JVM.
            </div>
            <div class="comp-item">
              <strong>Tratamento de Mudanças de Regra:</strong>
              Requer reprocessar todo o pipeline desde a extração na fonte original.
            </div>
          </div>

          <div class="comparison-card elt">
            <h3 style="color: #4ade80;">Padrão Moderno (ELT) — Implementado</h3>
            <p class="subtitle">Extract ➜ Load (Staging) ➜ Transform (no PostgreSQL)</p>
            <div class="comp-item">
              <strong>Motor de Processamento:</strong>
              Engine colunar / relacional do PostgreSQL (query planner, índices, multithreading).
            </div>
            <div class="comp-item">
              <strong>Vantagem de Performance:</strong>
              Transformação vetorial e cálculo em lote sem tráfego desnecessário de rede.
            </div>
            <div class="comp-item">
              <strong>Tratamento de Mudanças de Regra:</strong>
              Basta rodar um novo script SQL diretamente sobre as tabelas Staging ou Silver já armazenadas.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 6: PRODUÇÃO & CRONTAB -->
    <div id="tab-producao" class="tab-content">
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span>Guia de Execução Headless &amp; Agendamento em Produção (Passo 4 do Roteiro)</span>
          </div>
          <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #38bdf8;">hop-run.sh + Crontab</span>
        </div>

        <h4 style="color: #fff; font-size: 0.9rem; margin-top: 18px; margin-bottom: 6px;">1. Execução do Workflow de Arbitragem de Fontes Concorrentes:</h4>
        <div class="code-snippet">
          <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('cmd-hop-run-rec').innerText)">Copiar</button>
          <pre id="cmd-hop-run-rec">/home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh \\
  -j ecommerce \\
  -f /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-14-padronizacao-workflows-hop/hop/workflows/workflow_arbitragem_concorrente.hwf \\
  -r local</pre>
        </div>

        <h4 style="color: #fff; font-size: 0.9rem; margin-top: 18px; margin-bottom: 6px;">2. Execução do Workflow Mestre Geral (com ${{MES_REF}}):</h4>
        <div class="code-snippet">
          <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('cmd-hop-run').innerText)">Copiar</button>
          <pre id="cmd-hop-run">/home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh \\
  -j ecommerce \\
  -f /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-14-padronizacao-workflows-hop/hop/workflows/carga_diaria.hwf \\
  -r local \\
  -p MES_REF=2026-08</pre>
        </div>

        <h4 style="color: #fff; font-size: 0.9rem; margin-top: 18px; margin-bottom: 6px;">3. Agendamento Noturno no Crontab (03:00 da manhã):</h4>
        <div class="code-snippet">
          <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('cmd-cron').innerText)">Copiar</button>
          <pre id="cmd-cron">0 3 * * * MES_REF=$(date +\\%Y-\\%m) /home/ficdevia-16-tarde/Downloads/apache-hop-client-2.19.0/hop/hop-run.sh -j ecommerce -f /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-14-padronizacao-workflows-hop/hop/workflows/carga_diaria.hwf -r local -p MES_REF=$MES_REF >> /home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-14-padronizacao-workflows-hop/logs/cron_carga_diaria.log 2>&1</pre>
        </div>
      </div>
    </div>

  </div>

  <!-- Javascript Logic -->
  <script>
    const DADOS = {payload_js_str};

    function switchTab(tabId) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      
      const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick').includes(tabId));
      if (btn) btn.classList.add('active');
      
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');
    }}

    // Renderiza Tabela de Cidades
    function renderTabelaCidades(lista) {{
      const tbody = document.querySelector('#tabelaCidades tbody');
      tbody.innerHTML = '';

      lista.forEach(item => {{
        const tr = document.createElement('tr');
        let badgeClass = 'risk-baixo';
        if (item.classificacao_risco === 'Alto Risco') badgeClass = 'risk-alto';
        else if (item.classificacao_risco === 'Médio Risco') badgeClass = 'risk-medio';

        tr.innerHTML = `
          <td style="font-family: var(--font-mono); font-weight: 600;">${{item.cod_mun_6}}</td>
          <td style="font-weight: 700; color: #fff;">${{item.nome_municipio}}</td>
          <td><span style="font-family: var(--font-mono); background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px;">${{item.uf}}</span></td>
          <td>${{item.regiao}}</td>
          <td style="font-family: var(--font-mono);">${{Number(item.populacao).toLocaleString('pt-BR')}}</td>
          <td style="font-family: var(--font-mono); font-weight: 700; color: #f87171;">${{Number(item.total_casos).toLocaleString('pt-BR')}}</td>
          <td style="font-family: var(--font-mono); font-weight: 700; color: #fbbf24;">${{item.taxa_incidencia_100k}}</td>
          <td style="font-family: var(--font-mono);">${{item.chuva_mm}} mm</td>
          <td style="font-family: var(--font-mono);">${{item.leitos_uti}}</td>
          <td><span class="tag-risk ${{badgeClass}}">${{item.classificacao_risco}}</span></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function filtrarTabelaCidades() {{
      const query = document.getElementById('filtroCidade').value.toLowerCase();
      const filtradas = DADOS.indicadores.filter(c => 
        c.nome_municipio.toLowerCase().includes(query) || 
        c.uf.toLowerCase().includes(query) ||
        c.regiao.toLowerCase().includes(query)
      );
      renderTabelaCidades(filtradas);
    }}

    // Renderiza Tabela de Arbitragem de Temperatura
    function renderTabelaArbitragem(lista) {{
      const tbody = document.querySelector('#tabelaArbitragem tbody');
      tbody.innerHTML = '';

      lista.forEach(item => {{
        const tr = document.createElement('tr');
        const inmetVal = item.temp_inmet_original !== null && item.temp_inmet_original !== undefined ? `${{Number(item.temp_inmet_original).toFixed(1)}}°C` : '<span style="color: #f87171; font-style: italic;">Nulo / Offline</span>';
        const cptecVal = `${{Number(item.temp_cptec_original).toFixed(1)}}°C`;
        const eleitaVal = `${{Number(item.temperatura_eleita).toFixed(1)}}°C`;

        let badgeFonte = item.fonte_eleita === 'INMET_TERRESTRE' 
          ? '<span class="badge-inmet">INMET Terrestre</span>'
          : '<span class="badge-cptec">CPTEC Satélite (Fallback)</span>';

        tr.innerHTML = `
          <td style="font-family: var(--font-mono); font-weight: 600;">${{item.cod_mun_6}}</td>
          <td style="font-weight: 700; color: #fff;">${{item.municipio}}</td>
          <td style="font-family: var(--font-mono);">${{inmetVal}}</td>
          <td style="font-family: var(--font-mono); color: #c084fc;">${{cptecVal}}</td>
          <td style="font-family: var(--font-mono); font-weight: 800; color: #4ade80; font-size: 0.9rem;">${{eleitaVal}}</td>
          <td>${{badgeFonte}}</td>
          <td style="font-size: 0.76rem; color: #cbd5e1;">${{item.status_arbitragem}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function filtrarTabelaArbitragem() {{
      const query = document.getElementById('filtroArbitragem').value.toLowerCase();
      const filtradas = DADOS.clima_reconciliado.filter(c => 
        c.municipio.toLowerCase().includes(query) || 
        c.status_arbitragem.toLowerCase().includes(query) ||
        c.fonte_eleita.toLowerCase().includes(query)
      );
      renderTabelaArbitragem(filtradas);
    }}

    // Renderiza Quarentena
    function renderTabelaQuarentena(filtro) {{
      const tbody = document.querySelector('#tabelaQuarentena tbody');
      tbody.innerHTML = '';

      let lista = DADOS.rejeitados;
      if (filtro && filtro !== 'TODOS') {{
        lista = DADOS.rejeitados.filter(r => r.pipeline_origem === filtro);
      }}

      lista.forEach(r => {{
        const tr = document.createElement('tr');
        const regStr = typeof r.registro_bruto === 'object' ? JSON.stringify(r.registro_bruto) : String(r.registro_bruto);
        tr.innerHTML = `
          <td><span style="font-family: var(--font-mono); color: #c084fc; font-weight: 600;">${{r.pipeline_origem}}</span></td>
          <td style="color: #fca5a5; font-weight: 500;">${{r.motivo_erro}}</td>
          <td><code style="font-family: var(--font-mono); font-size: 0.72rem; color: #94a3b8; background: rgba(0,0,0,0.3); padding: 4px 8px; border-radius: 4px; display: block; max-width: 480px; overflow-x: auto;">${{regStr}}</code></td>
          <td style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-dim);">${{r.data_rejeicao ? r.data_rejeicao.split('T')[0] : '2026-09-18'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function filtrarQuarentena(pipeline) {{
      document.querySelectorAll('.q-filter-btn').forEach(b => b.classList.remove('active'));
      const btn = Array.from(document.querySelectorAll('.q-filter-btn')).find(b => b.getAttribute('onclick').includes(pipeline));
      if (btn) btn.classList.add('active');
      renderTabelaQuarentena(pipeline);
    }}

    function simularFogo(mongoUp) {{
      const btnUp = document.getElementById('btnMongoUp');
      const btnDown = document.getElementById('btnMongoDown');
      const nodeStart = document.getElementById('node-start');
      const nodeTrunc = document.getElementById('node-truncate');
      const nodeExt = document.getElementById('node-ext');
      const nodeMongo = document.getElementById('node-mongo');
      const nodeSilver = document.getElementById('node-silver');
      const nodeElt = document.getElementById('node-elt');
      const nodeSuccess = document.getElementById('node-success');
      const nodeAbort = document.getElementById('node-abort');
      const title = document.getElementById('terminal-title');
      const logBox = document.getElementById('terminal-log');

      if (mongoUp) {{
        btnUp.className = 'toggle-btn active-green';
        btnDown.className = 'toggle-btn';
        nodeStart.className = 'flow-node highlight-green';
        nodeTrunc.className = 'flow-node highlight-green';
        nodeExt.className = 'flow-node highlight-green';
        nodeMongo.className = 'flow-node highlight-green';
        nodeSilver.className = 'flow-node highlight-green';
        nodeElt.className = 'flow-node highlight-green';
        nodeSuccess.className = 'flow-node highlight-green';
        nodeAbort.className = 'flow-node dimmed';

        title.innerText = 'Log Real do Hop: Caminho Verde (MongoDB UP -> Carga Sucesso)';
        logBox.innerText = DADOS.log_sucesso || 'Log de sucesso executado pelo Apache Hop 2.19.';
      }} else {{
        btnUp.className = 'toggle-btn';
        btnDown.className = 'toggle-btn active-red';
        nodeStart.className = 'flow-node highlight-green';
        nodeTrunc.className = 'flow-node highlight-green';
        nodeExt.className = 'flow-node highlight-green';
        nodeMongo.className = 'flow-node highlight-red';
        nodeSilver.className = 'flow-node dimmed';
        nodeElt.className = 'flow-node dimmed';
        nodeSuccess.className = 'flow-node dimmed';
        nodeAbort.className = 'flow-node highlight-red';

        title.innerText = 'Log Real do Hop: Caminho Vermelho (MongoDB DOWN -> Abort com Código != 0)';
        logBox.innerText = DADOS.log_falha || 'Log de falha convergente capturado com sucesso no Teste de Fogo.';
      }}
    }}

    function initCharts() {{
      const ordenados = [...DADOS.indicadores].sort((a, b) => b.taxa_incidencia_100k - a.taxa_incidencia_100k).slice(0, 10);
      const labelsInc = ordenados.map(c => `${{c.nome_municipio}} (${{c.uf}})`);
      const valoresInc = ordenados.map(c => c.taxa_incidencia_100k);
      const cores = ordenados.map(c => c.taxa_incidencia_100k >= 100 ? '#f87171' : '#38bdf8');

      new Chart(document.getElementById('chartIncidencia'), {{
        type: 'bar',
        data: {{
          labels: labelsInc,
          datasets: [{{
            label: 'Incidência por 100k hab',
            data: valoresInc,
            backgroundColor: cores,
            borderRadius: 6
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{
            x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }},
            y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#94a3b8' }} }}
          }}
        }}
      }});

      const labelsReg = Object.keys(DADOS.regioes_casos);
      const valoresReg = Object.values(DADOS.regioes_casos);

      new Chart(document.getElementById('chartRegioes'), {{
        type: 'doughnut',
        data: {{
          labels: labelsReg,
          datasets: [{{
            data: valoresReg,
            backgroundColor: ['#38bdf8', '#818cf8', '#f59e0b', '#22c55e', '#ec4899'],
            borderWidth: 0
          }}]
        }},
        options: {{
          responsive: true,
          plugins: {{
            legend: {{
              position: 'bottom',
              labels: {{ color: '#94a3b8', font: {{ family: "'Plus Jakarta Sans'" }} }}
            }}
          }}
        }}
      }});
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      renderTabelaCidades(DADOS.indicadores);
      renderTabelaArbitragem(DADOS.clima_reconciliado);
      renderTabelaQuarentena('TODOS');
      simularFogo(true);
      initCharts();
    }});
  </script>
</body>
</html>
"""

    with open(CAMINHO_HTML, "w", encoding="utf-8") as f:
        f.write(html_code)

    print(f"✨ Dashboard Web atualizado com sucesso em: {CAMINHO_HTML}")

if __name__ == "__main__":
    gerar_dashboard()
