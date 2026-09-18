import os
import json
import pandas as pd
import numpy as np

def gerar_dashboard():
    DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
    csv_triplo_local = os.path.join(DIR_ATUAL, "resultado_brasil_triplo_integrado.csv")
    csv_padrao_local = os.path.join(DIR_ATUAL, "resultado_brasil_integrado.csv")
    csv_triplo_dl = "/home/ficdevia-16-tarde/Downloads/resultado_brasil_triplo_integrado.csv"
    csv_padrao_dl = "/home/ficdevia-16-tarde/Downloads/resultado_brasil_integrado.csv"

    tem_chuva = False
    if os.path.exists(csv_triplo_local):
        csv_path = csv_triplo_local
        tem_chuva = True
        print(f"Carregando base TRIPLA (Dengue + IBGE + Chuva INMET) da pasta aula 13: {csv_path}...")
    elif os.path.exists(csv_triplo_dl):
        csv_path = csv_triplo_dl
        tem_chuva = True
        print(f"Carregando base TRIPLA (Dengue + IBGE + Chuva INMET) de Downloads: {csv_path}...")
    elif os.path.exists(csv_padrao_local):
        csv_path = csv_padrao_local
        print(f"Carregando base DUPLA (Dengue + IBGE) da pasta aula 13: {csv_path}...")
    elif os.path.exists(csv_padrao_dl):
        csv_path = csv_padrao_dl
        print(f"Carregando base DUPLA (Dengue + IBGE) de Downloads: {csv_path}...")
    else:
        raise FileNotFoundError("Nenhum arquivo consolidado encontrado na pasta aula 13 nem em Downloads!")

    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

    df['v0001'] = pd.to_numeric(df['v0001'], errors='coerce').fillna(0).astype(int)
    df['total_casos_dengue'] = pd.to_numeric(df['total_casos_dengue'], errors='coerce').fillna(0).astype(int)
    df['incidencia'] = np.where(df['v0001'] > 0, (df['total_casos_dengue'] / df['v0001']) * 100000, 0.0)
    df['incidencia'] = df['incidencia'].round(2)

    if tem_chuva and 'chuva_mm' in df.columns:
        df['chuva_mm'] = pd.to_numeric(
            df['chuva_mm'].astype(str).str.replace(',', '.').str.strip(),
            errors='coerce'
        ).fillna(0.0).round(1)
    else:
        df['chuva_mm'] = 0.0
        df['tem_estacao'] = 'N'

    # Classificação de risco epidemiológico do Ministério da Saúde
    condicoes = [
        df['total_casos_dengue'] == 0,
        df['incidencia'] < 100,
        (df['incidencia'] >= 100) & (df['incidencia'] < 300),
        (df['incidencia'] >= 300) & (df['incidencia'] < 500),
        df['incidencia'] >= 500
    ]
    rotulos = ['Sem Casos', 'Baixo Risco', 'Médio Risco', 'Alto Risco', 'Epidemia']
    df['risco'] = np.select(condicoes, rotulos, default='Baixo Risco')

    # Mapeamento Regiões e Siglas
    uf_map = {
        'Acre': ('AC', 'Norte'), 'Alagoas': ('AL', 'Nordeste'), 'Amapá': ('AP', 'Norte'),
        'Amazonas': ('AM', 'Norte'), 'Bahia': ('BA', 'Nordeste'), 'Ceará': ('CE', 'Nordeste'),
        'Distrito Federal': ('DF', 'Centro-Oeste'), 'Espírito Santo': ('ES', 'Sudeste'),
        'Goiás': ('GO', 'Centro-Oeste'), 'Maranhão': ('MA', 'Nordeste'), 'Mato Grosso': ('MT', 'Centro-Oeste'),
        'Mato Grosso do Sul': ('MS', 'Centro-Oeste'), 'Minas Gerais': ('MG', 'Sudeste'),
        'Paraná': ('PR', 'Sul'), 'Paraíba': ('PB', 'Nordeste'), 'Pará': ('PA', 'Norte'),
        'Pernambuco': ('PE', 'Nordeste'), 'Piauí': ('PI', 'Nordeste'), 'Rio Grande do Norte': ('RN', 'Nordeste'),
        'Rio Grande do Sul': ('RS', 'Sul'), 'Rio de Janeiro': ('RJ', 'Sudeste'), 'Rondônia': ('RO', 'Norte'),
        'Roraima': ('RR', 'Norte'), 'Santa Catarina': ('SC', 'Sul'), 'Sergipe': ('SE', 'Nordeste'),
        'São Paulo': ('SP', 'Sudeste'), 'Tocantins': ('TO', 'Norte')
    }
    df['UF_SIGLA'] = df['NM_UF'].map(lambda x: uf_map.get(x, ('??', 'Outro'))[0])
    df['REGIAO'] = df['NM_UF'].map(lambda x: uf_map.get(x, ('??', 'Outro'))[1])

    # Métricas Gerais
    total_casos = int(df['total_casos_dengue'].sum())
    total_pop = int(df['v0001'].sum())
    taxa_nacional = round((total_casos / total_pop) * 100000, 2)
    total_municipios = len(df)
    mun_com_casos = int((df['total_casos_dengue'] > 0).sum())
    mun_sem_casos = total_municipios - mun_com_casos
    chuva_media = round(float(df['chuva_mm'].mean()), 1) if tem_chuva else 0.0

    risco_counts = df['risco'].value_counts().to_dict()

    # Top 10 Estados em Casos
    uf_agg = df.groupby(['NM_UF', 'UF_SIGLA']).agg(
        casos=('total_casos_dengue', 'sum'),
        pop=('v0001', 'sum'),
        chuva_media=('chuva_mm', 'mean')
    ).reset_index()
    uf_agg['incidencia'] = (uf_agg['casos'] / uf_agg['pop'] * 100000).round(2)
    uf_agg['chuva_media'] = uf_agg['chuva_media'].round(1)
    top_ufs_casos = uf_agg.sort_values(by='casos', ascending=False).head(10).to_dict(orient='records')

    # Top 10 Municípios em Incidência
    top_mun_incid = df[df['v0001'] >= 10000].sort_values(by='incidencia', ascending=False).head(10)[[
        'NM_MUN', 'UF_SIGLA', 'v0001', 'total_casos_dengue', 'incidencia', 'chuva_mm', 'risco'
    ]].to_dict(orient='records')

    # Lista completa otimizada para JSON: [cod, mun, uf, pop, casos, incid, chuva_mm, tem_estacao, risco]
    df_sorted = df.sort_values(by='total_casos_dengue', ascending=False)
    municipios_rows = [
        [
            str(row['cod_mun_6']),
            str(row['NM_MUN']),
            str(row['UF_SIGLA']),
            int(row['v0001']),
            int(row['total_casos_dengue']),
            float(row['incidencia']),
            float(row['chuva_mm']),
            str(row.get('tem_estacao', 'N')),
            str(row['risco'])
        ]
        for _, row in df_sorted.iterrows()
    ]

    payload = {
        "tem_chuva": tem_chuva,
        "kpis": {
            "total_casos": total_casos,
            "total_pop": total_pop,
            "taxa_nacional": taxa_nacional,
            "chuva_media": chuva_media,
            "total_municipios": total_municipios,
            "mun_com_casos": mun_com_casos,
            "mun_sem_casos": mun_sem_casos,
            "risco": {
                "epidemia": int(risco_counts.get('Epidemia', 0)),
                "alto": int(risco_counts.get('Alto Risco', 0)),
                "medio": int(risco_counts.get('Médio Risco', 0)),
                "baixo": int(risco_counts.get('Baixo Risco', 0)),
                "sem_casos": int(risco_counts.get('Sem Casos', 0))
            }
        },
        "top_ufs_casos": top_ufs_casos,
        "top_mun_incid": top_mun_incid,
        "municipios": municipios_rows
    }

    json_str = json.dumps(payload, ensure_ascii=False)

    pct_epidemia = round((risco_counts.get('Epidemia', 0) / total_municipios) * 100, 1)
    pct_alto = round((risco_counts.get('Alto Risco', 0) / total_municipios) * 100, 1)
    pct_medio = round((risco_counts.get('Médio Risco', 0) / total_municipios) * 100, 1)
    pct_baixo = round((risco_counts.get('Baixo Risco', 0) / total_municipios) * 100, 1)
    pct_sem = round((risco_counts.get('Sem Casos', 0) / total_municipios) * 100, 1)
    pct_atingidos = round((mun_com_casos / total_municipios) * 100, 1)

    template = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Observatório Epidemiológico Integrado: Dengue + Censo IBGE + Chuva INMET | Aula 13</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-main: #0a0e17;
      --bg-card: rgba(17, 24, 39, 0.75);
      --bg-card-hover: rgba(26, 36, 56, 0.85);
      --border-color: rgba(255, 255, 255, 0.08);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      
      --accent-epidemia: #f43f5e;
      --accent-epidemia-bg: rgba(244, 63, 94, 0.15);
      --accent-alto: #f97316;
      --accent-alto-bg: rgba(249, 115, 22, 0.15);
      --accent-medio: #eab308;
      --accent-medio-bg: rgba(234, 179, 8, 0.15);
      --accent-baixo: #10b981;
      --accent-baixo-bg: rgba(16, 185, 129, 0.15);
      --accent-zero: #64748b;
      --accent-zero-bg: rgba(100, 116, 139, 0.15);

      --color-primary: #6366f1;
      --color-primary-light: #818cf8;
      --color-cyan: #06b6d4;
      --color-blue-rain: #38bdf8;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-main);
      color: var(--text-primary);
      line-height: 1.5;
      padding: 24px;
      min-height: 100vh;
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.08) 0px, transparent 50%);
      background-attachment: fixed;
    }

    .container { max-width: 1400px; margin: 0 auto; }

    /* Header */
    header {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 32px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--border-color);
    }

    .badge-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      background: rgba(99, 102, 241, 0.15);
      color: var(--color-primary-light);
      border: 1px solid rgba(99, 102, 241, 0.3);
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      width: fit-content;
    }

    h1 {
      font-size: 2.25rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 40%, #38bdf8 80%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      letter-spacing: -0.02em;
    }

    .subtitle {
      color: var(--text-secondary);
      font-size: 1.05rem;
      max-width: 1000px;
    }

    /* KPI Grid */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
    }

    .kpi-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }

    .kpi-card:hover {
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.15);
      background: var(--bg-card-hover);
    }

    .kpi-label {
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 8px;
    }

    .kpi-value {
      font-size: 1.95rem;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-primary);
      margin-bottom: 6px;
    }

    .kpi-subtext {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    /* Risk Distribution Bar */
    .risk-banner {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 32px;
    }

    .section-title {
      font-size: 1.3rem;
      font-weight: 700;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .section-desc {
      color: var(--text-secondary);
      font-size: 0.95rem;
      margin-bottom: 20px;
    }

    .multi-progress-bar {
      height: 16px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      overflow: hidden;
      margin-bottom: 16px;
    }

    .progress-segment { height: 100%; transition: width 0.5s ease; }

    .risk-legend { display: flex; flex-wrap: wrap; gap: 16px; }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.875rem;
      color: var(--text-secondary);
    }

    .legend-dot { width: 10px; height: 10px; border-radius: 50%; }

    .legend-value {
      font-weight: 700;
      color: var(--text-primary);
      font-family: 'JetBrains Mono', monospace;
    }

    /* Insights Grid */
    .insights-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 20px;
      margin-bottom: 32px;
    }

    .insight-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .insight-header { display: flex; align-items: center; gap: 10px; }

    .insight-icon {
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: rgba(99, 102, 241, 0.15);
      color: var(--color-primary-light);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 1.1rem;
    }

    .insight-title { font-size: 1.1rem; font-weight: 700; }
    .insight-body { color: var(--text-secondary); font-size: 0.925rem; line-height: 1.6; }
    .highlight-stat { color: var(--color-primary-light); font-weight: 700; }

    /* Rankings Two Columns */
    .rankings-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 40px;
    }

    @media (max-width: 900px) {
      .rankings-grid { grid-template-columns: 1fr; }
    }

    .ranking-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
    }

    .bar-row { display: flex; flex-direction: column; gap: 4px; margin-bottom: 12px; }
    .bar-header { display: flex; justify-content: space-between; font-size: 0.875rem; }
    .bar-name { font-weight: 600; }
    .bar-val { font-family: 'JetBrains Mono', monospace; color: var(--text-secondary); }
    .bar-track { height: 8px; background: rgba(255, 255, 255, 0.05); border-radius: 9999px; overflow: hidden; }
    .bar-fill { height: 100%; border-radius: 9999px; background: linear-gradient(90deg, var(--color-primary), var(--accent-epidemia)); }

    /* Table & Controls Section */
    .table-section {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
    }

    .controls-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 20px;
      align-items: center;
      justify-content: space-between;
    }

    .search-input {
      flex: 1;
      min-width: 260px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 10px 16px;
      color: var(--text-primary);
      font-family: inherit;
      font-size: 0.95rem;
      outline: none;
    }

    .search-input:focus {
      border-color: var(--color-primary);
      box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }

    .filter-group { display: flex; gap: 10px; flex-wrap: wrap; }

    .filter-select {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 10px 14px;
      color: var(--text-primary);
      font-family: inherit;
      font-size: 0.9rem;
      outline: none;
      cursor: pointer;
    }

    .table-wrapper {
      overflow-x: auto;
      margin-bottom: 20px;
      border-radius: 10px;
      border: 1px solid var(--border-color);
    }

    table { width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left; }

    th {
      background: rgba(15, 23, 42, 0.95);
      color: var(--text-secondary);
      padding: 14px 16px;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--border-color);
      cursor: pointer;
      user-select: none;
      white-space: nowrap;
    }

    th:hover { color: var(--text-primary); }

    td {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      white-space: nowrap;
    }

    tr:hover td { background: rgba(255, 255, 255, 0.03); }
    .num-col { font-family: 'JetBrains Mono', monospace; text-align: right; }

    /* Badges */
    .badge-risk {
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      display: inline-block;
    }

    .badge-epidemia { background: var(--accent-epidemia-bg); color: var(--accent-epidemia); border: 1px solid rgba(244, 63, 94, 0.3); }
    .badge-alto { background: var(--accent-alto-bg); color: var(--accent-alto); border: 1px solid rgba(249, 115, 22, 0.3); }
    .badge-medio { background: var(--accent-medio-bg); color: var(--accent-medio); border: 1px solid rgba(234, 179, 8, 0.3); }
    .badge-baixo { background: var(--accent-baixo-bg); color: var(--accent-baixo); border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-zero { background: var(--accent-zero-bg); color: var(--accent-zero); border: 1px solid rgba(100, 116, 139, 0.3); }

    .badge-station {
      font-size: 0.7rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      background: rgba(56, 189, 248, 0.15);
      color: var(--color-blue-rain);
      border: 1px solid rgba(56, 189, 248, 0.3);
      margin-left: 6px;
    }

    /* Pagination */
    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.875rem;
      color: var(--text-secondary);
    }

    .page-btn {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 6px 14px;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.2s;
    }

    .page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .page-btn:hover:not(:disabled) { background: var(--color-primary); }

    footer {
      margin-top: 48px;
      padding-top: 24px;
      border-top: 1px solid var(--border-color);
      text-align: center;
      font-size: 0.85rem;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge-tag">Módulo 02 - Dados & Pipeline ETL/ELT • Aula 13 • Pipeline Triplo</div>
      <h1>Observatório Epidemiológico & Climático do Brasil</h1>
      <p class="subtitle">
        Integração tripla de alta performance no Apache Hop: Microdados de Dengue (DataSUS) + Censo Demográfico (IBGE) + Pluviosidade das 565 Estações Meteorológicas (INMET).
      </p>
    </header>

    <!-- Top KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Notificações Dengue</div>
        <div class="kpi-value" style="color: var(--accent-epidemia);">__TOTAL_CASOS__</div>
        <div class="kpi-subtext">Casos registrados (DataSUS)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">População Coberta</div>
        <div class="kpi-value" style="color: var(--color-cyan);">__TOTAL_POP__</div>
        <div class="kpi-subtext">Censo Demográfico IBGE 2022</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Taxa Média Nacional</div>
        <div class="kpi-value" style="color: var(--accent-medio);">__TAXA_NACIONAL__</div>
        <div class="kpi-subtext">Casos por 100.000 habitantes</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Chuva Média Anual</div>
        <div class="kpi-value" style="color: var(--color-blue-rain);">__CHUVA_MEDIA__ <span style="font-size: 1.1rem; color: var(--text-muted);">mm</span></div>
        <div class="kpi-subtext">Base INMET (565 estações)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Municípios em Epidemia</div>
        <div class="kpi-value" style="color: var(--accent-alto);">__MUN_EPIDEMIA__</div>
        <div class="kpi-subtext">Taxa &ge; 500 casos / 100k hab.</div>
      </div>
    </div>

    <!-- Epidemiological Risk Banner -->
    <div class="risk-banner">
      <div class="section-title">Classificação Epidemiológica de Risco (Ministério da Saúde)</div>
      <div class="section-desc">
        Distribuição dos 5.570 municípios brasileiros segundo parâmetros de incidência per capita.
      </div>
      <div class="multi-progress-bar">
        <div class="progress-segment" style="width: __PCT_EPIDEMIA__%; background: var(--accent-epidemia);" title="Epidemia"></div>
        <div class="progress-segment" style="width: __PCT_ALTO__%; background: var(--accent-alto);" title="Alto Risco"></div>
        <div class="progress-segment" style="width: __PCT_MEDIO__%; background: var(--accent-medio);" title="Médio Risco"></div>
        <div class="progress-segment" style="width: __PCT_BAIXO__%; background: var(--accent-baixo);" title="Baixo Risco"></div>
        <div class="progress-segment" style="width: __PCT_SEM__%; background: var(--accent-zero);" title="Sem Casos"></div>
      </div>
      <div class="risk-legend">
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--accent-epidemia);"></span>
          <span>Epidemia (&ge;500): <span class="legend-value">__CNT_EPIDEMIA__ (__PCT_EPIDEMIA__%)</span></span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--accent-alto);"></span>
          <span>Alto Risco (300 a 500): <span class="legend-value">__CNT_ALTO__ (__PCT_ALTO__%)</span></span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--accent-medio);"></span>
          <span>Médio Risco (100 a 300): <span class="legend-value">__CNT_MEDIO__ (__PCT_MEDIO__%)</span></span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--accent-baixo);"></span>
          <span>Baixo Risco (&lt;100): <span class="legend-value">__CNT_BAIXO__ (__PCT_BAIXO__%)</span></span>
        </div>
        <div class="legend-item">
          <span class="legend-dot" style="background: var(--accent-zero);"></span>
          <span>Sem Notificação: <span class="legend-value">__CNT_SEM__ (__PCT_SEM__%)</span></span>
        </div>
      </div>
    </div>

    <!-- Interpretation & Key Insights -->
    <div class="insights-grid">
      <div class="insight-card">
        <div class="insight-header">
          <div class="insight-icon">&#9748;</div>
          <div class="insight-title">Relação Clima & Proliferação Vetorial</div>
        </div>
        <div class="insight-body">
          A inclusão dos dados de <strong>precipitação do INMET</strong> revela como o regime de chuvas atua como catalisador dos criadouros do <em>Aedes aegypti</em>. Estados com elevados índices pluviométricos no primeiro semestre combinados com altas temperaturas formam o ambiente biológico ideal para explosão de casos de dengue.
        </div>
      </div>

      <div class="insight-card">
        <div class="insight-header">
          <div class="insight-icon">&#127758;</div>
          <div class="insight-title">O Epicentro no Centro-Oeste</div>
        </div>
        <div class="insight-body">
          O estado de <strong>Goiás</strong> lidera com folga o ranking nacional com mais de <span class="highlight-stat">110 mil casos</span> e incidência alarmante de <span class="highlight-stat">1.571 casos / 100k hab.</span>, associado a um volume anual acumulado médio de <span class="highlight-stat">1.071 mm de chuva</span> que concentrou focos nos períodos chuvosos.
        </div>
      </div>

      <div class="insight-card">
        <div class="insight-header">
          <div class="insight-icon">&#9881;</div>
          <div class="insight-title">Arquitetura de Pipeline Tripla</div>
        </div>
        <div class="insight-body">
          O Apache Hop executou com sucesso a esteira tripla: tratou a chave IBGE de 6 dígitos, agrupou 453 mil microdados do SUS e integrou a pluviosidade medida de <strong>565 estações meteorológicas</strong> com imputação regional para municípios sem estação.
        </div>
      </div>
    </div>

    <!-- Rankings Comparison -->
    <div class="rankings-grid">
      <div class="ranking-card">
        <div class="section-title">Top 10 Estados em Notificações</div>
        <div class="section-desc">Volume absoluto de casos notificados e chuva média</div>
        <div id="ranking-ufs-casos"></div>
      </div>

      <div class="ranking-card">
        <div class="section-title">Top 10 Municípios Mais Críticos (Taxa)</div>
        <div class="section-desc">Incidência por 100k hab. e pluviosidade medida</div>
        <div id="ranking-mun-incid"></div>
      </div>
    </div>

    <!-- Full Interactive Table -->
    <div class="table-section">
      <div class="section-title">Lista Consolidada de Municípios Brasileiros</div>
      <div class="section-desc">
        Navegue, pesquise e ordene os dados completos com População, Notificações de Dengue e Pluviosidade Anual do INMET.
      </div>

      <div class="controls-bar">
        <input type="text" id="search-box" class="search-input" placeholder="Buscar por município ou código IBGE (ex: Goiânia, 355030, Uberlândia, Cuiabá...)">
        
        <div class="filter-group">
          <select id="filter-uf" class="filter-select">
            <option value="">Todas as UFs</option>
          </select>

          <select id="filter-risco" class="filter-select">
            <option value="">Todos os Níveis de Risco</option>
            <option value="Epidemia">Epidemia (&ge; 500)</option>
            <option value="Alto Risco">Alto Risco (300 - 500)</option>
            <option value="Médio Risco">Médio Risco (100 - 300)</option>
            <option value="Baixo Risco">Baixo Risco (&lt; 100)</option>
            <option value="Sem Casos">Sem Notificações (0)</option>
          </select>

          <select id="page-size" class="filter-select">
            <option value="25">25 por página</option>
            <option value="50" selected>50 por página</option>
            <option value="100">100 por página</option>
            <option value="250">250 por página</option>
          </select>
        </div>
      </div>

      <div class="table-wrapper">
        <table id="mun-table">
          <thead>
            <tr>
              <th onclick="sortTable(0)">Cód. IBGE &#8645;</th>
              <th onclick="sortTable(1)">Município &#8645;</th>
              <th onclick="sortTable(2)">UF &#8645;</th>
              <th class="num-col" onclick="sortTable(3)">População (2022) &#8645;</th>
              <th class="num-col" onclick="sortTable(4)">Casos Dengue &#8645;</th>
              <th class="num-col" onclick="sortTable(5)">Incidência /100k &#8645;</th>
              <th class="num-col" onclick="sortTable(6)">Chuva Anual (mm) &#8645;</th>
              <th onclick="sortTable(8)">Classificação &#8645;</th>
            </tr>
          </thead>
          <tbody id="table-body"></tbody>
        </table>
      </div>

      <div class="pagination-bar">
        <div id="table-info">Carregando dados...</div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button id="btn-prev" class="page-btn" onclick="changePage(-1)">&larr; Anterior</button>
          <span id="page-indicator" style="font-family: 'JetBrains Mono', monospace; font-weight: 600;">1 / 1</span>
          <button id="btn-next" class="page-btn" onclick="changePage(1)">Próxima &rarr;</button>
        </div>
      </div>
    </div>

    <footer>
      Desenvolvido para o curso de Formação Inicial e Continuada em IA (FIC Dev IA) • Projeto Integrador de Engenharia de Dados com Apache Hop
    </footer>
  </div>

  <script>
    const DATA = __DATA_JSON__;

    // Render Rankings
    function renderRankings() {
      const ufContainer = document.getElementById('ranking-ufs-casos');
      const maxUfCasos = DATA.top_ufs_casos[0].casos;
      ufContainer.innerHTML = DATA.top_ufs_casos.map(uf => `
        <div class="bar-row">
          <div class="bar-header">
            <span class="bar-name">${uf.NM_UF} (${uf.UF_SIGLA})</span>
            <span class="bar-val">${uf.casos.toLocaleString('pt-BR')} casos | Chuva: ${uf.chuva_media.toLocaleString('pt-BR')} mm</span>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${(uf.casos / maxUfCasos) * 100}%;"></div>
          </div>
        </div>
      `).join('');

      const munContainer = document.getElementById('ranking-mun-incid');
      const maxMunIncid = DATA.top_mun_incid[0].incidencia;
      munContainer.innerHTML = DATA.top_mun_incid.map(m => `
        <div class="bar-row">
          <div class="bar-header">
            <span class="bar-name">${m.NM_MUN} - ${m.UF_SIGLA}</span>
            <span class="bar-val" style="color: var(--accent-epidemia); font-weight: 700;">${m.incidencia.toLocaleString('pt-BR')} /100k (${m.chuva_mm.toLocaleString('pt-BR')} mm)</span>
          </div>
          <div class="bar-track">
            <div class="bar-fill" style="width: ${(m.incidencia / maxMunIncid) * 100}%; background: linear-gradient(90deg, var(--accent-alto), var(--accent-epidemia));"></div>
          </div>
        </div>
      `).join('');
    }

    // Table State
    let filteredData = [...DATA.municipios];
    let currentPage = 1;
    let pageSize = 50;
    let currentSortCol = 4; // Casos por padrão
    let currentSortAsc = false; // Descendente

    // Populate UF Dropdown
    function populateUfFilter() {
      const ufSelect = document.getElementById('filter-uf');
      const ufs = [...new Set(DATA.municipios.map(m => m[2]))].sort();
      ufs.forEach(uf => {
        const opt = document.createElement('option');
        opt.value = uf;
        opt.textContent = uf;
        ufSelect.appendChild(opt);
      });
    }

    function getRiskBadge(risco) {
      switch(risco) {
        case 'Epidemia': return '<span class="badge-risk badge-epidemia">Epidemia</span>';
        case 'Alto Risco': return '<span class="badge-risk badge-alto">Alto Risco</span>';
        case 'Médio Risco': return '<span class="badge-risk badge-medio">Médio Risco</span>';
        case 'Baixo Risco': return '<span class="badge-risk badge-baixo">Baixo Risco</span>';
        default: return '<span class="badge-risk badge-zero">Sem Casos</span>';
      }
    }

    function applyFilters() {
      const query = document.getElementById('search-box').value.toLowerCase().trim();
      const uf = document.getElementById('filter-uf').value;
      const risco = document.getElementById('filter-risco').value;

      filteredData = DATA.municipios.filter(m => {
        const codMatch = m[0].includes(query);
        const nameMatch = m[1].toLowerCase().includes(query);
        const ufMatch = !uf || m[2] === uf;
        const riscoMatch = !risco || m[8] === risco;
        return (codMatch || nameMatch) && ufMatch && riscoMatch;
      });

      applySort();
      currentPage = 1;
      renderTable();
    }

    function sortTable(colIndex) {
      if (currentSortCol === colIndex) {
        currentSortAsc = !currentSortAsc;
      } else {
        currentSortCol = colIndex;
        currentSortAsc = (colIndex === 0 || colIndex === 1 || colIndex === 2);
      }
      applySort();
      renderTable();
    }

    function applySort() {
      filteredData.sort((a, b) => {
        let valA = a[currentSortCol];
        let valB = b[currentSortCol];

        if (typeof valA === 'string') {
          valA = valA.toLowerCase();
          valB = valB.toLowerCase();
        }

        if (valA < valB) return currentSortAsc ? -1 : 1;
        if (valA > valB) return currentSortAsc ? 1 : -1;
        return 0;
      });
    }

    function renderTable() {
      const tbody = document.getElementById('table-body');
      const start = (currentPage - 1) * pageSize;
      const end = Math.min(start + pageSize, filteredData.length);
      const pageRows = filteredData.slice(start, end);

      if (pageRows.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 40px; color: var(--text-muted);">Nenhum município encontrado com os filtros selecionados.</td></tr>';
      } else {
        tbody.innerHTML = pageRows.map(m => `
          <tr>
            <td style="font-family: 'JetBrains Mono', monospace; color: var(--text-muted);">${m[0]}</td>
            <td style="font-weight: 600;">
              ${m[1]}
              ${m[7] === 'S' ? '<span class="badge-station" title="Estação Meteorológica Oficial INMET">Estação</span>' : ''}
            </td>
            <td><span style="font-weight: 700; color: var(--color-primary-light);">${m[2]}</span></td>
            <td class="num-col">${m[3].toLocaleString('pt-BR')}</td>
            <td class="num-col" style="font-weight: 700; color: ${m[4] > 0 ? 'var(--text-primary)' : 'var(--text-muted)'};">${m[4].toLocaleString('pt-BR')}</td>
            <td class="num-col" style="font-weight: 700; color: ${m[5] >= 500 ? 'var(--accent-epidemia)' : (m[5] >= 300 ? 'var(--accent-alto)' : (m[5] >= 100 ? 'var(--accent-medio)' : 'var(--text-secondary)'))};">
              ${m[5].toFixed(2)}
            </td>
            <td class="num-col" style="color: var(--color-blue-rain); font-weight: 600;">
              ${m[6].toLocaleString('pt-BR', {minimumFractionDigits: 1, maximumFractionDigits: 1})} mm
            </td>
            <td>${getRiskBadge(m[8])}</td>
          </tr>
        `).join('');
      }

      const total = filteredData.length;
      document.getElementById('table-info').textContent = total > 0 
        ? `Exibindo ${start + 1} a ${end} de ${total.toLocaleString('pt-BR')} municípios`
        : 'Nenhum município exibido';

      const totalPages = Math.max(1, Math.ceil(total / pageSize));
      document.getElementById('page-indicator').textContent = `${currentPage} / ${totalPages}`;
      document.getElementById('btn-prev').disabled = currentPage === 1;
      document.getElementById('btn-next').disabled = currentPage >= totalPages;
    }

    function changePage(delta) {
      const totalPages = Math.ceil(filteredData.length / pageSize);
      currentPage = Math.max(1, Math.min(totalPages, currentPage + delta));
      renderTable();
    }

    // Event Listeners
    document.getElementById('search-box').addEventListener('input', applyFilters);
    document.getElementById('filter-uf').addEventListener('change', applyFilters);
    document.getElementById('filter-risco').addEventListener('change', applyFilters);
    document.getElementById('page-size').addEventListener('change', (e) => {
      pageSize = parseInt(e.target.value);
      currentPage = 1;
      renderTable();
    });

    // Init
    window.addEventListener('DOMContentLoaded', () => {
      renderRankings();
      populateUfFilter();
      applySort();
      renderTable();
    });
  </script>
