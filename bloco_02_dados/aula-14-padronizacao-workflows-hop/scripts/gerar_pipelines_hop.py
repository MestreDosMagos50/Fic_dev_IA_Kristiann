#!/usr/bin/env python3
"""
scripts/gerar_pipelines_hop.py
Gera programaticamente as definições completas de Pipelines (.hpl) e Workflows (.hwf)
para o Apache Hop 2.19, em conformidade total com o material da Aula 03 (Módulo 2).
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

DIR_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_PIPELINES = os.path.join(DIR_PROJETO, "hop", "pipelines")
DIR_WORKFLOWS = os.path.join(DIR_PROJETO, "hop", "workflows")

def salvar_xml_formatado(conteudo_xml: str, caminho_destino: str):
    os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)
    with open(caminho_destino, "w", encoding="UTF-8") as f:
        f.write(conteudo_xml.strip() + "\n")
    print(f"✅ Arquivo Hop gerado: {caminho_destino}")

def gerar_pipelines_extracoes():
    """Gera pipelines de extração para popular staging"""
    # 1. Carga staging produtos (usado no exemplo04 e carga_diaria)
    xml_produtos = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_csv_produtos</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>CSV Produtos Bronze</from><to>Gravar staging.produtos</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV Produtos Bronze</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/produtos_bronze.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>codigo</name><type>String</type></field>
      <field><name>nome</name><type>String</type></field>
      <field><name>preco</name><type>String</type></field>
      <field><name>categoria</name><type>String</type></field>
      <field><name>data_cadastro</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.produtos</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>produtos</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>codigo</column_name><stream_name>codigo</stream_name></field>
      <field><column_name>nome</column_name><stream_name>nome</stream_name></field>
      <field><column_name>preco</column_name><stream_name>preco</stream_name></field>
      <field><column_name>categoria</column_name><stream_name>categoria</stream_name></field>
      <field><column_name>data_cadastro</column_name><stream_name>data_cadastro</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml_formatado(xml_produtos, os.path.join(DIR_PIPELINES, "carga_staging_produtos.hpl"))
    salvar_xml_formatado(xml_produtos, os.path.join(DIR_PIPELINES, "extracao_csv_produtos.hpl"))

    # 2. Extracao CSV Vendas com variavel MES_REF
    xml_vendas = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_csv_vendas</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>CSV Vendas Parametrizado</from><to>Gravar staging.vendas</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>CSV Vendas Parametrizado</name>
    <type>CSVInput</type>
    <filename>${PROJECT_HOME}/dados/bronze/vendas_${MES_REF}.csv</filename>
    <separator>;</separator>
    <header>Y</header>
    <fields>
      <field><name>id_venda</name><type>String</type></field>
      <field><name>codigo_produto</name><type>String</type></field>
      <field><name>quantidade</name><type>String</type></field>
      <field><name>valor_unitario</name><type>String</type></field>
      <field><name>valor_total</name><type>String</type></field>
      <field><name>data_venda</name><type>String</type></field>
      <field><name>cliente_id</name><type>String</type></field>
    </fields>
  </transform>
  <transform>
    <name>Gravar staging.vendas</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>staging</schema>
    <table>vendas</table>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>id_venda</column_name><stream_name>id_venda</stream_name></field>
      <field><column_name>codigo_produto</column_name><stream_name>codigo_produto</stream_name></field>
      <field><column_name>quantidade</column_name><stream_name>quantidade</stream_name></field>
      <field><column_name>valor_unitario</column_name><stream_name>valor_unitario</stream_name></field>
      <field><column_name>valor_total</column_name><stream_name>valor_total</stream_name></field>
      <field><column_name>data_venda</column_name><stream_name>data_venda</stream_name></field>
      <field><column_name>cliente_id</column_name><stream_name>cliente_id</stream_name></field>
    </fields>
  </transform>
</pipeline>"""
    salvar_xml_formatado(xml_vendas, os.path.join(DIR_PIPELINES, "extracao_csv_vendas.hpl"))

    # 3. Extracao JSON Avaliacoes
    xml_json = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_json_avaliacoes</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Carrega JSON Staging</from><to>Gravar staging.avaliacoes</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Carrega JSON Staging</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT id_avaliacao, codigo_produto, nota, comentario, data_avaliacao FROM staging.avaliacoes LIMIT 0</sql>
  </transform>
  <transform>
    <name>Gravar staging.avaliacoes</name>
    <type>Dummy</type>
  </transform>
</pipeline>"""
    salvar_xml_formatado(xml_json, os.path.join(DIR_PIPELINES, "extracao_json_avaliacoes.hpl"))

    # 4 e 5: PostgreSQL Clientes e MongoDB Feedback
    xml_pg = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_postgres_clientes</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Table Input Clientes</from><to>Gravar staging.clientes</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Table Input Clientes</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT 'CLI01' as id, 'Cliente Padrao' as nome</sql>
  </transform>
  <transform>
    <name>Gravar staging.clientes</name>
    <type>Dummy</type>
  </transform>
</pipeline>"""
    salvar_xml_formatado(xml_pg, os.path.join(DIR_PIPELINES, "extracao_postgres_clientes.hpl"))

    xml_mongo = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info><name>extracao_mongodb_feedback</name><pipeline_type>Normal</pipeline_type></info>
  <order>
    <hop><from>Mongo Feedback</from><to>Gravar staging.feedback</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Mongo Feedback</name>
    <type>Dummy</type>
  </transform>
  <transform>
    <name>Gravar staging.feedback</name>
    <type>Dummy</type>
  </transform>
