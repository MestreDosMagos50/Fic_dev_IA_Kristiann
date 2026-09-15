#!/usr/bin/env python3
"""
FIC DEV IA – Engenharia de Dados | Aula 12
Script de Provisionamento dos KPIs da Aula 12 no Apache Superset:
- KPI Faturamento Sudeste (Big Number) -> Roteiro 4.4.3
- KPI Ticket Médio (Big Number) -> Exercício 4.4.4
- KPI Faturamento Total (Big Number with Trendline)
- Gráfico Comparativo de Vendas Diárias por Região (Bar Chart)
- Dashboard Integrado de Storytelling & KPIs
"""

import json
import subprocess

superset_code = """
import json
from superset.app import create_app

app = create_app()

with app.app_context():
    from superset import db
    from superset.models.core import Database
    from superset.models.slice import Slice
    from superset.models.dashboard import Dashboard
    from superset.connectors.sqla.models import SqlaTable, SqlMetric

    # 1. Localizar banco de dados
    db_obj = db.session.query(Database).filter(
        (Database.database_name == 'PostgreSQL') | 
        (Database.database_name == 'superset_data')
    ).first()

    if not db_obj:
        print("❌ Banco de dados não encontrado.")
        exit(1)

    print(f"📦 Usando Banco: '{db_obj.database_name}' (ID: {db_obj.id})")

    # 2. Criar ou Obter o Dataset vendas_detalhe
    table_name = 'vendas_detalhe'
    ds_vendas = db.session.query(SqlaTable).filter_by(table_name=table_name, database_id=db_obj.id).first()
    if not ds_vendas:
        ds_vendas = SqlaTable(
            table_name=table_name,
            database_id=db_obj.id,
            schema='public'
        )
        db.session.add(ds_vendas)
        db.session.commit()
        print(f"✅ Dataset '{table_name}' criado (ID: {ds_vendas.id})")
    
    try:
        ds_vendas.fetch_metadata()
        db.session.commit()
    except Exception as e:
        print(f"Fetch metadata vendas_detalhe: {e}")

    ds_vendas_id = f"{ds_vendas.id}__table"

    # Criar ou Obter o Dataset Faturamento Diario por Regiao (Roteiro 4.4.2)
    sql_dataset_name = "Faturamento Diario por Regiao"
    ds_fat = db.session.query(SqlaTable).filter_by(table_name=sql_dataset_name, database_id=db_obj.id).first()
    if not ds_fat:
        ds_fat = SqlaTable(
            table_name=sql_dataset_name,
            database_id=db_obj.id,
            schema='public',
            sql=\"\"\"
            SELECT
                CAST(data_hora_venda AS DATE) AS data_venda,
                regiao_cliente AS regiao,
                SUM(quantidade * preco_unitario) AS faturamento_diario
            FROM vendas_detalhe
            GROUP BY 1, 2
            ORDER BY 1, 2
            \"\"\"
        )
        db.session.add(ds_fat)
        db.session.commit()
        print(f"✅ Dataset SQL Lab '{sql_dataset_name}' criado (ID: {ds_fat.id})")
    
    try:
        ds_fat.fetch_metadata()
        db.session.commit()
    except Exception as e:
        print(f"Fetch metadata ds_fat: {e}")

    ds_fat_id = f"{ds_fat.id}__table"

    # 3. Métricas Customizadas
    metric_faturamento_sql = {
        "expressionType": "SQL",
        "sqlExpression": "SUM(quantidade * preco_unitario)",
        "label": "Faturamento Total (R$)",
        "hasCustomLabel": True
    }

    metric_ticket_medio_sql = {
        "expressionType": "SQL",
        "sqlExpression": "ROUND(SUM(quantidade * preco_unitario) / NULLIF(COUNT(id), 0), 2)",
        "label": "Ticket Médio (R$)",
        "hasCustomLabel": True
    }

    metric_fat_diario_simple = {
        "expressionType": "SQL",
        "sqlExpression": "SUM(faturamento_diario)",
        "label": "Faturamento Diário (R$)",
        "hasCustomLabel": True
    }

    # 4. Criar Gráficos de KPIs (Big Number)
    kpis_config = [
        {
            "slice_name": "KPI Faturamento Sudeste",
            "viz_type": "big_number_total",
            "datasource_id": ds_vendas.id,
            "params": {
                "datasource": ds_vendas_id,
                "viz_type": "big_number_total",
                "metric": metric_faturamento_sql,
                "adhoc_filters": [
                    {
                        "clause": "WHERE",
                        "comparator": "Sudeste",
                        "expressionType": "SIMPLE",
                        "filterOptionName": "filter_regiao_sudeste",
                        "isExtra": False,
                        "operator": "==",
                        "operatorId": "EQUALS",
                        "subject": "regiao_cliente"
                    }
                ],
                "header_font_size": 0.4,
                "subheader_font_size": 0.15,
                "subheader": "Meta Alerta: < R$ 500,00",
                "y_axis_format": "$,.2f"
            }
        },
        {
            "slice_name": "KPI Ticket Médio Geral",
            "viz_type": "big_number_total",
            "datasource_id": ds_vendas.id,
            "params": {
                "datasource": ds_vendas_id,
                "viz_type": "big_number_total",
                "metric": metric_ticket_medio_sql,
                "adhoc_filters": [],
                "header_font_size": 0.4,
                "subheader_font_size": 0.15,
                "subheader": "Meta Alerta: < R$ 150,00",
                "y_axis_format": "$,.2f"
            }
        },
        {
            "slice_name": "KPI Faturamento Total Geral",
            "viz_type": "big_number",
            "datasource_id": ds_vendas.id,
            "params": {
                "datasource": ds_vendas_id,
                "viz_type": "big_number",
                "metric": metric_faturamento_sql,
                "time_range": "No filter",
                "subheader": "Faturamento Consolidado de Todas as Regiões",
                "y_axis_format": "$,.2f",
                "adhoc_filters": []
            }
        },
        {
            "slice_name": "Faturamento Diário por Região - Barras",
            "viz_type": "echarts_timeseries_bar",
            "datasource_id": ds_fat.id,
            "params": {
                "datasource": ds_fat_id,
                "viz_type": "echarts_timeseries_bar",
                "x_axis": "data_venda",
                "groupby": ["regiao"],
                "metrics": [metric_fat_diario_simple],
                "color_scheme": "supersetColors",
                "rich_tooltip": True,
                "show_legend": True,
                "adhoc_filters": []
            }
        }
    ]

    slices_criados = []
    for cfg in kpis_config:
        s = db.session.query(Slice).filter_by(slice_name=cfg["slice_name"]).first()
        if not s:
            s = Slice(
                slice_name=cfg["slice_name"],
                viz_type=cfg["viz_type"],
                datasource_type="table",
                datasource_id=cfg["datasource_id"],
                params=json.dumps(cfg["params"])
            )
            db.session.add(s)
            db.session.commit()
            print(f"✅ Criado Gráfico/KPI: '{s.slice_name}' (ID: {s.id})")
        else:
            s.viz_type = cfg["viz_type"]
            s.params = json.dumps(cfg["params"])
            db.session.commit()
            print(f"🔄 Atualizado Gráfico/KPI: '{s.slice_name}' (ID: {s.id})")
        slices_criados.append(s)

    # 5. Criar Dashboard "Dashboard Aula 12 - Storytelling & KPIs"
    dash_title = "Dashboard Aula 12 - Storytelling & KPIs"
    dash = db.session.query(Dashboard).filter_by(dashboard_title=dash_title).first()
    
    if not dash:
        dash = Dashboard(
            dashboard_title=dash_title,
            slug="storytelling_kpis_aula12",
            published=True
        )
        db.session.add(dash)
        db.session.commit()
        print(f"✅ Criado Dashboard: '{dash.dashboard_title}' (ID: {dash.id})")
    else:
        dash.published = True
        db.session.commit()
        print(f"ℹ️ Dashboard já existente: '{dash.dashboard_title}' (ID: {dash.id})")

    # Associar os 4 gráficos ao Dashboard
    dash.slices = slices_criados

    # Montar Layout:
    # Linha 1 (ROW-0): 3 KPIs lado a lado (largura 4 cada = 12 colunas)
    # Linha 2 (ROW-1): Gráfico de Barras de Faturamento Diário (largura 12)
    position_data = {
        "DASHBOARD_VERSION_KEY": "v2",
        "ROOT_ID": {"children": ["GRID_ID"], "id": "ROOT_ID", "type": "ROOT"},
        "GRID_ID": {"children": ["ROW-0", "ROW-1"], "id": "GRID_ID", "parents": ["ROOT_ID"], "type": "GRID"},
        "ROW-0": {
            "children": [f"CHART-{slices_criados[0].id}", f"CHART-{slices_criados[1].id}", f"CHART-{slices_criados[2].id}"],
            "id": "ROW-0",
            "meta": {"background": "BACKGROUND_TRANSPARENT"},
            "parents": ["ROOT_ID", "GRID_ID"],
            "type": "ROW"
        },
        "ROW-1": {
            "children": [f"CHART-{slices_criados[3].id}"],
            "id": "ROW-1",
            "meta": {"background": "BACKGROUND_TRANSPARENT"},
            "parents": ["ROOT_ID", "GRID_ID"],
            "type": "ROW"
        }
    }

    # Posicionamento dos 3 KPIs
    for idx, s in enumerate(slices_criados[:3]):
        chart_key = f"CHART-{s.id}"
        position_data[chart_key] = {
            "children": [],
            "id": chart_key,
            "meta": {
                "chartId": s.id,
                "height": 30,
                "sliceName": s.slice_name,
                "width": 4
            },
            "parents": ["ROOT_ID", "GRID_ID", "ROW-0"],
            "type": "CHART"
        }

    # Posicionamento do gráfico de barras
    bar_chart = slices_criados[3]
    bar_key = f"CHART-{bar_chart.id}"
    position_data[bar_key] = {
        "children": [],
        "id": bar_key,
        "meta": {
            "chartId": bar_chart.id,
            "height": 55,
            "sliceName": bar_chart.slice_name,
            "width": 12
        },
        "parents": ["ROOT_ID", "GRID_ID", "ROW-1"],
        "type": "CHART"
    }

    dash.position_json = json.dumps(position_data)
    db.session.commit()

    print(f"🎉 Dashboard de KPIs configurado com sucesso!")
    print(f"🔗 Link direto: http://localhost:8088/superset/dashboard/{dash.id}/ ou slug 'storytelling_kpis_aula12'")
"""

def main():
    print("====================================================================")
    print("📊 Provisionando Datasets e Gráficos de KPIs da Aula 12 no Superset")
    print("====================================================================")
    proc = subprocess.run(
        ["docker", "exec", "-i", "superset", "python", "-c", superset_code],
        capture_output=True,
        text=True,
        timeout=30
    )
    if proc.returncode == 0:
        print(proc.stdout)
    else:
        print(f"Erro: {proc.stderr}")

if __name__ == "__main__":
    main()
