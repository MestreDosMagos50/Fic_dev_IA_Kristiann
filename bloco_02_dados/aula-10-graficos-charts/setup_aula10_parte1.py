import json
from superset.app import create_app

app = create_app()

with app.app_context():
    from superset import db
    from superset.models.slice import Slice
    from superset.models.dashboard import Dashboard
    from superset.connectors.sqla.models import SqlaTable

    # 1. Obter o dataset vendas_teste
    table = db.session.query(SqlaTable).filter_by(table_name='vendas_teste').first()
    if not table:
        print("Erro: Dataset 'vendas_teste' não encontrado!")
        exit(1)
        
    datasource_id = f"{table.id}__table"
    print(f"Dataset 'vendas_teste' encontrado! ID: {table.id}")

    # Definir métrica padrão SUM(valor)
    valor_col = next((c for c in table.columns if c.column_name == 'valor'), None)
    valor_col_id = valor_col.id if valor_col else None
    
    metric_sum_valor = {
        "aggregate": "SUM",
        "column": {
            "column_name": "valor",
            "id": valor_col_id,
            "type": "NUMERIC(10, 2)"
        },
        "expressionType": "SIMPLE",
        "hasCustomLabel": True,
        "label": "Total Vendas",
        "sqlExpression": None
    }

    # 2. Configurações dos Gráficos da Parte 1
    charts_config = [
        {
            "slice_name": "Vendas por Produto - Barras",
            "viz_type": "echarts_timeseries_bar",
            "params": {
                "datasource": datasource_id,
                "viz_type": "echarts_timeseries_bar",
                "x_axis": "produto",
                "metrics": [metric_sum_valor],
                "groupby": [],
                "color_scheme": "supersetColors",
                "orientation": "vertical",
                "show_legend": False,
                "rich_tooltip": True,
                "truncateXAxis": True,
                "y_axis_format": "SMART_NUMBER",
                "adhoc_filters": []
            }
        },
        {
            "slice_name": "Vendas Mensais - Linhas",
            "viz_type": "echarts_timeseries_line",
            "params": {
                "datasource": datasource_id,
                "viz_type": "echarts_timeseries_line",
                "x_axis": "data_venda",
                "time_grain_sqla": "P1M",
                "metrics": [metric_sum_valor],
                "groupby": [],
                "color_scheme": "supersetColors",
                "rich_tooltip": True,
                "show_legend": False,
                "adhoc_filters": []
            }
        },
        {
            "slice_name": "Proporção Vendas por Produto - Pizza",
            "viz_type": "pie",
            "params": {
                "datasource": datasource_id,
                "viz_type": "pie",
                "groupby": ["produto"],
                "metric": metric_sum_valor,
                "color_scheme": "supersetColors",
                "show_legend": True,
                "legendOrientation": "top",
                "label_type": "key_percent",
                "donut": False,
                "outerRadius": 70,
                "adhoc_filters": []
            }
        },
        {
            "slice_name": "Vendas por Data e Produto - Dispersão",
            "viz_type": "echarts_timeseries_scatter",
            "params": {
                "datasource": datasource_id,
                "viz_type": "echarts_timeseries_scatter",
                "x_axis": "data_venda",
                "metrics": [metric_sum_valor],
                "groupby": ["produto"],
                "color_scheme": "supersetColors",
                "rich_tooltip": True,
                "show_legend": True,
                "adhoc_filters": []
            }
        },
        {
            "slice_name": "Vendas por Produto ao Longo dos Meses - Barras Empilhadas",
            "viz_type": "echarts_timeseries_bar",
            "params": {
                "datasource": datasource_id,
                "viz_type": "echarts_timeseries_bar",
                "x_axis": "data_venda",
                "time_grain_sqla": "P1M",
                "metrics": [metric_sum_valor],
                "groupby": ["produto"],
                "stack": "Stack",
                "color_scheme": "supersetColors",
                "rich_tooltip": True,
                "show_legend": True,
                "adhoc_filters": []
            }
        },
        {
            "slice_name": "Distribuição dos Valores de Vendas - Histograma",
            "viz_type": "histogram_v2",
            "params": {
                "datasource": datasource_id,
                "viz_type": "histogram_v2",
                "column": "valor",
                "bins": 5,
                "normalize": False,
                "color_scheme": "supersetColors",
                "show_legend": False,
                "adhoc_filters": []
            }
        }
    ]

    # 3. Criar ou Atualizar os Gráficos
    created_slices = []
    for cfg in charts_config:
        s = db.session.query(Slice).filter_by(slice_name=cfg["slice_name"]).first()
        if not s:
            s = Slice(
                slice_name=cfg["slice_name"],
                viz_type=cfg["viz_type"],
                datasource_type="table",
                datasource_id=table.id,
                params=json.dumps(cfg["params"])
            )
            db.session.add(s)
            db.session.commit()
            print(f"✅ Criado Gráfico: '{s.slice_name}' (ID: {s.id})")
        else:
            s.viz_type = cfg["viz_type"]
            s.params = json.dumps(cfg["params"])
            db.session.commit()
            print(f"🔄 Atualizado Gráfico: '{s.slice_name}' (ID: {s.id})")
        created_slices.append(s)

    # 4. Criar ou Atualizar o Dashboard "Meu Primeiro Dashboard"
    dash_title = "Meu Primeiro Dashboard"
    dash = db.session.query(Dashboard).filter_by(dashboard_title=dash_title).first()
    if not dash:
        dash = Dashboard(
            dashboard_title=dash_title,
            slug="meu_primeiro_dashboard",
            published=True
        )
        db.session.add(dash)
        db.session.commit()
        print(f"✅ Criado Dashboard: '{dash.dashboard_title}' (ID: {dash.id})")
    else:
        print(f"ℹ️ Dashboard existente: '{dash.dashboard_title}' (ID: {dash.id})")

    # Associar os gráficos ao Dashboard
    dash.slices = created_slices
    dash.published = True

    # Montar layout visual agradável em grid (2 colunas x 3 linhas)
    # GRID_ID -> ROWs -> CHARTs
    position_data = {
        "DASHBOARD_VERSION_KEY": "v2",
        "ROOT_ID": {"children": ["GRID_ID"], "id": "ROOT_ID", "type": "ROOT"},
        "GRID_ID": {"children": ["ROW-0", "ROW-1", "ROW-2"], "id": "GRID_ID", "parents": ["ROOT_ID"], "type": "GRID"}
    }
    
    rows = [["ROW-0", created_slices[0:2]], ["ROW-1", created_slices[2:4]], ["ROW-2", created_slices[4:6]]]
    for row_id, slices_in_row in rows:
        row_children = []
        for s in slices_in_row:
            chart_key = f"CHART-{s.id}"
            row_children.append(chart_key)
            position_data[chart_key] = {
                "children": [],
                "id": chart_key,
                "meta": {
                    "chartId": s.id,
                    "height": 50,
                    "sliceName": s.slice_name,
                    "width": 6
                },
                "parents": ["ROOT_ID", "GRID_ID", row_id],
                "type": "CHART"
            }
        position_data[row_id] = {
            "children": row_children,
            "id": row_id,
            "meta": {"background": "BACKGROUND_TRANSPARENT"},
            "parents": ["ROOT_ID", "GRID_ID"],
            "type": "ROW"
        }

    dash.position_json = json.dumps(position_data)
    db.session.commit()
    print(f"🎉 Dashboard '{dash.dashboard_title}' configurado com {len(created_slices)} gráficos com sucesso!")