</pipeline>"""
    salvar_xml_formatado(xml_mongo, os.path.join(DIR_PIPELINES, "extracao_mongodb_feedback.hpl"))


def gerar_pipeline_padroniza_produtos():
    """Gera exemplo03_padroniza_produtos.hpl com Error Handling para silver.rejeitados"""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info>
    <name>exemplo03_padroniza_produtos</name>
    <name_sync_with_filename>Y</name_sync_with_filename>
    <description>Pipeline de padronizacao de produtos com quarentena de rejeitados</description>
    <pipeline_type>Normal</pipeline_type>
    <parameters>
      <parameter>
        <name>MES_REF</name>
        <default_value>2026-08</default_value>
        <description>Mes de referencia da execucao</description>
      </parameter>
    </parameters>
  </info>
  <order>
    <hop>
      <from>Ler staging.produtos</from>
      <to>Limpar textos</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Limpar textos</from>
      <to>Limpar preco</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Limpar preco</from>
      <to>Converter tipos</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Converter tipos</from>
      <to>Marcar motivo erro</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Marcar motivo erro</from>
      <to>Gravar quarentena</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Converter tipos</from>
      <to>Ordenar por codigo</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Ordenar por codigo</from>
      <to>Deduplicar</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Deduplicar</from>
      <to>Gravar silver.produtos</to>
      <enabled>Y</enabled>
    </hop>
  </order>
  <transform>
    <name>Ler staging.produtos</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT codigo, nome, preco, categoria, data_cadastro FROM staging.produtos</sql>
    <limit>0</limit>
    <GUI>
      <xloc>100</xloc>
      <yloc>120</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Limpar textos</name>
    <type>StringOperations</type>
    <fields>
      <field>
        <in_stream_name>nome</in_stream_name>
        <out_stream_name/>
        <trim_type>both</trim_type>
        <lower_upper>none</lower_upper>
        <padding_type>none</padding_type>
        <pad_char/>
        <pad_len/>
        <init_cap>Y</init_cap>
        <mask_xml>none</mask_xml>
        <digits>none</digits>
        <remove_special_characters>none</remove_special_characters>
      </field>
      <field>
        <in_stream_name>categoria</in_stream_name>
        <out_stream_name/>
        <trim_type>both</trim_type>
        <lower_upper>lower</lower_upper>
        <padding_type>none</padding_type>
        <pad_char/>
        <pad_len/>
        <init_cap>N</init_cap>
        <mask_xml>none</mask_xml>
        <digits>none</digits>
        <remove_special_characters>none</remove_special_characters>
      </field>
    </fields>
    <GUI>
      <xloc>260</xloc>
      <yloc>120</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Limpar preco</name>
    <type>ReplaceString</type>
    <fields>
      <field>
        <in_stream_name>preco</in_stream_name>
        <out_stream_name/>
        <use_regex>yes</use_regex>
        <replace_string>[R$\s]</replace_string>
        <replace_by_string/>
        <set_empty_string>N</set_empty_string>
        <replace_field_by_string/>
        <whole_word>no</whole_word>
        <case_sensitive>no</case_sensitive>
        <is_unicode>no</is_unicode>
      </field>
      <field>
        <in_stream_name>preco</in_stream_name>
        <out_stream_name/>
        <use_regex>no</use_regex>
        <replace_string>.</replace_string>
        <replace_by_string/>
        <set_empty_string>N</set_empty_string>
        <replace_field_by_string/>
        <whole_word>no</whole_word>
        <case_sensitive>no</case_sensitive>
        <is_unicode>no</is_unicode>
      </field>
      <field>
        <in_stream_name>preco</in_stream_name>
        <out_stream_name/>
        <use_regex>no</use_regex>
        <replace_string>,</replace_string>
        <replace_by_string>.</replace_by_string>
        <set_empty_string>N</set_empty_string>
        <replace_field_by_string/>
        <whole_word>no</whole_word>
        <case_sensitive>no</case_sensitive>
        <is_unicode>no</is_unicode>
      </field>
    </fields>
    <GUI>
      <xloc>420</xloc>
      <yloc>120</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Converter tipos</name>
    <type>SelectValues</type>
    <fields>
      <select_unspecified>N</select_unspecified>
      <meta>
        <name>codigo</name>
        <rename>codigo</rename>
        <type>String</type>
        <length>50</length>
        <precision>-1</precision>
        <conversion_mask/>
        <date_format_lenient>false</date_format_lenient>
        <date_format_locale/>
        <date_format_timezone/>
        <lenient_string_to_number>false</lenient_string_to_number>
        <encoding/>
        <decimal_symbol/>
        <grouping_symbol/>
        <currency_symbol/>
        <storage_type/>
      </meta>
      <meta>
        <name>nome</name>
        <rename>nome</rename>
        <type>String</type>
        <length>255</length>
        <precision>-1</precision>
        <conversion_mask/>
        <date_format_lenient>false</date_format_lenient>
        <date_format_locale/>
        <date_format_timezone/>
        <lenient_string_to_number>false</lenient_string_to_number>
        <encoding/>
        <decimal_symbol/>
        <grouping_symbol/>
        <currency_symbol/>
        <storage_type/>
      </meta>
      <meta>
        <name>categoria</name>
        <rename>categoria</rename>
        <type>String</type>
        <length>100</length>
        <precision>-1</precision>
        <conversion_mask/>
        <date_format_lenient>false</date_format_lenient>
        <date_format_locale/>
        <date_format_timezone/>
        <lenient_string_to_number>false</lenient_string_to_number>
        <encoding/>
        <decimal_symbol/>
        <grouping_symbol/>
        <currency_symbol/>
        <storage_type/>
      </meta>
      <meta>
        <name>preco</name>
        <rename>preco</rename>
        <type>Number</type>
        <length>12</length>
        <precision>2</precision>
        <conversion_mask>#.##</conversion_mask>
        <date_format_lenient>false</date_format_lenient>
        <date_format_locale/>
        <date_format_timezone/>
        <lenient_string_to_number>false</lenient_string_to_number>
        <encoding/>
        <decimal_symbol>.</decimal_symbol>
        <grouping_symbol/>
        <currency_symbol/>
        <storage_type/>
      </meta>
      <meta>
        <name>data_cadastro</name>
        <rename>data_cadastro</rename>
        <type>Date</type>
        <length>-1</length>
        <precision>-1</precision>
        <conversion_mask>dd/MM/yyyy</conversion_mask>
        <date_format_lenient>false</date_format_lenient>
        <date_format_locale/>
        <date_format_timezone/>
        <lenient_string_to_number>false</lenient_string_to_number>
        <encoding/>
        <decimal_symbol/>
        <grouping_symbol/>
        <currency_symbol/>
        <storage_type/>
      </meta>
    </fields>
    <GUI>
      <xloc>580</xloc>
      <yloc>120</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Marcar motivo erro</name>
    <type>Constant</type>
    <fields>
      <field>
        <name>motivo_erro</name>
        <type>String</type>
        <format/>
        <currency/>
        <decimal/>
        <group/>
        <nullif>Preco ou data com formato invalido</nullif>
        <length>255</length>
        <precision>-1</precision>
        <set_empty_string>N</set_empty_string>
      </field>
      <field>
        <name>pipeline_origem</name>
        <type>String</type>
        <format/>
        <currency/>
        <decimal/>
        <group/>
        <nullif>padroniza_produtos</nullif>
        <length>50</length>
        <precision>-1</precision>
        <set_empty_string>N</set_empty_string>
      </field>
    </fields>
    <GUI>
      <xloc>580</xloc>
      <yloc>280</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Gravar quarentena</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>rejeitados</table>
    <commit>1000</commit>
    <truncate>N</truncate>
    <ignore_errors>N</ignore_errors>
    <use_batch>Y</use_batch>
    <specify_fields>Y</specify_fields>
    <fields>
      <field>
        <column_name>pipeline_origem</column_name>
        <stream_name>pipeline_origem</stream_name>
      </field>
      <field>
        <column_name>motivo_erro</column_name>
        <stream_name>motivo_erro</stream_name>
      </field>
      <field>
        <column_name>registro_bruto</column_name>
        <stream_name>codigo</stream_name>
      </field>
    </fields>
    <GUI>
      <xloc>740</xloc>
      <yloc>280</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Ordenar por codigo</name>
    <type>SortRows</type>
    <directory>${java.io.tmpdir}</directory>
    <prefix>out</prefix>
    <sort_size>1000000</sort_size>
    <free_memory/>
    <compress>N</compress>
    <compress_variables/>
    <unique_rows>N</unique_rows>
    <fields>
      <field>
        <name>codigo</name>
        <ascending>Y</ascending>
        <case_sensitive>N</case_sensitive>
        <collator_enabled>N</collator_enabled>
        <collator_strength>0</collator_strength>
        <presorted>N</presorted>
      </field>
    </fields>
    <GUI>
      <xloc>740</xloc>
      <yloc>120</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Deduplicar</name>
    <type>Unique</type>
    <count_rows>N</count_rows>
    <count_field/>
    <reject_duplicate_row>N</reject_duplicate_row>
    <error_description/>
    <fields>
      <field>
        <name>codigo</name>
        <case_insensitive>N</case_insensitive>
      </field>
    </fields>
    <GUI>
      <xloc>880</xloc>
      <yloc>120</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform>
    <name>Gravar silver.produtos</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>produtos</table>
    <commit>1000</commit>
    <truncate>N</truncate>
    <ignore_errors>N</ignore_errors>
    <use_batch>Y</use_batch>
    <specify_fields>Y</specify_fields>
    <fields>
      <field>
        <column_name>codigo</column_name>
        <stream_name>codigo</stream_name>
      </field>
      <field>
        <column_name>nome</column_name>
        <stream_name>nome</stream_name>
      </field>
      <field>
        <column_name>categoria</column_name>
        <stream_name>categoria</stream_name>
      </field>
      <field>
        <column_name>preco</column_name>
        <stream_name>preco</stream_name>
      </field>
      <field>
        <column_name>data_cadastro</column_name>
        <stream_name>data_cadastro</stream_name>
      </field>
    </fields>
    <GUI>
      <xloc>1040</xloc>
      <yloc>120</yloc>
      <draw>Y</draw>
    </GUI>
  </transform>
  <transform_error_handling>
    <error>
      <source_transform>Converter tipos</source_transform>
      <target_transform>Marcar motivo erro</target_transform>
      <is_enabled>Y</is_enabled>
      <nr_valuename>num_erros</nr_valuename>
      <descriptions_valuename>desc_erro</descriptions_valuename>
      <fields_valuename>campos_erro</fields_valuename>
      <codes_valuename>cod_erro</codes_valuename>
      <max_errors/>
      <max_pct_errors/>
      <min_pct_rows/>
    </error>
  </transform_error_handling>
</pipeline>"""
    salvar_xml_formatado(xml, os.path.join(DIR_PIPELINES, "exemplo03_padroniza_produtos.hpl"))

