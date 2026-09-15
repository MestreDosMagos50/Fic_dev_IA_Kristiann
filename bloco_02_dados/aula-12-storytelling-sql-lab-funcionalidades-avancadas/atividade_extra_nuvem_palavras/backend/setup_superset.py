#!/usr/bin/env python3
"""
Script de Configuração e Provisionamento Automático no Apache Superset
Cria o Dataset 'nuvem_palavras_tech', o Gráfico 'Nuvem de Palavras de Tecnologia' (Word Cloud)
e monta o Dashboard com auto-refresh de 5 minutos (300 segundos).
"""

import json
import subprocess
import os

def gerar_script_superset_interno():
    """Retorna o código Python a ser executado dentro do contêiner do Superset."""
    return """
import json
from superset.app import create_app

app = create_app()

with app.app_context():
    from superset import db
    from superset.models.core import Database
    from superset.models.slice import Slice
    from superset.models.dashboard import Dashboard
    from superset.connectors.sqla.models import SqlaTable, TableColumn, SqlMetric

    # 1. Localizar o Banco de Dados PostgreSQL configurado no Superset
    db_obj = db.session.query(Database).filter(
        (Database.database_name == 'PostgreSQL') | 
        (Database.database_name == 'Banco de Vendas') | 
        (Database.database_name.ilike('%postgres%'))
    ).first()

    if not db_obj:
        # Fallback: pega o primeiro banco não sqlite
        db_obj = db.session.query(Database).filter(Database.database_name != 'examples').first()

    if not db_obj:
        print("❌ Nenhum banco de dados encontrado no Superset!")
        exit(1)

    print(f"📦 Usando Banco de Dados: '{db_obj.database_name}' (ID: {db_obj.id})")

    # 2. Criar ou Obter o Dataset nuvem_palavras_tech
    table_name = 'nuvem_palavras_tech'
    dataset = db.session.query(SqlaTable).filter_by(table_name=table_name, database_id=db_obj.id).first()
    
    if not dataset:
        dataset = SqlaTable(
            table_name=table_name,
            database_id=db_obj.id,
            schema='public'
        )
        db.session.add(dataset)
        db.session.commit()
        print(f"✅ Dataset '{table_name}' criado no Superset (ID: {dataset.id})")
    else:
        print(f"ℹ️ Dataset '{table_name}' já existe (ID: {dataset.id})")

    # Forçar busca de colunas físicas
    try:
        dataset.fetch_metadata()
        db.session.commit()
    except Exception as e:
        print(f"Aviso metadata: {e}")

    datasource_id = f"{dataset.id}__table"

    # 3. Configurar Métrica SUM(frequencia)
    freq_col = next((c for c in dataset.columns if c.column_name == 'frequencia'), None)
    freq_col_id = freq_col.id if freq_col else None

    metric_sum_frequencia = {
        "aggregate": "SUM",
        "column": {
            "column_name": "frequencia",
            "id": freq_col_id,
            "type": "INT"
        },
        "expressionType": "SIMPLE",
        "hasCustomLabel": True,
        "label": "Frequência Total",
        "sqlExpression": None
    }

    # 4. Criar ou Atualizar Gráfico Word Cloud
    slice_name = "Nuvem de Palavras - Tecnologias em Alta"
    chart = db.session.query(Slice).filter_by(slice_name=slice_name).first()
    
    chart_params = {
        "datasource": datasource_id,
        "viz_type": "word_cloud",
        "series": "palavra",
        "metric": metric_sum_frequencia,
        "color_scheme": "supersetColors",
        "rotation": "square",
        "size_from": 14,
        "size_to": 65,
        "row_limit": 60,
        "adhoc_filters": []
    }

    if not chart:
        chart = Slice(
            slice_name=slice_name,
            viz_type="word_cloud",
            datasource_type="table",
            datasource_id=dataset.id,
            params=json.dumps(chart_params)
        )
        db.session.add(chart)
        db.session.commit()
        print(f"✅ Gráfico '{slice_name}' criado com sucesso (ID: {chart.id})")
    else:
        chart.params = json.dumps(chart_params)
        db.session.commit()
        print(f"🔄 Gráfico '{slice_name}' atualizado (ID: {chart.id})")

    # 5. Criar Dashboard com Auto-Refresh de 5 minutos (300 segundos)
    dash_title = "Dashboard Nuvem de Palavras Tech (Auto-Refresh 5m)"
    dash = db.session.query(Dashboard).filter_by(dashboard_title=dash_title).first()
    
    # Configuração JSON do Dashboard com auto-refresh a cada 300 segundos
    json_metadata = {
        "refresh_frequency": 300,
        "timed_refresh_immune_slices": [],
        "expanded_slices": {},
        "color_scheme": "supersetColors"
    }

    if not dash:
        dash = Dashboard(
            dashboard_title=dash_title,
            slug="nuvem_palavras_tech_5min",
            published=True,
            json_metadata=json.dumps(json_metadata)
        )
        db.session.add(dash)
        db.session.commit()
        print(f"✅ Dashboard '{dash_title}' criado (ID: {dash.id})")
    else:
        dash.json_metadata = json.dumps(json_metadata)
        dash.published = True
        db.session.commit()
        print(f"🔄 Dashboard '{dash_title}' atualizado (ID: {dash.id})")

    # Associar o gráfico ao Dashboard
    dash.slices = [chart]

    # Estrutura de grid visual
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
                "height": 70,
                "sliceName": chart.slice_name,
                "width": 12
            },
            "parents": ["ROOT_ID", "GRID_ID", "ROW-0"],
            "type": "CHART"
        }
    }
    dash.position_json = json.dumps(position_data)
    db.session.commit()

    print(f"🎉 Configuração concluída com sucesso no Apache Superset!")
    print(f"🔗 Acesse o Dashboard em: http://localhost:8088/superset/dashboard/{dash.id}/ ou slug 'nuvem_palavras_tech_5min'")
"""

def main():
    print("====================================================================")
    print("🛠️ Provisionando Nuvem de Palavras e Dashboard no Apache Superset...")
    print("====================================================================")
    
    script_content = gerar_script_superset_interno()
    temp_script_path = "/tmp/setup_wordcloud_internal.py"
    
    # 1. Copiar script para o contêiner superset
    try:
        proc_write = subprocess.run(
            ["docker", "exec", "-i", "superset", "python", "-c", script_content],
            capture_output=True,
            text=True,
            timeout=30
        )
        if proc_write.returncode == 0:
            print(proc_write.stdout)
            return
        else:
            print(f"⚠️ Erro ao executar no superset: {proc_write.stderr}")
    except Exception as e:
        print(f"Erro de execução: {e}")

    print("\nℹ️ Instruções manuais caso o Superset não esteja rodando via Docker:")
    print("1. Crie o Dataset apontando para a tabela 'nuvem_palavras_tech'.")
    print("2. Crie um gráfico do tipo 'Word Cloud', Dimensão: 'palavra', Métrica: 'SUM(frequencia)'.")
    print("3. Adicione o gráfico a um Dashboard e nas configurações do Dashboard ative 'Auto-refresh: 5 minutes'.")

if __name__ == "__main__":
    main()
