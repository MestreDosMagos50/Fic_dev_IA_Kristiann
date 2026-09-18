import os
import pandas as pd

# Define os caminhos dos arquivos de entrada
caminho_ibge = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR.csv"
if not os.path.exists(caminho_ibge):
    caminho_ibge_alt = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR_20260520/Agregados_por_municipios_basico_BR.csv"
    if os.path.exists(caminho_ibge_alt):
        caminho_ibge = caminho_ibge_alt

DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
caminho_dengue = "/home/ficdevia-16-tarde/Downloads/DENGBR26.csv"
caminho_hpl = os.path.join(DIR_ATUAL, "integracao_brasil.hpl")
caminho_saida = os.path.join(DIR_ATUAL, "resultado_brasil_integrado")
caminho_hpl_downloads = "/home/ficdevia-16-tarde/Downloads/integracao_brasil.hpl"

# Lê as colunas para mapeamento posicional correto no Hop CSVInput
ibge_cols = pd.read_csv(caminho_ibge, sep=';', nrows=1, encoding='iso-8859-1').columns.tolist()
dengue_cols = pd.read_csv(caminho_dengue, nrows=1).columns.tolist()

ibge_fields_xml = '\n'.join([
    f'      <field><name>{c}</name><type>Integer</type><trim_type>both</trim_type></field>' if c == 'v0001'
    else f'      <field><name>{c}</name><type>String</type><trim_type>both</trim_type></field>'
    for c in ibge_cols
])

dengue_fields_xml = '\n'.join([
    f'      <field><name>{c}</name><type>String</type><trim_type>both</trim_type></field>'
    for c in dengue_cols
])

hpl_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<pipeline>
  <info>
    <name>integracao_brasil</name>
    <name_sync_with_filename>Y</name_sync_with_filename>
    <description>Integracao Dengue DataSUS e Censo Populacional IBGE</description>
    <pipeline_type>Normal</pipeline_type>
  </info>
  <order>
    <hop>
      <from>Dados Populacionais (IBGE)</from>
      <to>Ajusta Chave IBGE (6 digitos)</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Ajusta Chave IBGE (6 digitos)</from>
      <to>Lookup Dengue</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Microdados Dengue (DataSUS)</from>
      <to>Agrupa Notificacoes Dengue</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Agrupa Notificacoes Dengue</from>
      <to>Lookup Dengue</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Lookup Dengue</from>
      <to>Exporta Base Consolidada</to>
      <enabled>Y</enabled>
    </hop>
  </order>
  <transform>
    <name>Dados Populacionais (IBGE)</name>
    <type>CSVInput</type>
    <filename>{caminho_ibge}</filename>
    <separator>;</separator>
    <enclosure>"</enclosure>
    <header>Y</header>
    <buffer_size>50000</buffer_size>
    <encoding>ISO-8859-1</encoding>
    <fields>
{ibge_fields_xml}
    </fields>
    <GUI><xloc>140</xloc><yloc>120</yloc></GUI>
  </transform>
  <transform>
    <name>Ajusta Chave IBGE (6 digitos)</name>
    <type>StringCut</type>
    <fields>
      <field>
        <in_stream_name>CD_MUN</in_stream_name>
        <out_stream_name>cod_mun_6</out_stream_name>
        <cut_from>0</cut_from>
        <cut_to>6</cut_to>
      </field>
    </fields>
    <GUI><xloc>380</xloc><yloc>120</yloc></GUI>
  </transform>
  <transform>
    <name>Microdados Dengue (DataSUS)</name>
    <type>CSVInput</type>
    <filename>{caminho_dengue}</filename>
    <separator>,</separator>
    <enclosure>"</enclosure>
    <header>Y</header>
    <buffer_size>50000</buffer_size>
    <encoding>UTF-8</encoding>
    <fields>
{dengue_fields_xml}
    </fields>
    <GUI><xloc>140</xloc><yloc>260</yloc></GUI>
  </transform>
  <transform>
    <name>Agrupa Notificacoes Dengue</name>
    <type>MemoryGroupBy</type>
    <give_back_row>N</give_back_row>
    <group>
      <field><name>ID_MN_RESI</name></field>
    </group>
    <fields>
      <field>
        <aggregate>total_casos_dengue</aggregate>
        <subject>ID_MN_RESI</subject>
        <type>COUNT_ALL</type>
      </field>
    </fields>
    <GUI><xloc>380</xloc><yloc>260</yloc></GUI>
  </transform>
  <transform>
    <name>Lookup Dengue</name>
    <type>StreamLookup</type>
    <from>Agrupa Notificacoes Dengue</from>
    <input_sorted>N</input_sorted>
    <preserve_memory>Y</preserve_memory>
    <lookup>
      <key>
        <name>cod_mun_6</name>
        <field>ID_MN_RESI</field>
      </key>
      <value>
        <name>total_casos_dengue</name>
        <rename>total_casos_dengue</rename>
        <default>0</default>
        <type>Integer</type>
      </value>
    </lookup>
    <GUI><xloc>620</xloc><yloc>180</yloc></GUI>
  </transform>
  <transform>
    <name>Exporta Base Consolidada</name>
    <type>TextFileOutput</type>
    <separator>;</separator>
    <enclosure>"</enclosure>
    <header>Y</header>
    <format>UNIX</format>
    <encoding>UTF-8</encoding>
    <file>
      <name>{caminho_saida}</name>
      <extention>csv</extention>
      <create_parent_folder>Y</create_parent_folder>
    </file>
    <fields>
      <field><name>CD_MUN</name><type>String</type></field>
      <field><name>cod_mun_6</name><type>String</type></field>
      <field><name>NM_MUN</name><type>String</type></field>
      <field><name>NM_UF</name><type>String</type></field>
      <field><name>AREA_KM2</name><type>String</type></field>
      <field><name>v0001</name><type>Integer</type></field>
      <field><name>total_casos_dengue</name><type>Integer</type></field>
    </fields>
    <GUI><xloc>860</xloc><yloc>180</yloc></GUI>
  </transform>
</pipeline>
"""

with open(caminho_hpl, "w", encoding="utf-8") as f:
    f.write(hpl_content.strip())

with open(caminho_hpl_downloads, "w", encoding="utf-8") as f:
    f.write(hpl_content.strip())

print(f"Pipeline '{caminho_hpl}' gerado com sucesso na pasta aula 13 e espelhado em Downloads!")