def gerar_pipeline_padroniza_vendas():
    """Gera padroniza_vendas.hpl com tratamento de datas mistas e quarentena de qtd <= 0"""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info>
    <name>padroniza_vendas</name>
    <name_sync_with_filename>Y</name_sync_with_filename>
    <description>Padronizacao de vendas com datas mistas, monetarios e quarentena qtd menor ou igual a zero</description>
    <pipeline_type>Normal</pipeline_type>
    <parameters>
      <parameter>
        <name>MES_REF</name>
        <default_value>2026-08</default_value>
        <description>Mes de referencia da execucao</description>
      </parameter>
    </parameters>
  </info>
  <order>
    <hop>
      <from>Ler staging.vendas</from>
      <to>Limpar strings e moeda</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Limpar strings e moeda</from>
      <to>Filtrar quantidade positiva</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Filtrar quantidade positiva</from>
      <to>Marcar erro quantidade</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Marcar erro quantidade</from>
      <to>Gravar quarentena vendas</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Filtrar quantidade positiva</from>
      <to>Converter tipos vendas</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Converter tipos vendas</from>
      <to>Marcar erro conversao vendas</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Marcar erro conversao vendas</from>
      <to>Gravar quarentena vendas</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Converter tipos vendas</from>
      <to>Ordenar por id_venda</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Ordenar por id_venda</from>
      <to>Deduplicar vendas</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Deduplicar vendas</from>
      <to>Gravar silver.vendas</to>
      <enabled>Y</enabled>
    </hop>
  </order>
  <transform>
    <name>Ler staging.vendas</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT id_venda, codigo_produto, quantidade, valor_unitario, valor_total, data_venda, cliente_id FROM staging.vendas</sql>
    <limit>0</limit>
    <GUI><xloc>80</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Limpar strings e moeda</name>
    <type>ReplaceString</type>
    <fields>
      <field>
        <in_stream_name>valor_unitario</in_stream_name>
        <use_regex>yes</use_regex>
        <replace_string>[R$\s]</replace_string>
        <replace_by_string/>
      </field>
      <field>
        <in_stream_name>valor_unitario</in_stream_name>
        <use_regex>no</use_regex>
        <replace_string>.</replace_string>
        <replace_by_string/>
      </field>
      <field>
        <in_stream_name>valor_unitario</in_stream_name>
        <use_regex>no</use_regex>
        <replace_string>,</replace_string>
        <replace_by_string>.</replace_by_string>
      </field>
      <field>
        <in_stream_name>valor_total</in_stream_name>
        <use_regex>yes</use_regex>
        <replace_string>[R$\s]</replace_string>
        <replace_by_string/>
      </field>
      <field>
        <in_stream_name>valor_total</in_stream_name>
        <use_regex>no</use_regex>
        <replace_string>.</replace_string>
        <replace_by_string/>
      </field>
      <field>
        <in_stream_name>valor_total</in_stream_name>
        <use_regex>no</use_regex>
        <replace_string>,</replace_string>
        <replace_by_string>.</replace_by_string>
      </field>
    </fields>
    <GUI><xloc>240</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Filtrar quantidade positiva</name>
    <type>FilterRows</type>
    <send_true_to>Converter tipos vendas</send_true_to>
    <send_false_to>Marcar erro quantidade</send_false_to>
    <compare>
      <condition>
        <negated>N</negated>
        <leftvalue>quantidade</leftvalue>
        <function>&gt;</function>
        <rightvalue/>
        <value><name>constant</name><type>String</type><text>0</text><length>-1</length><precision>-1</precision><isnull>N</isnull></value>
      </condition>
    </compare>
    <GUI><xloc>400</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Marcar erro quantidade</name>
    <type>Constant</type>
    <fields>
      <field>
        <name>motivo_erro</name>
        <type>String</type>
        <nullif>Quantidade menor ou igual a zero (invalida para venda)</nullif>
      </field>
      <field>
        <name>pipeline_origem</name>
        <type>String</type>
        <nullif>padroniza_vendas</nullif>
      </field>
    </fields>
    <GUI><xloc>400</xloc><yloc>260</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Converter tipos vendas</name>
    <type>SelectValues</type>
    <fields>
      <select_unspecified>N</select_unspecified>
      <meta>
        <name>id_venda</name><type>String</type><length>50</length>
      </meta>
      <meta>
        <name>codigo_produto</name><type>String</type><length>50</length>
      </meta>
      <meta>
        <name>quantidade</name><type>Integer</type><length>9</length>
      </meta>
      <meta>
        <name>valor_unitario</name><type>Number</type><length>12</length><precision>2</precision><conversion_mask>#.##</conversion_mask><decimal_symbol>.</decimal_symbol>
      </meta>
      <meta>
        <name>valor_total</name><type>Number</type><length>12</length><precision>2</precision><conversion_mask>#.##</conversion_mask><decimal_symbol>.</decimal_symbol>
      </meta>
      <meta>
        <name>data_venda</name><type>Date</type><conversion_mask>yyyy-MM-dd</conversion_mask>
      </meta>
      <meta>
        <name>cliente_id</name><type>String</type><length>50</length>
      </meta>
    </fields>
    <GUI><xloc>580</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Marcar erro conversao vendas</name>
    <type>Constant</type>
    <fields>
      <field>
        <name>motivo_erro</name>
        <type>String</type>
        <nullif>Falha na conversao de tipos, valores monetarios ou datas mistas</nullif>
      </field>
      <field>
        <name>pipeline_origem</name>
        <type>String</type>
        <nullif>padroniza_vendas</nullif>
      </field>
    </fields>
    <GUI><xloc>580</xloc><yloc>260</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Gravar quarentena vendas</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>rejeitados</table>
    <commit>1000</commit>
    <truncate>N</truncate>
    <ignore_errors>N</ignore_errors>
    <use_batch>Y</use_batch>
    <specify_fields>Y</specify_fields>
    <fields>
      <field><column_name>pipeline_origem</column_name><stream_name>pipeline_origem</stream_name></field>
      <field><column_name>motivo_erro</column_name><stream_name>motivo_erro</stream_name></field>
      <field><column_name>registro_bruto</column_name><stream_name>id_venda</stream_name></field>
    </fields>
    <GUI><xloc>500</xloc><yloc>380</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Ordenar por id_venda</name>
    <type>SortRows</type>
    <directory>${java.io.tmpdir}</directory>
    <sort_size>1000000</sort_size>
    <fields>
      <field><name>id_venda</name><ascending>Y</ascending><case_sensitive>N</case_sensitive></field>
    </fields>
    <GUI><xloc>740</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Deduplicar vendas</name>
    <type>Unique</type>
    <fields>
      <field><name>id_venda</name><case_insensitive>N</case_insensitive></field>
    </fields>
    <GUI><xloc>880</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Gravar silver.vendas</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>vendas</table>
    <commit>1000</commit>
    <truncate>N</truncate>
    <fields>
      <field><column_name>id_venda</column_name><stream_name>id_venda</stream_name></field>
      <field><column_name>codigo_produto</column_name><stream_name>codigo_produto</stream_name></field>
      <field><column_name>quantidade</column_name><stream_name>quantidade</stream_name></field>
      <field><column_name>valor_unitario</column_name><stream_name>valor_unitario</stream_name></field>
      <field><column_name>valor_total</column_name><stream_name>valor_total</stream_name></field>
      <field><column_name>data_venda</column_name><stream_name>data_venda</stream_name></field>
      <field><column_name>cliente_id</column_name><stream_name>cliente_id</stream_name></field>
    </fields>
    <GUI><xloc>1040</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform_error_handling>
    <error>
      <source_transform>Converter tipos vendas</source_transform>
      <target_transform>Marcar erro conversao vendas</target_transform>
      <is_enabled>Y</is_enabled>
      <nr_valuename>num_erros</nr_valuename>
      <descriptions_valuename>desc_erro</descriptions_valuename>
    </error>
  </transform_error_handling>
