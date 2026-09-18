#!/usr/bin/env python3
"""
scripts/gerar_workflow_arbitragem.py
Gera novo Workflow (.hwf) e novas Pipelines (.hpl) para demonstrar
reconciliação de dados concorrentes e arbitragem de fontes (INMET vs CPTEC).
"""

import os

DIR_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_PIPELINES = os.path.join(DIR_PROJETO, "hop", "pipelines")
DIR_WORKFLOWS = os.path.join(DIR_PROJETO, "hop", "workflows")

def salvar_xml(conteudo: str, caminho: str):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo.strip() + "\n")
    print(f"✅ Hop XML gerado: {caminho}")

def gerar_tudo():
    # 1. Pipeline Extracao INMET Temperatura
    xml_inmet = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_inmet_temperatura</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>CSV INMET Temperatura</from><to>Gravar staging.inmet_temperatura</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV INMET Temperatura</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/inmet_temperatura.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>cod_mun_6</name><type>String</type></field>
      <field><name>municipio</name><type>String</type></field>
      <field><name>temperatura_c</name><type>String</type></field>
      <field><name>umidade_relativa</name><type>String</type></field>
      <field><name>status_sensor</name><type>String</type></field>
      <field><name>data_leitura</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.inmet_temperatura</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>inmet_temperatura</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>municipio</column_name><stream_name>municipio</stream_name></field>
      <field><column_name>temperatura_c</column_name><stream_name>temperatura_c</stream_name></field>
      <field><column_name>umidade_relativa</column_name><stream_name>umidade_relativa</stream_name></field>
      <field><column_name>status_sensor</column_name><stream_name>status_sensor</stream_name></field>
      <field><column_name>data_leitura</column_name><stream_name>data_leitura</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_inmet, os.path.join(DIR_PIPELINES, "extracao_inmet_temperatura.hpl"))

    # 2. Pipeline Extracao CPTEC Temperatura
    xml_cptec = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_cptec_temperatura</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>CSV CPTEC Temperatura Satelite</from><to>Gravar staging.cptec_temperatura</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV CPTEC Temperatura Satelite</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/cptec_temperatura.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>cod_mun_6</name><type>String</type></field>
      <field><name>municipio</name><type>String</type></field>
      <field><name>temperatura_satelite_c</name><type>String</type></field>
      <field><name>umidade_satelite</name><type>String</type></field>
      <field><name>indice_cobertura</name><type>String</type></field>
      <field><name>data_leitura</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.cptec_temperatura</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>cptec_temperatura</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>municipio</column_name><stream_name>municipio</stream_name></field>
      <field><column_name>temperatura_satelite_c</column_name><stream_name>temperatura_satelite_c</stream_name></field>
      <field><column_name>umidade_satelite</column_name><stream_name>umidade_satelite</stream_name></field>
      <field><column_name>indice_cobertura</column_name><stream_name>indice_cobertura</stream_name></field>
      <field><column_name>data_leitura</column_name><stream_name>data_leitura</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_cptec, os.path.join(DIR_PIPELINES, "extracao_cptec_temperatura.hpl"))

    # 3. Novo Workflow Dedicado: workflow_arbitragem_concorrente.hwf
    xml_wf = """<?xml version="1.0" encoding="UTF-8"?>
<workflow>
  <name>workflow_arbitragem_concorrente</name>
  <name_sync_with_filename>Y</name_sync_with_filename>
  <description>Workflow de Arbitragem e Reconciliacao: INMET Terrestre vs CPTEC Satelite</description>
  <actions>
    <action>
      <name>Start</name>
      <type>SPECIAL</type>
      <repeat>N</repeat>
      <nr>0</nr>
      <xloc>80</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>SQL: Truncate Staging Concorrente</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sql>TRUNCATE TABLE staging.inmet_temperatura, staging.cptec_temperatura;</sql>
      <sqlfromfile>N</sqlfromfile>
      <nr>0</nr>
      <xloc>260</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Fonte 1: INMET Terrestre (Fisica)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_inmet_temperatura.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>460</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Fonte 2: CPTEC Satelite (Redundancia)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_cptec_temperatura.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>680</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>SQL: Motor de Arbitragem e Fallback</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sqlfilename>${PROJECT_HOME}/sql/06_elt_arbitragem_temperatura.sql</sqlfilename>
      <sqlfromfile>Y</sqlfromfile>
      <nr>0</nr>
      <xloc>900</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Log: Sucesso na Reconciliacao</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Basic</loglevel>
      <logmessage>RECONCILIACAO E ARBITRAGEM DE FONTES CLIMATICAS CONCLUIDA COM SUCESSO! TABELA silver.clima_reconciliado POPULADA.</logmessage>
      <nr>0</nr>
      <xloc>900</xloc>
      <yloc>280</yloc>
    </action>
    <action>
      <name>Log de Erro</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Error</loglevel>
      <logmessage>FALHA CRITICA NO WORKFLOW DE ARBITRAGEM DE FONTES!</logmessage>
      <nr>0</nr>
      <xloc>560</xloc>
      <yloc>280</yloc>
    </action>
    <action>
      <name>Abort</name>
      <type>ABORT</type>
      <message>Execucao abortada por erro na esteira de arbitragem.</message>
      <nr>0</nr>
      <xloc>360</xloc>
      <yloc>280</yloc>
    </action>
  </actions>
  <hops>
    <hop><from>Start</from><to>SQL: Truncate Staging Concorrente</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>Y</unconditional></hop>
    <hop><from>SQL: Truncate Staging Concorrente</from><to>Fonte 1: INMET Terrestre (Fisica)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>SQL: Truncate Staging Concorrente</from><to>Log de Erro</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 1: INMET Terrestre (Fisica)</from><to>Fonte 2: CPTEC Satelite (Redundancia)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 1: INMET Terrestre (Fisica)</from><to>Log de Erro</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 2: CPTEC Satelite (Redundancia)</from><to>SQL: Motor de Arbitragem e Fallback</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 2: CPTEC Satelite (Redundancia)</from><to>Log de Erro</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>SQL: Motor de Arbitragem e Fallback</from><to>Log: Sucesso na Reconciliacao</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>SQL: Motor de Arbitragem e Fallback</from><to>Log de Erro</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Log de Erro</from><to>Abort</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>Y</unconditional></hop>
  </hops>
</workflow>"""
    salvar_xml(xml_wf, os.path.join(DIR_WORKFLOWS, "workflow_arbitragem_concorrente.hwf"))

if __name__ == "__main__":
    print("🚀 Gerando Novo Workflow e Novas Pipelines de Arbitragem Concorrente...")
    gerar_tudo()
    print("✨ Concluído com sucesso!")
