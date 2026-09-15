import json
from superset.app import create_app

app = create_app()

with app.app_context():
    from superset import db, security_manager
    from superset.models.slice import Slice
    from superset.models.dashboard import Dashboard
    from superset.models.core import Database
    from superset.connectors.sqla.models import SqlaTable, TableColumn, SqlMetric

    # 1. Localizar o banco "Banco de Vendas"
    database = db.session.query(Database).filter_by(database_name="Banco de Vendas").first()
    if not database:
        print("Erro: Banco 'Banco de Vendas' não encontrado!")
        exit(1)

    print(f"✅ Banco encontrado: {database.database_name} (ID: {database.id})")

    # 2. Registrar ou atualizar o dataset 'recomendacoes_produtos'
    table = db.session.query(SqlaTable).filter_by(
        table_name="recomendacoes_produtos",
        database_id=database.id
    ).first()

    if not table:
        table = SqlaTable(
            table_name="recomendacoes_produtos",
            schema="public",
            database=database
        )
        db.session.add(table)
        db.session.commit()
        table.fetch_metadata()
        db.session.commit()
        print(f"✅ Dataset 'recomendacoes_produtos' criado e sincronizado! ID: {table.id}")
    else:
        table.fetch_metadata()
        db.session.commit()
        print(f"ℹ️ Dataset 'recomendacoes_produtos' existente! ID: {table.id}")

    datasource_id = f"{table.id}__table"

    # 3. Definir a métrica MAX(similaridade)
    sim_col = next((c for c in table.columns if c.column_name == 'similaridade'), None)
    sim_col_id = sim_col.id if sim_col else None

    metric_similaridade = {
        "aggregate": "MAX",
        "column": {
            "column_name": "similaridade",
            "id": sim_col_id,
            "type": "NUMERIC(5, 4)"
        },
        "expressionType": "SIMPLE",
        "hasCustomLabel": True,
        "label": "Similaridade",
        "sqlExpression": None
    }

    # 4. Criar o Gráfico de Top Recomendações
    chart_name = "Top Recomendações de Produtos"
    chart_params = {
        "datasource": datasource_id,
        "viz_type": "echarts_timeseries_bar",
        "x_axis": "produto_recomendado",
        "metrics": [metric_similaridade],
        "groupby": ["categoria"],
        "order_desc": True,
        "sort_series_type": "sum",
        "color_scheme": "supersetColors",
        "orientation": "vertical",
        "show_legend": True,
        "legendOrientation": "top",
        "rich_tooltip": True,
        "truncateXAxis": True,
        "y_axis_format": ".2f",
        "adhoc_filters": []
    }

    chart = db.session.query(Slice).filter_by(slice_name=chart_name).first()
    if not chart:
        chart = Slice(
            slice_name=chart_name,
            viz_type="echarts_timeseries_bar",
            datasource_type="table",
            datasource_id=table.id,
            params=json.dumps(chart_params)
        )
        db.session.add(chart)
        db.session.commit()
        print(f"✅ Gráfico '{chart.slice_name}' criado! ID: {chart.id}")
    else:
        chart.viz_type = "echarts_timeseries_bar"
        chart.datasource_id = table.id
        chart.params = json.dumps(chart_params)
        db.session.commit()
        print(f"🔄 Gráfico '{chart.slice_name}' atualizado! ID: {chart.id}")

    # 5. Criar o Dashboard de Recomendações
    dash_title = "Dashboard de Recomendações"
    dash = db.session.query(Dashboard).filter_by(dashboard_title=dash_title).first()
    if not dash:
        dash = Dashboard(
            dashboard_title=dash_title,
            slug="dashboard_recomendacoes",
            published=True
        )
        db.session.add(dash)
        db.session.commit()
        print(f"✅ Dashboard '{dash.dashboard_title}' criado! ID: {dash.id}")
    else:
        print(f"ℹ️ Dashboard '{dash.dashboard_title}' já existente! ID: {dash.id}")

    dash.slices = [chart]
    dash.published = True

    # Montar layout visual agradável
    chart_key = f"CHART-{chart.id}"
    position_data = {
        "DASHBOARD_VERSION_KEY": "v2",
        "ROOT_ID": {"children": ["GRID_ID"], "id": "ROOT_ID", "type": "ROOT"},
        "GRID_ID": {"children": ["ROW-0"], "id": "GRID_ID", "parents": ["ROOT_ID"], "type": "GRID"},
        "ROW-0": {
            "children": [chart_key],
            "id": "ROW-0",
            "meta": {"background": "BACKGROUND_TRANSPARENT"},
            "parents": ["ROOT_ID", "GRID_ID"],
            "type": "ROW"
        },
        chart_key: {
            "children": [],
            "id": chart_key,
            "meta": {
                "chartId": chart.id,
                "height": 60,
                "sliceName": chart.slice_name,
                "width": 12
            },
            "parents": ["ROOT_ID", "GRID_ID", "ROW-0"],
            "type": "CHART"
        }
    }
    dash.position_json = json.dumps(position_data)
    db.session.commit()
    print(f"🎉 Dashboard montado com o gráfico '{chart.slice_name}'!")

    # 6. Configuração de Acesso Público (Role Public)
    public_role = security_manager.find_role("Public")
    if public_role:
        # Permissões necessárias para visualização pública
        perm_targets = [
            ("can_read", "Dashboard"),
            ("can_read", "Chart"),
            ("can_read", "Dataset"),
            ("can_dashboard", "Superset"),
            ("can_slice", "Superset"),
            ("can_explore_json", "Superset"),
            ("all_datasource_access", "all_datasource_access")
        ]
        
        # Sincronizar permissões
        for p_name, v_name in perm_targets:
            p_view = security_manager.find_permission_view_menu(p_name, v_name)
            if p_view and p_view not in public_role.permissions:
                security_manager.add_permission_role(public_role, p_view)
                print(f"➕ Permissão concedida a Public: {p_name} on {v_name}")
                
        # Permissão específica do banco Banco de Vendas
        db_pview = security_manager.find_permission_view_menu("database_access", database.perm)
        if db_pview and db_pview not in public_role.permissions:
            security_manager.add_permission_role(public_role, db_pview)
            print(f"➕ Permissão concedida a Public: database_access on {database.perm}")

        # Permissão do schema public
        schema_perm = security_manager.get_schema_perm(database.database_name, "public")
        if schema_perm:
            sc_pview = security_manager.find_permission_view_menu("schema_access", schema_perm)
            if sc_pview and sc_pview not in public_role.permissions:
                security_manager.add_permission_role(public_role, sc_pview)
                print(f"➕ Permissão concedida a Public: schema_access on {schema_perm}")

        db.session.commit()
        print("🔓 Role Public configurada com sucesso para visualização anônima!")

    print(f"\n==================================================")
    print(f"Dashboard URL: http://localhost:8088/superset/dashboard/dashboard_recomendacoes/")
    print(f"Direct ID URL: http://localhost:8088/superset/dashboard/{dash.id}/")
    print(f"==================================================")
