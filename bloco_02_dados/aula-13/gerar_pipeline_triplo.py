import os
import glob
import unicodedata
import re
import pandas as pd
import numpy as np

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ''
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto.upper().strip()

def limpar_nome_estacao(nome):
    nome = normalizar_texto(nome)
    # Remove sufixos como ' - VILA MILITAR', ' (PONTE ALTA)', etc.
    return re.split(r'[-–(]', nome)[0].strip()

def preparar_dados_inmet():
    pasta_inmet = "/home/ficdevia-16-tarde/Downloads/2024"
    caminho_ibge_base = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR.csv"
    if not os.path.exists(caminho_ibge_base):
        caminho_ibge_base = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR_20260520/Agregados_por_municipios_basico_BR.csv"

    DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
    caminho_chuva_out = os.path.join(DIR_ATUAL, "inmet_chuva_consolidada_2024.csv")
    caminho_chuva_downloads = "/home/ficdevia-16-tarde/Downloads/inmet_chuva_consolidada_2024.csv"

    print("1/3 - Mapeando municípios do IBGE para relacionamento geográfico...")
    df_ibge = pd.read_csv(caminho_ibge_base, sep=';', encoding='iso-8859-1', usecols=['CD_MUN', 'NM_MUN', 'NM_UF'])
    
    uf_sigla_map = {
        'Rondônia': 'RO', 'Acre': 'AC', 'Amazonas': 'AM', 'Roraima': 'RR', 'Pará': 'PA', 'Amapá': 'AP', 'Tocantins': 'TO',
        'Maranhão': 'MA', 'Piauí': 'PI', 'Ceará': 'CE', 'Rio Grande do Norte': 'RN', 'Paraíba': 'PB', 'Pernambuco': 'PE',
        'Alagoas': 'AL', 'Sergipe': 'SE', 'Bahia': 'BA', 'Minas Gerais': 'MG', 'Espírito Santo': 'ES', 'Rio de Janeiro': 'RJ',
        'São Paulo': 'SP', 'Paraná': 'PR', 'Santa Catarina': 'SC', 'Rio Grande do Sul': 'RS', 'Mato Grosso do Sul': 'MS',
        'Mato Grosso': 'MT', 'Goiás': 'GO', 'Distrito Federal': 'DF'
    }
    df_ibge['UF_SIGLA'] = df_ibge['NM_UF'].map(uf_sigla_map)
    df_ibge['cod_mun_6'] = df_ibge['CD_MUN'].astype(str).str[:6]
    df_ibge['KEY'] = df_ibge['NM_MUN'].apply(normalizar_texto) + '_' + df_ibge['UF_SIGLA']
    ibge_lookup = dict(zip(df_ibge['KEY'], df_ibge['cod_mun_6']))

    print(f"2/3 - Processando 565 estações meteorológicas automáticas do INMET em {pasta_inmet}...")
    arquivos_inmet = glob.glob(os.path.join(pasta_inmet, "*.CSV"))
    if not arquivos_inmet:
        print(f"Aviso: Nenhum arquivo CSV encontrado em {pasta_inmet}. Usando base prévia se existir.")
        return caminho_chuva_out

    estacoes_dados = []
    for f in arquivos_inmet:
        try:
            with open(f, 'r', encoding='latin1') as fp:
                linhas_meta = [fp.readline() for _ in range(8)]
            
            meta = dict(l.strip().split(';', 1) for l in linhas_meta if ';' in l)
            uf = meta.get('UF:', '').strip().upper()
            estacao_raw = meta.get('ESTACAO:', '').strip()
            estacao_limpa = limpar_nome_estacao(estacao_raw)
            key = estacao_limpa + '_' + uf
            cod_mun = ibge_lookup.get(key, '')

            # Lê a coluna de precipitação horária (coluna de índice 2)
            df_st = pd.read_csv(f, sep=';', skiprows=8, encoding='latin1', usecols=[2], decimal=',')
            s_precip = pd.to_numeric(df_st.iloc[:, 0], errors='coerce').fillna(0)
            s_precip = s_precip[s_precip >= 0]
            chuva_acumulada = round(float(s_precip.sum()), 1)

            estacoes_dados.append({
                'cod_mun_6': cod_mun,
                'uf': uf,
                'estacao': estacao_limpa,
                'chuva_mm': chuva_acumulada
            })
        except Exception as e:
            continue

    df_estacoes = pd.DataFrame(estacoes_dados)
    medias_uf = df_estacoes.groupby('uf')['chuva_mm'].mean().round(1).to_dict()

    # Monta a base consolidada para todos os 5.570 municípios
    linhas_finais = []
    cods_processados = set()

    # 1. Municípios que possuem estação meteorológica própria
    for _, r in df_estacoes.iterrows():
        cod = r['cod_mun_6']
        if cod and cod not in cods_processados:
            linhas_finais.append({
                'cod_mun_6': cod,
                'chuva_mm': str(r['chuva_mm']).replace('.', ','),
                'tem_estacao': 'S'
            })
            cods_processados.add(cod)

    # 2. Municípios sem estação direta: recebem a média pluviométrica de sua respectiva UF
    for _, r in df_ibge.iterrows():
        cod = str(r['cod_mun_6'])
        uf = r['UF_SIGLA']
        if cod not in cods_processados:
            media_estado = medias_uf.get(uf, 1000.0)
            linhas_finais.append({
                'cod_mun_6': cod,
                'chuva_mm': str(media_estado).replace('.', ','),
                'tem_estacao': 'N'
            })
            cods_processados.add(cod)

    df_final_chuva = pd.DataFrame(linhas_finais)
    df_final_chuva.to_csv(caminho_chuva_out, sep=';', index=False, encoding='utf-8')
    try:
        df_final_chuva.to_csv(caminho_chuva_downloads, sep=';', index=False, encoding='utf-8')
    except Exception:
        pass
    print(f"Base pluviométrica salva em: {caminho_chuva_out} ({len(df_final_chuva)} municípios).")
    return caminho_chuva_out

