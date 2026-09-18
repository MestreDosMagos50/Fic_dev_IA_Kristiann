#!/usr/bin/env python3
"""
scripts/gerar_pipelines_brasil.py
Gera as definições de Pipelines (.hpl) e Workflows (.hwf) do Apache Hop 2.19
para as 5 Fontes de Dados Brasileiras (IBGE Municípios, DataSUS Dengue, INMET Chuva,
CNES Leitos SUS e Alertas de Vigilância MongoDB).
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

def gerar_todas_pipelines_brasil():
    # 1. Extracao IBGE Municipios CSV
    xml_ext_ibge = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_ibge_municipios</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>CSV IBGE Municipios</from><to>Gravar staging.ibge_municipios</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV IBGE Municipios</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/ibge_municipios.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>cod_mun</name><type>String</type></field>
      <field><name>cod_mun_6</name><type>String</type></field>
      <field><name>nome_municipio</name><type>String</type></field>
      <field><name>uf</name><type>String</type></field>
      <field><name>regiao</name><type>String</type></field>
      <field><name>populacao</name><type>String</type></field>
      <field><name>area_km2</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.ibge_municipios</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>ibge_municipios</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun</column_name><stream_name>cod_mun</stream_name></field>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>nome_municipio</column_name><stream_name>nome_municipio</stream_name></field>
      <field><column_name>uf</column_name><stream_name>uf</stream_name></field>
      <field><column_name>regiao</column_name><stream_name>regiao</stream_name></field>
      <field><column_name>populacao</column_name><stream_name>populacao</stream_name></field>
      <field><column_name>area_km2</column_name><stream_name>area_km2</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_ext_ibge, os.path.join(DIR_PIPELINES, "extracao_ibge_municipios.hpl"))

    # 2. Extracao DataSUS Dengue CSV com parametro MES_REF
    xml_ext_datasus = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info>
    <name>extracao_datasus_dengue</name>
    <pipeline_type>Normal</pipeline_type>
    <parameters>
      <parameter>
        <name>MES_REF</name>
        <default_value>2026-08</default_value>
        <description>Mes de referencia YYYY-MM para notificacoes</description>
      </parameter>
    </parameters>
  </info>
  <order>
    <hop><from>CSV DataSUS Dengue Parametrizado</from><to>Gravar staging.datasus_dengue</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV DataSUS Dengue Parametrizado</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/datasus_dengue_${MES_REF}.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>id_notificacao</name><type>String</type></field>
      <field><name>cod_mun_6</name><type>String</type></field>
      <field><name>data_notificacao</name><type>String</type></field>
      <field><name>casos_notificados</name><type>String</type></field>
      <field><name>casos_confirmados</name><type>String</type></field>
      <field><name>classificacao</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.datasus_dengue</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>datasus_dengue</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>id_notificacao</column_name><stream_name>id_notificacao</stream_name></field>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>data_notificacao</column_name><stream_name>data_notificacao</stream_name></field>
      <field><column_name>casos_notificados</column_name><stream_name>casos_notificados</stream_name></field>
      <field><column_name>casos_confirmados</column_name><stream_name>casos_confirmados</stream_name></field>
      <field><column_name>classificacao</column_name><stream_name>classificacao</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_ext_datasus, os.path.join(DIR_PIPELINES, "extracao_datasus_dengue.hpl"))

    # 3. Extracao INMET Chuva CSV
    xml_ext_inmet = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_inmet_chuva</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>CSV INMET Pluviometria</from><to>Gravar staging.inmet_chuva</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV INMET Pluviometria</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/inmet_chuva.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>cod_mun_6</name><type>String</type></field>
      <field><name>chuva_acumulada_mm</name><type>String</type></field>
      <field><name>dias_com_chuva</name><type>String</type></field>
      <field><name>estacao_monitorada</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.inmet_chuva</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>inmet_chuva</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>chuva_acumulada_mm</column_name><stream_name>chuva_acumulada_mm</stream_name></field>
      <field><column_name>dias_com_chuva</column_name><stream_name>dias_com_chuva</stream_name></field>
      <field><column_name>estacao_monitorada</column_name><stream_name>estacao_monitorada</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_ext_inmet, os.path.join(DIR_PIPELINES, "extracao_inmet_chuva.hpl"))

    # 4. Extracao CNES Leitos Hospitalares CSV
    xml_ext_cnes = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_cnes_leitos</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>CSV CNES Leitos</from><to>Gravar staging.cnes_leitos</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV CNES Leitos</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/cnes_leitos_hospitalares.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>cod_mun_6</name><type>String</type></field>
      <field><name>municipio</name><type>String</type></field>
      <field><name>leitos_clinicos</name><type>String</type></field>
      <field><name>leitos_uti</name><type>String</type></field>
      <field><name>postos_saude</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.cnes_leitos</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>cnes_leitos</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>municipio</column_name><stream_name>municipio</stream_name></field>
      <field><column_name>leitos_clinicos</column_name><stream_name>leitos_clinicos</stream_name></field>
      <field><column_name>leitos_uti</column_name><stream_name>leitos_uti</stream_name></field>
      <field><column_name>postos_saude</column_name><stream_name>postos_saude</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_ext_cnes, os.path.join(DIR_PIPELINES, "extracao_cnes_leitos.hpl"))

    # 5. Extracao Alertas Vigilancia MongoDB
    xml_ext_alertas = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_alertas_vigilancia</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Ler Staging Alertas</from><to>Gravar staging.alertas_vigilancia</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Ler Staging Alertas</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT id_alerta, cod_mun_6, cidade, nivel_risco, acao, data FROM staging.alertas_vigilancia LIMIT 10</sql>
  </transform>
  <transform>
    <name>Gravar staging.alertas_vigilancia</name>
    <type>Dummy</type>
  </transform>
</pipeline>"""
    salvar_xml(xml_ext_alertas, os.path.join(DIR_PIPELINES, "extracao_alertas_vigilancia.hpl"))

    # 6. Padronizacao IBGE Municipios (Silver + Quarentena)
    xml_padr_ibge = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>padroniza_ibge_municipios</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Ler staging.ibge_municipios</from><to>Limpar Textos e UF</to><enabled>Y</enabled></hop>
    <hop><from>Limpar Textos e UF</from><to>Converter Populacao e Area</to><enabled>Y</enabled></hop>
    <hop><from>Converter Populacao e Area</from><to>Gravar silver.municipios</to><enabled>Y</enabled></hop>
    <hop><from>Converter Populacao e Area</from><to>Motivo Quarentena IBGE</to><enabled>Y</enabled><error_handling>Y</error_handling></hop>
    <hop><from>Motivo Quarentena IBGE</from><to>Gravar Quarentena</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Ler staging.ibge_municipios</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT cod_mun, cod_mun_6, nome_municipio, uf, regiao, populacao, area_km2 FROM staging.ibge_municipios</sql>
  </transform>
  <transform>
    <name>Limpar Textos e UF</name>
    <type>StringOperations</type>
    <fields>
      <field><in_stream_name>nome_municipio</in_stream_name><trim_type>both</trim_type><init_cap>Y</init_cap></field>
      <field><in_stream_name>uf</in_stream_name><trim_type>both</trim_type><lower_upper>upper</lower_upper></field>
    </fields>
  </transform>
  <transform>
    <name>Converter Populacao e Area</name>
    <type>SelectValues</type>
    <fields>
      <select_unspecified>N</select_unspecified>
      <meta>
        <name>cod_mun_6</name><type>String</type>
      </meta>
      <meta>
        <name>cod_mun</name><type>String</type>
      </meta>
      <meta>
        <name>nome_municipio</name><type>String</type>
      </meta>
      <meta>
        <name>uf</name><type>String</type>
      </meta>
      <meta>
        <name>regiao</name><type>String</type>
      </meta>
      <meta>
        <name>populacao</name><type>Integer</type><conversion_mask>#</conversion_mask>
      </meta>
      <meta>
        <name>area_km2</name><type>Number</type><conversion_mask>#.##</conversion_mask><decimal_symbol>,</decimal_symbol>
      </meta>
    </fields>
  </transform>
  <transform>
    <name>Gravar silver.municipios</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>municipios</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>cod_mun</column_name><stream_name>cod_mun</stream_name></field>
      <field><column_name>nome_municipio</column_name><stream_name>nome_municipio</stream_name></field>
      <field><column_name>uf</column_name><stream_name>uf</stream_name></field>
      <field><column_name>regiao</column_name><stream_name>regiao</stream_name></field>
      <field><column_name>populacao</column_name><stream_name>populacao</stream_name></field>
      <field><column_name>area_km2</column_name><stream_name>area_km2</stream_name></field>
    </fields>
  </transform>
  <transform>
    <name>Motivo Quarentena IBGE</name>
    <type>Constant</type>
    <fields>
      <field>
        <name>pipeline_origem</name><type>String</type><nullif>padroniza_ibge_municipios</nullif><length>50</length><precision>-1</precision><set_empty_string>N</set_empty_string>
      </field>
      <field>
        <name>motivo_erro</name><type>String</type><nullif>Populacao invalida ou erro de casting numerico</nullif><length>255</length><precision>-1</precision><set_empty_string>N</set_empty_string>
      </field>
    </fields>
  </transform>
  <transform>
    <name>Gravar Quarentena</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>rejeitados</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>pipeline_origem</column_name><stream_name>pipeline_origem</stream_name></field>
      <field><column_name>motivo_erro</column_name><stream_name>motivo_erro</stream_name></field>
      <field><column_name>registro_bruto</column_name><stream_name>nome_municipio</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_padr_ibge, os.path.join(DIR_PIPELINES, "padroniza_ibge_municipios.hpl"))

    # 7. Padronizacao DataSUS Dengue (Silver + Quarentena)
    xml_padr_dengue = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>padroniza_datasus_dengue</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Ler staging.datasus_dengue</from><to>Validar e Converter Tipos</to><enabled>Y</enabled></hop>
    <hop><from>Validar e Converter Tipos</from><to>Gravar silver.notificacoes_dengue</to><enabled>Y</enabled></hop>
    <hop><from>Validar e Converter Tipos</from><to>Motivo Quarentena DataSUS</to><enabled>Y</enabled><error_handling>Y</error_handling></hop>
    <hop><from>Motivo Quarentena DataSUS</from><to>Gravar Quarentena DataSUS</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Ler staging.datasus_dengue</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT id_notificacao, cod_mun_6, data_notificacao, casos_notificados, casos_confirmados, classificacao FROM staging.datasus_dengue</sql>
  </transform>
  <transform>
    <name>Validar e Converter Tipos</name>
    <type>SelectValues</type>
    <fields>
      <select_unspecified>N</select_unspecified>
      <meta>
        <name>id_notificacao</name><type>String</type>
      </meta>
      <meta>
        <name>cod_mun_6</name><type>String</type>
      </meta>
      <meta>
        <name>data_notificacao</name><type>Date</type><conversion_mask>yyyy-MM-dd</conversion_mask>
      </meta>
      <meta>
        <name>casos_notificados</name><type>Integer</type><conversion_mask>#</conversion_mask>
      </meta>
      <meta>
        <name>casos_confirmados</name><type>Integer</type><conversion_mask>#</conversion_mask>
      </meta>
      <meta>
        <name>classificacao</name><type>String</type>
      </meta>
    </fields>
  </transform>
  <transform>
    <name>Gravar silver.notificacoes_dengue</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>notificacoes_dengue</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>id_notificacao</column_name><stream_name>id_notificacao</stream_name></field>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>data_notificacao</column_name><stream_name>data_notificacao</stream_name></field>
      <field><column_name>casos_notificados</column_name><stream_name>casos_notificados</stream_name></field>
      <field><column_name>casos_confirmados</column_name><stream_name>casos_confirmados</stream_name></field>
      <field><column_name>classificacao</column_name><stream_name>classificacao</stream_name></field>
    </fields>
  </transform>
  <transform>
    <name>Motivo Quarentena DataSUS</name>
    <type>Constant</type>
    <fields>
      <field>
        <name>pipeline_origem</name><type>String</type><nullif>padroniza_datasus_dengue</nullif><length>50</length><precision>-1</precision><set_empty_string>N</set_empty_string>
      </field>
      <field>
        <name>motivo_erro</name><type>String</type><nullif>Data de notificacao fora do formato YYYY-MM-DD ou casos invalidos</nullif><length>255</length><precision>-1</precision><set_empty_string>N</set_empty_string>
      </field>
    </fields>
  </transform>
  <transform>
    <name>Gravar Quarentena DataSUS</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>rejeitados</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>pipeline_origem</column_name><stream_name>pipeline_origem</stream_name></field>
      <field><column_name>motivo_erro</column_name><stream_name>motivo_erro</stream_name></field>
      <field><column_name>registro_bruto</column_name><stream_name>id_notificacao</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_padr_dengue, os.path.join(DIR_PIPELINES, "padroniza_datasus_dengue.hpl"))

    # 8. Padronizacao INMET Chuva (Silver + Quarentena)
    xml_padr_chuva = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>padroniza_inmet_chuva</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Ler staging.inmet_chuva</from><to>Converter Tipos Pluviometria</to><enabled>Y</enabled></hop>
    <hop><from>Converter Tipos Pluviometria</from><to>Gravar silver.inmet_chuva</to><enabled>Y</enabled></hop>
    <hop><from>Converter Tipos Pluviometria</from><to>Motivo Quarentena Chuva</to><enabled>Y</enabled><error_handling>Y</error_handling></hop>
    <hop><from>Motivo Quarentena Chuva</from><to>Gravar Quarentena Chuva</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Ler staging.inmet_chuva</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT cod_mun_6, chuva_acumulada_mm, dias_com_chuva, estacao_monitorada FROM staging.inmet_chuva</sql>
  </transform>
  <transform>
    <name>Converter Tipos Pluviometria</name>
    <type>SelectValues</type>
    <fields>
      <select_unspecified>N</select_unspecified>
      <meta>
        <name>cod_mun_6</name><type>String</type>
      </meta>
      <meta>
        <name>chuva_acumulada_mm</name><type>Number</type><conversion_mask>#.##</conversion_mask><decimal_symbol>,</decimal_symbol>
      </meta>
      <meta>
        <name>dias_com_chuva</name><type>Integer</type><conversion_mask>#</conversion_mask>
      </meta>
      <meta>
        <name>estacao_monitorada</name><type>String</type>
      </meta>
    </fields>
  </transform>
  <transform>
    <name>Gravar silver.inmet_chuva</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>inmet_chuva</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>chuva_acumulada_mm</column_name><stream_name>chuva_acumulada_mm</stream_name></field>
      <field><column_name>dias_com_chuva</column_name><stream_name>dias_com_chuva</stream_name></field>
      <field><column_name>estacao_monitorada</column_name><stream_name>estacao_monitorada</stream_name></field>
    </fields>
  </transform>
  <transform>
    <name>Motivo Quarentena Chuva</name>
    <type>Constant</type>
    <fields>
      <field>
        <name>pipeline_origem</name><type>String</type><nullif>padroniza_inmet_chuva</nullif><length>50</length><precision>-1</precision><set_empty_string>N</set_empty_string>
      </field>
      <field>
        <name>motivo_erro</name><type>String</type><nullif>Precipitacao invalida ou dias com chuva negativo</nullif><length>255</length><precision>-1</precision><set_empty_string>N</set_empty_string>
      </field>
    </fields>
  </transform>
  <transform>
    <name>Gravar Quarentena Chuva</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>rejeitados</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>pipeline_origem</column_name><stream_name>pipeline_origem</stream_name></field>
      <field><column_name>motivo_erro</column_name><stream_name>motivo_erro</stream_name></field>
      <field><column_name>registro_bruto</column_name><stream_name>cod_mun_6</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_padr_chuva, os.path.join(DIR_PIPELINES, "padroniza_inmet_chuva.hpl"))

    # 9. Padronizacao CNES Leitos SUS
    xml_padr_cnes = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>padroniza_cnes_leitos</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Ler staging.cnes_leitos</from><to>Converter Inteiros Leitos</to><enabled>Y</enabled></hop>
    <hop><from>Converter Inteiros Leitos</from><to>Gravar silver.cnes_leitos</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Ler staging.cnes_leitos</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT cod_mun_6, municipio, leitos_clinicos, leitos_uti, postos_saude FROM staging.cnes_leitos</sql>
  </transform>
  <transform>
    <name>Converter Inteiros Leitos</name>
    <type>SelectValues</type>
    <fields>
      <select_unspecified>N</select_unspecified>
      <meta>
        <name>cod_mun_6</name><type>String</type>
      </meta>
      <meta>
        <name>municipio</name><type>String</type>
      </meta>
      <meta>
        <name>leitos_clinicos</name><type>Integer</type><conversion_mask>#</conversion_mask>
      </meta>
      <meta>
        <name>leitos_uti</name><type>Integer</type><conversion_mask>#</conversion_mask>
      </meta>
      <meta>
        <name>postos_saude</name><type>Integer</type><conversion_mask>#</conversion_mask>
      </meta>
    </fields>
  </transform>
  <transform>
    <name>Gravar silver.cnes_leitos</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>cnes_leitos</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>municipio</column_name><stream_name>municipio</stream_name></field>
      <field><column_name>leitos_clinicos</column_name><stream_name>leitos_clinicos</stream_name></field>
      <field><column_name>leitos_uti</column_name><stream_name>leitos_uti</stream_name></field>
      <field><column_name>postos_saude</column_name><stream_name>postos_saude</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_padr_cnes, os.path.join(DIR_PIPELINES, "padroniza_cnes_leitos.hpl"))

    # 10. Padronizacao Alertas Vigilancia
    xml_padr_alertas = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>padroniza_alertas_vigilancia</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Ler staging.alertas_vigilancia</from><to>Gravar silver.alertas_vigilancia</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Ler staging.alertas_vigilancia</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT id_alerta, cod_mun_6, cidade, nivel_risco, acao, data FROM staging.alertas_vigilancia</sql>
  </transform>
  <transform>
    <name>Gravar silver.alertas_vigilancia</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>alertas_vigilancia</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>id_alerta</column_name><stream_name>id_alerta</stream_name></field>
      <field><column_name>cod_mun_6</column_name><stream_name>cod_mun_6</stream_name></field>
      <field><column_name>cidade</column_name><stream_name>cidade</stream_name></field>
      <field><column_name>nivel_risco</column_name><stream_name>nivel_risco</stream_name></field>
      <field><column_name>acao</column_name><stream_name>acao</stream_name></field>
      <field><column_name>data</column_name><stream_name>data</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml(xml_padr_alertas, os.path.join(DIR_PIPELINES, "padroniza_alertas_vigilancia.hpl"))