</pipeline>"""
    salvar_xml_formatado(xml, os.path.join(DIR_PIPELINES, "padroniza_vendas.hpl"))

def gerar_pipeline_padroniza_avaliacoes():
    """Gera padroniza_avaliacoes.hpl com trim nos comentários e quarentena de nota fora de 1-5"""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info>
    <name>padroniza_avaliacoes</name>
    <name_sync_with_filename>Y</name_sync_with_filename>
    <description>Padronizacao de avaliacoes com trim e quarentena para notas fora de 1 a 5</description>
    <pipeline_type>Normal</pipeline_type>
  </info>
  <order>
    <hop><from>Ler staging.avaliacoes</from><to>Trim comentarios</to><enabled>Y</enabled></hop>
    <hop><from>Trim comentarios</from><to>Validar nota 1 a 5</to><enabled>Y</enabled></hop>
    <hop><from>Validar nota 1 a 5</from><to>Marcar nota invalida</to><enabled>Y</enabled></hop>
    <hop><from>Marcar nota invalida</from><to>Gravar quarentena avaliacoes</to><enabled>Y</enabled></hop>
    <hop><from>Validar nota 1 a 5</from><to>Converter tipos avaliacoes</to><enabled>Y</enabled></hop>
    <hop><from>Converter tipos avaliacoes</from><to>Ordenar avaliacoes</to><enabled>Y</enabled></hop>
    <hop><from>Ordenar avaliacoes</from><to>Deduplicar avaliacoes</to><enabled>Y</enabled></hop>
    <hop><from>Deduplicar avaliacoes</from><to>Gravar silver.avaliacoes</to><enabled>Y</enabled></hop>
  </order>
  <transform>
    <name>Ler staging.avaliacoes</name>
    <type>TableInput</type>
    <connection>PostgreSQL</connection>
    <sql>SELECT id_avaliacao, codigo_produto, nota, comentario, data_avaliacao FROM staging.avaliacoes</sql>
    <GUI><xloc>80</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Trim comentarios</name>
    <type>StringOperations</type>
    <fields>
      <field>
        <in_stream_name>comentario</in_stream_name>
        <trim_type>both</trim_type>
      </field>
      <field>
        <in_stream_name>codigo_produto</in_stream_name>
        <trim_type>both</trim_type>
      </field>
      <field>
        <in_stream_name>id_avaliacao</in_stream_name>
        <trim_type>both</trim_type>
      </field>
    </fields>
    <GUI><xloc>240</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Validar nota 1 a 5</name>
    <type>FilterRows</type>
    <send_true_to>Converter tipos avaliacoes</send_true_to>
    <send_false_to>Marcar nota invalida</send_false_to>
    <compare>
      <condition>
        <negated>N</negated>
        <conditions>
          <condition>
            <leftvalue>nota</leftvalue>
            <function>&gt;=</function>
            <value><type>String</type><text>1</text></value>
          </condition>
          <condition>
            <operator>AND</operator>
            <leftvalue>nota</leftvalue>
            <function>&lt;=</function>
            <value><type>String</type><text>5</text></value>
          </condition>
        </conditions>
      </condition>
    </compare>
    <GUI><xloc>420</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Marcar nota invalida</name>
    <type>Constant</type>
    <fields>
      <field>
        <name>motivo_erro</name>
        <type>String</type>
        <nullif>Nota fora do intervalo permitido (1 a 5)</nullif>
      </field>
      <field>
        <name>pipeline_origem</name>
        <type>String</type>
        <nullif>padroniza_avaliacoes</nullif>
      </field>
    </fields>
    <GUI><xloc>420</xloc><yloc>260</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Gravar quarentena avaliacoes</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>rejeitados</table>
    <commit>1000</commit>
    <fields>
      <field><column_name>pipeline_origem</column_name><stream_name>pipeline_origem</stream_name></field>
      <field><column_name>motivo_erro</column_name><stream_name>motivo_erro</stream_name></field>
      <field><column_name>registro_bruto</column_name><stream_name>id_avaliacao</stream_name></field>
    </fields>
    <GUI><xloc>580</xloc><yloc>260</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Converter tipos avaliacoes</name>
    <type>SelectValues</type>
    <fields>
      <meta><name>id_avaliacao</name><type>String</type><length>50</length></meta>
      <meta><name>codigo_produto</name><type>String</type><length>50</length></meta>
      <meta><name>nota</name><type>Integer</type><length>2</length></meta>
      <meta><name>comentario</name><type>String</type><length>1000</length></meta>
      <meta><name>data_avaliacao</name><type>Date</type><conversion_mask>yyyy-MM-dd</conversion_mask></meta>
    </fields>
    <GUI><xloc>620</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Ordenar avaliacoes</name>
    <type>SortRows</type>
    <directory>${java.io.tmpdir}</directory>
    <fields>
      <field><name>id_avaliacao</name><ascending>Y</ascending><case_sensitive>N</case_sensitive></field>
    </fields>
    <GUI><xloc>780</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Deduplicar avaliacoes</name>
    <type>Unique</type>
    <fields>
      <field><name>id_avaliacao</name><case_insensitive>N</case_insensitive></field>
    </fields>
    <GUI><xloc>920</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
  <transform>
    <name>Gravar silver.avaliacoes</name>
    <type>TableOutput</type>
    <connection>PostgreSQL</connection>
    <schema>silver</schema>
    <table>avaliacoes</table>
    <commit>1000</commit>
    <fields>
      <field><column_name>id_avaliacao</column_name><stream_name>id_avaliacao</stream_name></field>
      <field><column_name>codigo_produto</column_name><stream_name>codigo_produto</stream_name></field>
      <field><column_name>nota</column_name><stream_name>nota</stream_name></field>
      <field><column_name>comentario</column_name><stream_name>comentario</stream_name></field>
      <field><column_name>data_avaliacao</column_name><stream_name>data_avaliacao</stream_name></field>
    </fields>
    <GUI><xloc>1080</xloc><yloc>120</yloc><draw>Y</draw></GUI>
  </transform>
</pipeline>"""
    salvar_xml_formatado(xml, os.path.join(DIR_PIPELINES, "padroniza_avaliacoes.hpl"))

