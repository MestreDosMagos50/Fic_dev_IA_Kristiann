import json
from superset.app import create_app

app = create_app()

with app.app_context():
    from superset import db
    from superset.models.slice import Slice
    from superset.models.dashboard import Dashboard
    from superset.connectors.sqla.models import SqlaTable

    # Obter dataset
    table = db.session.query(SqlaTable).filter_by(table_name="recomendacoes_produtos").first()
    if not table:
        print("Erro: Dataset 'recomendacoes_produtos' não encontrado!")
        exit(1)

    datasource_id = f"{table.id}__table"

    # Métrica de similaridade
    sim_col = next((c for c in table.columns if c.column_name == 'similaridade'), None)
    metric_similaridade = {
        "aggregate": "MAX",
        "column": {"column_name": "similaridade", "id": sim_col.id if sim_col else None, "type": "NUMERIC(5, 4)"},
        "expressionType": "SIMPLE",
        "hasCustomLabel": True,
        "label": "Similaridade",
        "sqlExpression": None
    }

    # Métrica de contagem
    metric_count = {
        "aggregate": "COUNT",
        "column": {"column_name": "id", "type": "INTEGER"},
        "expressionType": "SIMPLE",
        "hasCustomLabel": True,
        "label": "Total Recomendações",
        "sqlExpression": None
    }

    # 1. Gráfico de Pizza: Distribuição por Categoria
    g_pizza = {
        "slice_name": "Recomendações por Categoria - Pizza",
        "viz_type": "pie",
        "params": {
            "datasource": datasource_id,
            "viz_type": "pie",
            "groupby": ["categoria"],
            "metric": metric_count,
            "color_scheme": "supersetColors",
            "show_legend": True,
            "legendOrientation": "top",
            "label_type": "key_percent",
            "donut": True,
            "adhoc_filters": []
        }
    }

    # 2. Gráfico de Dispersão: Similaridade vs Avaliação
    g_scatter = {
        "slice_name": "Similaridade vs Nota de Avaliação",
        "viz_type": "echarts_timeseries_scatter",
        "params": {
            "datasource": datasource_id,
            "viz_type": "echarts_timeseries_scatter",
            "x_axis": "similaridade",
            "metrics": [{
                "aggregate": "AVG",
                "column": {"column_name": "nota_avaliacao", "type": "NUMERIC(3, 1)"},
                "expressionType": "SIMPLE",
                "hasCustomLabel": True,
                "label": "Média Avaliação"
            }],
            "groupby": ["categoria"],
            "color_scheme": "supersetColors",
            "show_legend": True,
            "adhoc_filters": []
        }
    }

    # 3. KPI / Big Number: Maior Similaridade
    g_kpi = {
        "slice_name": "Maior Score de Similaridade",
        "viz_type": "big_number_total",
        "params": {
            "datasource": datasource_id,
            "viz_type": "big_number_total",
            "metric": metric_similaridade,
            "subheader": "Score do item mais recomendado (Notebook Gamer X)",
            "y_axis_format": ".2%",
            "adhoc_filters": []
        }
    }

    extras = [g_pizza, g_scatter, g_kpi]
    created_extras = []
    for cfg in extras:
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
            print(f"✅ Criado Gráfico Complementar: '{s.slice_name}' (ID: {s.id})")
        else:
            s.params = json.dumps(cfg["params"])
            db.session.commit()
            print(f"🔄 Atualizado Gráfico Complementar: '{s.slice_name}' (ID: {s.id})")
        created_extras.append(s)

    # Adicionar todos ao Dashboard de Recomendações
    dash = db.session.query(Dashboard).filter_by(slug="dashboard_recomendacoes").first()
    if dash:
        base_slice = db.session.query(Slice).filter_by(slice_name="Top Recomendações de Produtos").first()
        all_slices = [base_slice] + created_extras if base_slice else created_extras
        dash.slices = all_slices

        # Layout em grade harmônica:
        # Linha 1: KPI (largura 4) + Top Recomendações (largura 8)
        # Linha 2: Pizza (largura 6) + Scatter (largura 6)
        c_base = f"CHART-{base_slice.id}"
        c_kpi = f"CHART-{created_extras[2].id}"
        c_pizza = f"CHART-{created_extras[0].id}"
        c_scatter = f"CHART-{created_extras[1].id}"

        position_data = {
            "DASHBOARD_VERSION_KEY": "v2",
            "ROOT_ID": {"children": ["GRID_ID"], "id": "ROOT_ID", "type": "ROOT"},
            "GRID_ID": {"children": ["ROW-0", "ROW-1"], "id": "GRID_ID", "parents": ["ROOT_ID"], "type": "GRID"},
            "ROW-0": {
                "children": [c_kpi, c_base],
                "id": "ROW-0",
                "meta": {"background": "BACKGROUND_TRANSPARENT"},
                "parents": ["ROOT_ID", "GRID_ID"],
                "type": "ROW"
            },
            "ROW-1": {
                "children": [c_pizza, c_scatter],
                "id": "ROW-1",
                "meta": {"background": "BACKGROUND_TRANSPARENT"},
                "parents": ["ROOT_ID", "GRID_ID"],
                "type": "ROW"
            },
            c_kpi: {"children": [], "id": c_kpi, "meta": {"chartId": created_extras[2].id, "height": 50, "sliceName": created_extras[2].slice_name, "width": 4}, "parents": ["ROOT_ID", "GRID_ID", "ROW-0"], "type": "CHART"},
            c_base: {"children": [], "id": c_base, "meta": {"chartId": base_slice.id, "height": 50, "sliceName": base_slice.slice_name, "width": 8}, "parents": ["ROOT_ID", "GRID_ID", "ROW-0"], "type": "CHART"},
            c_pizza: {"children": [], "id": c_pizza, "meta": {"chartId": created_extras[0].id, "height": 50, "sliceName": created_extras[0].slice_name, "width": 6}, "parents": ["ROOT_ID", "GRID_ID", "ROW-1"], "type": "CHART"},
            c_scatter: {"children": [], "id": c_scatter, "meta": {"chartId": created_extras[1].id, "height": 50, "sliceName": created_extras[1].slice_name, "width": 6}, "parents": ["ROOT_ID", "GRID_ID", "ROW-1"], "type": "CHART"},
        }
        dash.position_json = json.dumps(position_data)
        db.session.commit()
        print(f"🎉 Dashboard de Recomendações expandido para {len(all_slices)} gráficos com sucesso!")