</body>
</html>
"""

    html_content = template.replace("__DATA_JSON__", json_str) \
                           .replace("__TOTAL_CASOS__", f"{total_casos:,}".replace(",", ".")) \
                           .replace("__TOTAL_POP__", f"{total_pop:,}".replace(",", ".")) \
                           .replace("__TAXA_NACIONAL__", f"{taxa_nacional:.2f}".replace(".", ",")) \
                           .replace("__CHUVA_MEDIA__", f"{chuva_media:.1f}".replace(".", ",")) \
                           .replace("__MUN_EPIDEMIA__", f"{risco_counts.get('Epidemia', 0):,}".replace(",", ".")) \
                           .replace("__PCT_EPIDEMIA__", str(pct_epidemia)) \
                           .replace("__PCT_ALTO__", str(pct_alto)) \
                           .replace("__PCT_MEDIO__", str(pct_medio)) \
                           .replace("__PCT_BAIXO__", str(pct_baixo)) \
                           .replace("__PCT_SEM__", str(pct_sem)) \
                           .replace("__CNT_EPIDEMIA__", f"{risco_counts.get('Epidemia', 0):,}".replace(",", ".")) \
                           .replace("__CNT_ALTO__", f"{risco_counts.get('Alto Risco', 0):,}".replace(",", ".")) \
                           .replace("__CNT_MEDIO__", f"{risco_counts.get('Médio Risco', 0):,}".replace(",", ".")) \
                           .replace("__CNT_BAIXO__", f"{risco_counts.get('Baixo Risco', 0):,}".replace(",", ".")) \
                           .replace("__CNT_SEM__", f"{risco_counts.get('Sem Casos', 0):,}".replace(",", "."))

    output_dir = "/home/ficdevia-16-tarde/projetos/Fic_dev_IA_Kristiann/bloco_02_dados/aula-13"
    index_html = os.path.join(output_dir, "index.html")
    dashboard_html = os.path.join(output_dir, "dashboard_dengue_ibge.html")

    with open(index_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    with open(dashboard_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Dashboard atualizado com sucesso em:\n - {index_html}\n - {dashboard_html}")

if __name__ == "__main__":
    gerar_dashboard()