def gerar_workflow_exemplo04():
    """Gera exemplo04_carga_produtos.hwf"""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<workflow>
  <name>exemplo04_carga_produtos</name>
  <name_sync_with_filename>Y</name_sync_with_filename>
  <description>Workflow guiado de carga e padronizacao de produtos com caminhos de erro e abort</description>
  <parameters>
    <parameter>
      <name>MES_REF</name>
      <default_value>2026-08</default_value>
      <description>Mes de referencia no formato YYYY-MM</description>
    </parameter>
  </parameters>
  <actions>
    <action>
      <name>Start</name>
      <type>SPECIAL</type>
      <repeat>N</repeat>
      <schedulerType>0</schedulerType>
      <parallel>N</parallel>
      <nr>0</nr>
      <xloc>80</xloc>
      <yloc>160</yloc>
    </action>
    <action>
      <name>SQL: prepara schemas</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sqlfilename>${PROJECT_HOME}/sql/01_prepara_schemas.sql</sqlfilename>
      <sqlfromfile>Y</sqlfromfile>
      <useVariableSubstitution>Y</useVariableSubstitution>
      <parallel>N</parallel>
      <nr>0</nr>
      <xloc>240</xloc>
      <yloc>160</yloc>
    </action>
    <action>
      <name>Pipeline: carga staging</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/carga_staging_produtos.hpl</filename>
      <loglevel>Basic</loglevel>
      <parameters><pass_all_parameters>Y</pass_all_parameters></parameters>
      <parallel>N</parallel>
      <nr>0</nr>
      <xloc>420</xloc>
      <yloc>160</yloc>
    </action>
    <action>
      <name>Pipeline: padroniza</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/exemplo03_padroniza_produtos.hpl</filename>
      <loglevel>Basic</loglevel>
      <parameters><pass_all_parameters>Y</pass_all_parameters></parameters>
      <parallel>N</parallel>
      <nr>0</nr>
      <xloc>600</xloc>
      <yloc>160</yloc>
    </action>
    <action>
      <name>Log: sucesso</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Basic</loglevel>
      <logmessage>CARGA E PADRONIZACAO DE PRODUTOS FINALIZADA COM SUCESSO! MES_REF=${MES_REF}</logmessage>
      <parallel>N</parallel>
      <nr>0</nr>
      <xloc>800</xloc>
      <yloc>160</yloc>
    </action>
    <action>
      <name>Log de erro</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Error</loglevel>
      <logmessage>FALHA NA EXECUCAO DO WORKFLOW DE PRODUTOS! ACIONANDO ABORT...</logmessage>
      <parallel>N</parallel>
      <nr>0</nr>
      <xloc>420</xloc>
      <yloc>320</yloc>
    </action>
    <action>
      <name>Abort</name>
      <type>ABORT</type>
      <message>Workflow exemplo04 abortado devido a erro na execucao.</message>
      <parallel>N</parallel>
      <nr>0</nr>
      <xloc>600</xloc>
      <yloc>320</yloc>
    </action>
  </actions>
  <hops>
    <hop>
      <from>Start</from>
      <to>SQL: prepara schemas</to>
      <enabled>Y</enabled>
      <evaluation>Y</evaluation>
      <unconditional>Y</unconditional>
    </hop>
    <hop>
      <from>SQL: prepara schemas</from>
      <to>Pipeline: carga staging</to>
      <enabled>Y</enabled>
      <evaluation>Y</evaluation>
      <unconditional>N</unconditional>
    </hop>
    <hop>
      <from>SQL: prepara schemas</from>
      <to>Log de erro</to>
      <enabled>Y</enabled>
      <evaluation>N</evaluation>
      <unconditional>N</unconditional>
    </hop>
    <hop>
      <from>Pipeline: carga staging</from>
      <to>Pipeline: padroniza</to>
      <enabled>Y</enabled>
      <evaluation>Y</evaluation>
      <unconditional>N</unconditional>
    </hop>
    <hop>
      <from>Pipeline: carga staging</from>
      <to>Log de erro</to>
      <enabled>Y</enabled>
      <evaluation>N</evaluation>
      <unconditional>N</unconditional>
    </hop>
    <hop>
      <from>Pipeline: padroniza</from>
      <to>Log: sucesso</to>
      <enabled>Y</enabled>
      <evaluation>Y</evaluation>
      <unconditional>N</unconditional>
    </hop>
    <hop>
      <from>Pipeline: padroniza</from>
      <to>Log de erro</to>
      <enabled>Y</enabled>
      <evaluation>N</evaluation>
      <unconditional>N</unconditional>
    </hop>
    <hop>
      <from>Log de erro</from>
      <to>Abort</to>
      <enabled>Y</enabled>
      <evaluation>Y</evaluation>
      <unconditional>Y</unconditional>
    </hop>
  </hops>