def gerar_pipeline_triplo():
    caminho_ibge = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR.csv"
    if not os.path.exists(caminho_ibge):
        caminho_ibge_alt = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR_20260520/Agregados_por_municipios_basico_BR.csv"
        if os.path.exists(caminho_ibge_alt):
            caminho_ibge = caminho_ibge_alt

    caminho_dengue = "/home/ficdevia-16-tarde/Downloads/DENGBR26.csv"
    caminho_chuva = preparar_dados_inmet()
    
    DIR_ATUAL = os.path.dirname(os.path.abspath(__file__))
    caminho_hpl = os.path.join(DIR_ATUAL, "integracao_brasil_triplo.hpl")
    caminho_saida = os.path.join(DIR_ATUAL, "resultado_brasil_triplo_integrado")
    caminho_hpl_downloads = "/home/ficdevia-16-tarde/Downloads/integracao_brasil_triplo.hpl"

    print("3/3 - Gerando arquivo de pipeline do Apache Hop (integracao_brasil_triplo.hpl)...")
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
    <name>integracao_brasil_triplo</name>
    <name_sync_with_filename>Y</name_sync_with_filename>
    <description>Integracao Tripla: Dengue DataSUS + Censo Populacional IBGE + Chuva INMET</description>
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
      <to>Lookup Chuva INMET</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Dados Pluviometricos INMET (Chuva)</from>
      <to>Lookup Chuva INMET</to>
      <enabled>Y</enabled>
    </hop>
    <hop>
      <from>Lookup Chuva INMET</from>
      <to>Exporta Base Tripla Consolidada</to>
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
    <GUI><xloc>600</xloc><yloc>180</yloc></GUI>
  </transform>
  <transform>
    <name>Dados Pluviometricos INMET (Chuva)</name>
    <type>CSVInput</type>
    <filename>{caminho_chuva}</filename>
    <separator>;</separator>
    <enclosure>"</enclosure>
    <header>Y</header>
    <buffer_size>50000</buffer_size>
    <encoding>UTF-8</encoding>
    <fields>
      <field><name>cod_mun_6</name><type>String</type><trim_type>both</trim_type></field>
      <field><name>chuva_mm</name><type>Number</type><decimal>,</decimal><trim_type>both</trim_type></field>
      <field><name>tem_estacao</name><type>String</type><trim_type>both</trim_type></field>
    </fields>
    <GUI><xloc>600</xloc><yloc>320</yloc></GUI>
  </transform>
  <transform>
    <name>Lookup Chuva INMET</name>
    <type>StreamLookup</type>
    <from>Dados Pluviometricos INMET (Chuva)</from>
    <input_sorted>N</input_sorted>
    <preserve_memory>Y</preserve_memory>
    <lookup>
      <key>
        <name>cod_mun_6</name>
        <field>cod_mun_6</field>
      </key>
      <value>
        <name>chuva_mm</name>
        <rename>chuva_mm</rename>
        <default>0</default>
        <type>Number</type>
      </value>
      <value>
        <name>tem_estacao</name>
        <rename>tem_estacao</rename>
        <default>N</default>
        <type>String</type>
      </value>
    </lookup>
    <GUI><xloc>820</xloc><yloc>180</yloc></GUI>
  </transform>
  <transform>
    <name>Exporta Base Tripla Consolidada</name>
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
      <field><name>chuva_mm</name><type>Number</type></field>
      <field><name>tem_estacao</name><type>String</type></field>
    </fields>
    <GUI><xloc>1060</xloc><yloc>180</yloc></GUI>
  </transform>
</pipeline>
"""

    with open(caminho_hpl, "w", encoding="utf-8") as f:
        f.write(hpl_content.strip())

    try:
        with open(caminho_hpl_downloads, "w", encoding="utf-8") as f:
            f.write(hpl_content.strip())
    except Exception:
        pass

    print(f"Sucesso! Nova pipeline tripla gerada em: {caminho_hpl}")
    print(f"Espelho em Downloads: {caminho_hpl_downloads}")
    print(f"Saída configurada para: {caminho_saida}.csv")

if __name__ == "__main__":
    gerar_pipeline_triplo()