def gerar_workflows_brasil():
    # 1. exemplo04_carga_municipios.hwf (Workflow didático passo 2)
    xml_ex4 = """<?xml version="1.0" encoding="UTF-8"?>
<workflow>
  <name>exemplo04_carga_municipios</name>
  <name_sync_with_filename>Y</name_sync_with_filename>
  <description>Workflow didático: Truncate Staging -> Extracao CSV IBGE -> Padronizacao Silver</description>
  <actions>
    <action>
      <name>Start</name>
      <type>SPECIAL</type>
      <repeat>N</repeat>
      <nr>0</nr>
      <xloc>80</xloc>
      <yloc>120</yloc>
    </action>
    <action>
      <name>Truncate staging.ibge_municipios</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sql>TRUNCATE TABLE staging.ibge_municipios;</sql>
      <sqlfromfile>N</sqlfromfile>
      <nr>0</nr>
      <xloc>240</xloc>
      <yloc>120</yloc>
    </action>
    <action>
      <name>Extracao IBGE Municipios</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_ibge_municipios.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>440</xloc>
      <yloc>120</yloc>
    </action>
    <action>
      <name>Padronizacao IBGE Silver</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/padroniza_ibge_municipios.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>640</xloc>
      <yloc>120</yloc>
    </action>
    <action>
      <name>Sucesso</name>
      <type>SUCCESS</type>
      <nr>0</nr>
      <xloc>820</xloc>
      <yloc>120</yloc>
    </action>
  </actions>
  <hops>
    <hop><from>Start</from><to>Truncate staging.ibge_municipios</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>Y</unconditional></hop>
    <hop><from>Truncate staging.ibge_municipios</from><to>Extracao IBGE Municipios</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao IBGE Municipios</from><to>Padronizacao IBGE Silver</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padronizacao IBGE Silver</from><to>Sucesso</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
  </hops>
</workflow>"""
    salvar_xml(xml_ex4, os.path.join(DIR_WORKFLOWS, "exemplo04_carga_municipios.hwf"))

    # 2. carga_diaria.hwf (Workflow Mestre com as 5 Fontes Brasileiras, Teste de Fogo MongoDB, Quarentena e SQL ELT)
    xml_mestre = """<?xml version="1.0" encoding="UTF-8"?>
<workflow>
  <name>carga_diaria</name>
  <name_sync_with_filename>Y</name_sync_with_filename>
  <description>Workflow Mestre Brasileiro: Truncate Staging -> 5 Fontes Brasil -> Teste de Fogo Mongo -> Silver &amp; Quarentena -> SQL ELT Indicadores</description>
  <parameters>
    <parameter>
      <name>MES_REF</name>
      <default_value>2026-08</default_value>
      <description>Mes de referencia YYYY-MM para notificacoes DataSUS</description>
    </parameter>
  </parameters>
  <actions>
    <action>
      <name>Start</name>
      <type>SPECIAL</type>
      <repeat>N</repeat>
      <nr>0</nr>
      <xloc>60</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>SQL: Truncate Staging e Silver Brasil</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sql>TRUNCATE TABLE staging.ibge_municipios, staging.datasus_dengue, staging.inmet_chuva, staging.cnes_leitos, staging.alertas_vigilancia, silver.municipios, silver.notificacoes_dengue, silver.inmet_chuva, silver.cnes_leitos, silver.alertas_vigilancia, silver.rejeitados CASCADE;</sql>
      <sqlfromfile>N</sqlfromfile>
      <nr>0</nr>
      <xloc>200</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Fonte 1: IBGE Municipios (CSV)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_ibge_municipios.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>360</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Fonte 2: DataSUS Dengue (${MES_REF})</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_datasus_dengue.hpl</filename>
      <loglevel>Basic</loglevel>
      <parameters><pass_all_parameters>Y</pass_all_parameters></parameters>
      <nr>0</nr>
      <xloc>540</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Fonte 3: INMET Chuva (CSV)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_inmet_chuva.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>700</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Fonte 4: CNES Leitos SUS (Postgres)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_cnes_leitos.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>880</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Fonte 5: Alertas MongoDB (Teste de Fogo)</name>
      <type>SHELL</type>
      <insertScript>Y</insertScript>
      <script>mongosh --eval "db.adminCommand('ping')" --quiet</script>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>1080</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Padroniza IBGE (Silver)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/padroniza_ibge_municipios.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>1080</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Padroniza DataSUS Dengue (Silver)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/padroniza_datasus_dengue.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>880</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Padroniza INMET Chuva (Silver)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/padroniza_inmet_chuva.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>700</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Padroniza CNES Leitos (Silver)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/padroniza_cnes_leitos.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>540</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>SQL ELT: Indicadores Municipais</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sqlfilename>${PROJECT_HOME}/sql/04_elt_indicadores_municipais.sql</sqlfilename>
      <sqlfromfile>Y</sqlfromfile>
      <nr>0</nr>
      <xloc>360</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Log: Sucesso Completo Brasil</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Basic</loglevel>
      <logmessage>CARGA BRASIL CONCLUIDA COM SUCESSO! 5 FONTES PROCESSADAS, SILVER, QUARENTENA E ELT PRONTOS. MES_REF=${MES_REF}</logmessage>
      <nr>0</nr>
      <xloc>180</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Log de Erro Convergente</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Error</loglevel>
      <logmessage>ERRO CRITICO NA ESTEIRA BRASILEIRA! CONVERGINDO FLUXO VERMELHO PARA ABORT...</logmessage>
      <nr>0</nr>
      <xloc>600</xloc>
      <yloc>400</yloc>
    </action>
    <action>
      <name>Abort</name>
      <type>ABORT</type>
      <message>Execucao da Carga Diaria abortada com falha.</message>
      <nr>0</nr>
      <xloc>800</xloc>
      <yloc>400</yloc>
    </action>
  </actions>
  <hops>
    <hop><from>Start</from><to>SQL: Truncate Staging e Silver Brasil</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>Y</unconditional></hop>
    <hop><from>SQL: Truncate Staging e Silver Brasil</from><to>Fonte 1: IBGE Municipios (CSV)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>SQL: Truncate Staging e Silver Brasil</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 1: IBGE Municipios (CSV)</from><to>Fonte 2: DataSUS Dengue (${MES_REF})</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 1: IBGE Municipios (CSV)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 2: DataSUS Dengue (${MES_REF})</from><to>Fonte 3: INMET Chuva (CSV)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 2: DataSUS Dengue (${MES_REF})</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 3: INMET Chuva (CSV)</from><to>Fonte 4: CNES Leitos SUS (Postgres)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 3: INMET Chuva (CSV)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 4: CNES Leitos SUS (Postgres)</from><to>Fonte 5: Alertas MongoDB (Teste de Fogo)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 4: CNES Leitos SUS (Postgres)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 5: Alertas MongoDB (Teste de Fogo)</from><to>Padroniza IBGE (Silver)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Fonte 5: Alertas MongoDB (Teste de Fogo)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza IBGE (Silver)</from><to>Padroniza DataSUS Dengue (Silver)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza IBGE (Silver)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza DataSUS Dengue (Silver)</from><to>Padroniza INMET Chuva (Silver)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza DataSUS Dengue (Silver)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza INMET Chuva (Silver)</from><to>Padroniza CNES Leitos (Silver)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza INMET Chuva (Silver)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza CNES Leitos (Silver)</from><to>SQL ELT: Indicadores Municipais</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza CNES Leitos (Silver)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>SQL ELT: Indicadores Municipais</from><to>Log: Sucesso Completo Brasil</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>SQL ELT: Indicadores Municipais</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Log de Erro Convergente</from><to>Abort</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>Y</unconditional></hop>
  </hops>
</workflow>"""
    salvar_xml(xml_mestre, os.path.join(DIR_WORKFLOWS, "carga_diaria.hwf"))
    salvar_xml(xml_mestre, os.path.join(DIR_WORKFLOWS, "carga_diaria_brasil.hwf"))

if __name__ == "__main__":
    print("🚀 Gerando Pipelines e Workflows XML das 5 Fontes Brasileiras...")
    gerar_todas_pipelines_brasil()
    gerar_workflows_brasil()
    print("✨ Concluído com sucesso!")