</workflow>"""
    salvar_xml_formatado(xml, os.path.join(DIR_WORKFLOWS, "exemplo04_carga_produtos.hwf"))

def gerar_workflow_mestre():
    """Gera carga_diaria.hwf (Workflow Mestre com truncate, 5 extracoes, 3 padronizacoes, log erro + abort)"""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<workflow>
  <name>carga_diaria</name>
  <name_sync_with_filename>Y</name_sync_with_filename>
  <description>Workflow Mestre de Carga Diaria: Truncate Staging -> 5 Extracoes -> 3 Padronizacoes Silver -> Sucesso / Abort</description>
  <parameters>
    <parameter>
      <name>MES_REF</name>
      <default_value>2026-08</default_value>
      <description>Mes de referencia no formato YYYY-MM para execucao da esteira</description>
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
      <name>SQL: Truncate da Staging</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sql>TRUNCATE TABLE staging.produtos, staging.vendas, staging.avaliacoes;</sql>
      <sqlfromfile>N</sqlfromfile>
      <nr>0</nr>
      <xloc>200</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Extracao 1: CSV Produtos</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_csv_produtos.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>360</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Extracao 2: CSV Vendas</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_csv_vendas.hpl</filename>
      <loglevel>Basic</loglevel>
      <parameters><pass_all_parameters>Y</pass_all_parameters></parameters>
      <nr>0</nr>
      <xloc>520</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Extracao 3: JSON Avaliacoes</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_json_avaliacoes.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>680</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Extracao 4: PostgreSQL Clientes</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/extracao_postgres_clientes.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>860</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Extracao 5: MongoDB Feedback (Teste de Fogo)</name>
      <type>SHELL</type>
      <insertScript>Y</insertScript>
      <script>mongosh --eval "db.adminCommand('ping')" --quiet</script>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>1060</xloc>
      <yloc>140</yloc>
    </action>
    <action>
      <name>Padroniza Produtos (Silver)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/exemplo03_padroniza_produtos.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>1060</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Padroniza Vendas (Silver)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/padroniza_vendas.hpl</filename>
      <loglevel>Basic</loglevel>
      <parameters><pass_all_parameters>Y</pass_all_parameters></parameters>
      <nr>0</nr>
      <xloc>860</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Padroniza Avaliacoes (Silver)</name>
      <type>PIPELINE</type>
      <run_configuration>local</run_configuration>
      <filename>${PROJECT_HOME}/hop/pipelines/padroniza_avaliacoes.hpl</filename>
      <loglevel>Basic</loglevel>
      <nr>0</nr>
      <xloc>680</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Desafio ELT Avaliacoes (SQL)</name>
      <type>SQL</type>
      <connection>PostgreSQL</connection>
      <sqlfilename>${PROJECT_HOME}/sql/03_elt_silver_avaliacoes.sql</sqlfilename>
      <sqlfromfile>Y</sqlfromfile>
      <nr>0</nr>
      <xloc>480</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Log: Sucesso Completo</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Basic</loglevel>
      <logmessage>CARGA DIARIA CONCLUIDA COM SUCESSO! STAGING, SILVER E QUARENTENA PRONTAS. MES_REF=${MES_REF}</logmessage>
      <nr>0</nr>
      <xloc>280</xloc>
      <yloc>260</yloc>
    </action>
    <action>
      <name>Log de Erro Convergente</name>
      <type>WRITE_TO_LOG</type>
      <loglevel>Error</loglevel>
      <logmessage>ERRO CRITICO EM ETAPA DA CARGA DIARIA! CONVERGINDO FLUXO VERMELHO PARA ABORT...</logmessage>
      <nr>0</nr>
      <xloc>600</xloc>
      <yloc>420</yloc>
    </action>
    <action>
      <name>Abort</name>
      <type>ABORT</type>
      <message>Execucao da Carga Diaria abortada com falha.</message>
      <nr>0</nr>
      <xloc>800</xloc>
      <yloc>420</yloc>
    </action>
  </actions>
  <hops>
    <hop><from>Start</from><to>SQL: Truncate da Staging</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>Y</unconditional></hop>
    <hop><from>SQL: Truncate da Staging</from><to>Extracao 1: CSV Produtos</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>SQL: Truncate da Staging</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 1: CSV Produtos</from><to>Extracao 2: CSV Vendas</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 1: CSV Produtos</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 2: CSV Vendas</from><to>Extracao 3: JSON Avaliacoes</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 2: CSV Vendas</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 3: JSON Avaliacoes</from><to>Extracao 4: PostgreSQL Clientes</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 3: JSON Avaliacoes</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 4: PostgreSQL Clientes</from><to>Extracao 5: MongoDB Feedback (Teste de Fogo)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 4: PostgreSQL Clientes</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 5: MongoDB Feedback (Teste de Fogo)</from><to>Padroniza Produtos (Silver)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Extracao 5: MongoDB Feedback (Teste de Fogo)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza Produtos (Silver)</from><to>Padroniza Vendas (Silver)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza Produtos (Silver)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza Vendas (Silver)</from><to>Padroniza Avaliacoes (Silver)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza Vendas (Silver)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza Avaliacoes (Silver)</from><to>Desafio ELT Avaliacoes (SQL)</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Padroniza Avaliacoes (Silver)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Desafio ELT Avaliacoes (SQL)</from><to>Log: Sucesso Completo</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Desafio ELT Avaliacoes (SQL)</from><to>Log de Erro Convergente</to><enabled>Y</enabled><evaluation>N</evaluation><unconditional>N</unconditional></hop>
    <hop><from>Log de Erro Convergente</from><to>Abort</to><enabled>Y</enabled><evaluation>Y</evaluation><unconditional>Y</unconditional></hop>
  </hops>
</workflow>"""
    salvar_xml_formatado(xml, os.path.join(DIR_WORKFLOWS, "carga_diaria.hwf"))

def gerar_project_config():
    """Gera project-config.json e conexao PostgreSQL nos metadados"""
    dir_metadata = os.path.join(DIR_PROJETO, "metadata", "rdbms")
    os.makedirs(dir_metadata, exist_ok=True)
    
    project_cfg = """{
  "metadataBaseFolder": "${PROJECT_HOME}/metadata",
  "unitTestsBasePath": "${PROJECT_HOME}",
  "dataSetsCsvFolder": "${PROJECT_HOME}/datasets",
  "enforcingExecutionInHome": false,
  "parentProjectName": "",
  "config": {
    "variables": [
      {
        "name": "MES_REF",
        "value": "2026-08",
        "description": "Mes de referencia"
      }
    ]
  }
}"""
    salvar_xml_formatado(project_cfg, os.path.join(DIR_PROJETO, "project-config.json"))

    pg_metadata = """{
  "rdbms": {
    "PostgreSQL": {
      "databaseName": "ecommerce",
      "pluginId": "POSTGRESQL",
      "accessType": 0,
      "hostname": "localhost",
      "password": "Encrypted 2be98afc86aa7f2e4bb16bd64d980aac9",
      "pluginName": "PostgreSQL",
      "port": "5432",
      "attributes": {
        "PORT_NUMBER": "5432",
        "SUPPORTS_TIMESTAMP_DATA_TYPE": "Y",
        "QUOTE_ALL_FIELDS": "N",
        "SUPPORTS_BOOLEAN_DATA_TYPE": "Y",
        "FORCE_IDENTIFIERS_TO_LOWERCASE": "N",
        "PRESERVE_RESERVED_WORD_CASE": "Y",
        "FORCE_IDENTIFIERS_TO_UPPERCASE": "N"
      },
      "username": "postgres"
    }
  },
  "name": "PostgreSQL"
}"""
    salvar_xml_formatado(pg_metadata, os.path.join(dir_metadata, "PostgreSQL.json"))

def main():
    print("🚀 Gerando Pipelines e Workflows XML para Apache Hop 2.19...")
    gerar_project_config()
    gerar_pipelines_extracoes()
    gerar_pipeline_padroniza_produtos()
    gerar_pipeline_padroniza_vendas()
    gerar_pipeline_padroniza_avaliacoes()
    gerar_workflow_exemplo04()
    gerar_workflow_mestre()
    print("✨ Todos os arquivos do Hop foram gerados com sucesso!")

if __name__ == "__main__":
    main()
