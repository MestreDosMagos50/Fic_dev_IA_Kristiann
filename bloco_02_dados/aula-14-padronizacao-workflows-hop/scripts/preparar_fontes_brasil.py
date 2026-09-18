#!/usr/bin/env python3
"""
scripts/preparar_fontes_brasil.py
Gera as 5 bases de dados brasileiras na camada Bronze (IBGE, DataSUS, INMET, CNES, Alertas NoSQL)
utilizando dados reais de municípios brasileiros e inserindo anomalias controladas para testar
a Quarentena da Arquitetura Medallion.
"""

import os
import json
import pandas as pd
import numpy as np

DIR_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_BRONZE = os.path.join(DIR_PROJETO, "dados", "bronze")
os.makedirs(DIR_BRONZE, exist_ok=True)

# Caminhos das bases reais em Downloads
p_ibge_raw = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR.csv"
if not os.path.exists(p_ibge_raw):
    p_ibge_raw = "/home/ficdevia-16-tarde/Downloads/Agregados_por_municipios_basico_BR_20260520/Agregados_por_municipios_basico_BR.csv"

p_inmet_raw = "/home/ficdevia-16-tarde/Downloads/inmet_chuva_consolidada_2024.csv"
p_dengue_raw = "/home/ficdevia-16-tarde/Downloads/DENGBR26.csv"

def gerar_fontes():
    print("🇧🇷 Preparando as 5 fontes de dados do Brasil...")

    # 1. Carrega uma amostragem representativa das cidades do IBGE (capitais e cidades principais de todas as regiões)
    cidades_selecionadas = [
        {"cod_mun": "3550308", "cod_mun_6": "355030", "nome_municipio": "São Paulo", "uf": "SP", "regiao": "Sudeste", "populacao": 11451245, "area_km2": 1521.11},
        {"cod_mun": "3304557", "cod_mun_6": "330455", "nome_municipio": "Rio de Janeiro", "uf": "RJ", "regiao": "Sudeste", "populacao": 6211423, "area_km2": 1200.33},
        {"cod_mun": "3106200", "cod_mun_6": "310620", "nome_municipio": "Belo Horizonte", "uf": "MG", "regiao": "Sudeste", "populacao": 2315560, "area_km2": 331.40},
        {"cod_mun": "5300108", "cod_mun_6": "530010", "nome_municipio": "Brasília", "uf": "DF", "regiao": "Centro-Oeste", "populacao": 2817068, "area_km2": 5760.78},
        {"cod_mun": "2927408", "cod_mun_6": "292740", "nome_municipio": "Salvador", "uf": "BA", "regiao": "Nordeste", "populacao": 2418005, "area_km2": 693.44},
        {"cod_mun": "2304400", "cod_mun_6": "230440", "nome_municipio": "Fortaleza", "uf": "CE", "regiao": "Nordeste", "populacao": 2428678, "area_km2": 312.41},
        {"cod_mun": "4106902", "cod_mun_6": "410690", "nome_municipio": "Curitiba", "uf": "PR", "regiao": "Sul", "populacao": 1773733, "area_km2": 435.04},
        {"cod_mun": "1302603", "cod_mun_6": "130260", "nome_municipio": "Manaus", "uf": "AM", "regiao": "Norte", "populacao": 2063547, "area_km2": 11401.09},
        {"cod_mun": "2611606", "cod_mun_6": "261160", "nome_municipio": "Recife", "uf": "PE", "regiao": "Nordeste", "populacao": 1488920, "area_km2": 218.84},
        {"cod_mun": "5208707", "cod_mun_6": "520870", "nome_municipio": "Goiânia", "uf": "GO", "regiao": "Centro-Oeste", "populacao": 1437237, "area_km2": 728.84},
        {"cod_mun": "1501402", "cod_mun_6": "150140", "nome_municipio": "Belém", "uf": "PA", "regiao": "Norte", "populacao": 1303389, "area_km2": 1059.46},
        {"cod_mun": "4314902", "cod_mun_6": "431490", "nome_municipio": "Porto Alegre", "uf": "RS", "regiao": "Sul", "populacao": 1332570, "area_km2": 496.68},
        {"cod_mun": "3509502", "cod_mun_6": "350950", "nome_municipio": "Campinas", "uf": "SP", "regiao": "Sudeste", "populacao": 1138309, "area_km2": 794.57},
        {"cod_mun": "3549805", "cod_mun_6": "354980", "nome_municipio": "São José dos Campos", "uf": "SP", "regiao": "Sudeste", "populacao": 697428, "area_km2": 1099.41},
        {"cod_mun": "3543402", "cod_mun_6": "354340", "nome_municipio": "Ribeirão Preto", "uf": "SP", "regiao": "Sudeste", "populacao": 698259, "area_km2": 650.92},
        {"cod_mun": "3170206", "cod_mun_6": "317020", "nome_municipio": "Uberlândia", "uf": "MG", "regiao": "Sudeste", "populacao": 713232, "area_km2": 4115.21},
        {"cod_mun": "4205407", "cod_mun_6": "420540", "nome_municipio": "Florianópolis", "uf": "SC", "regiao": "Sul", "populacao": 537213, "area_km2": 675.41},
        {"cod_mun": "3205309", "cod_mun_6": "320530", "nome_municipio": "Vitória", "uf": "ES", "regiao": "Sudeste", "populacao": 322869, "area_km2": 97.12},
        {"cod_mun": "5002704", "cod_mun_6": "500270", "nome_municipio": "Campo Grande", "uf": "MS", "regiao": "Centro-Oeste", "populacao": 897938, "area_km2": 8082.97},
        {"cod_mun": "5103403", "cod_mun_6": "510340", "nome_municipio": "Cuiabá", "uf": "MT", "regiao": "Centro-Oeste", "populacao": 650912, "area_km2": 3266.54},
        # Registros anômalos para quarentena do IBGE:
        {"cod_mun": "9999999", "cod_mun_6": "999999", "nome_municipio": "Cidade Fantasma Sem Habitante", "uf": "XX", "regiao": "Invalida", "populacao": -500, "area_km2": 0},
        {"cod_mun": "8888888", "cod_mun_6": "888888", "nome_municipio": "Municipio Com Populacao Nula", "uf": "YY", "regiao": "Invalida", "populacao": 0, "area_km2": 150},
        {"cod_mun": "3550308", "cod_mun_6": "355030", "nome_municipio": "São Paulo Duplicado", "uf": "SP", "regiao": "Sudeste", "populacao": 11451245, "area_km2": 1521.11}
    ]

    df_ibge = pd.DataFrame(cidades_selecionadas)
    p_ibge_out = os.path.join(DIR_BRONZE, "ibge_municipios.csv")
    df_ibge.to_csv(p_ibge_out, sep=";", index=False)
    print(f"✅ Fonte 1 gerada (IBGE População): {len(df_ibge)} registros em {p_ibge_out}")

    # 2. Fonte 2: DataSUS Notificações de Dengue (Parametrizada por mês)
    notificacoes_dengue = [
        {"id_notificacao": "NOT-001", "cod_mun_6": "355030", "data_notificacao": "12/08/2026", "casos_notificados": 1420, "casos_confirmados": 1150, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-002", "cod_mun_6": "330455", "data_notificacao": "2026-08-13", "casos_notificados": 980, "casos_confirmados": 820, "classificacao": "Dengue com Sinais de Alarme"},
        {"id_notificacao": "NOT-003", "cod_mun_6": "310620", "data_notificacao": "14/08/2026", "casos_notificados": 2450, "casos_confirmados": 2100, "classificacao": "Dengue Grave"},
        {"id_notificacao": "NOT-004", "cod_mun_6": "530010", "data_notificacao": "2026-08-15", "casos_notificados": 3100, "casos_confirmados": 2890, "classificacao": "Dengue Grave"},
        {"id_notificacao": "NOT-005", "cod_mun_6": "292740", "data_notificacao": "16/08/2026", "casos_notificados": 450, "casos_confirmados": 380, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-006", "cod_mun_6": "230440", "data_notificacao": "17/08/2026", "casos_notificados": 520, "casos_confirmados": 440, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-007", "cod_mun_6": "410690", "data_notificacao": "2026-08-18", "casos_notificados": 310, "casos_confirmados": 260, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-008", "cod_mun_6": "130260", "data_notificacao": "19/08/2026", "casos_notificados": 180, "casos_confirmados": 150, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-009", "cod_mun_6": "261160", "data_notificacao": "20/08/2026", "casos_notificados": 610, "casos_confirmados": 530, "classificacao": "Dengue com Sinais de Alarme"},
        {"id_notificacao": "NOT-010", "cod_mun_6": "520870", "data_notificacao": "2026-08-21", "casos_notificados": 1890, "casos_confirmados": 1650, "classificacao": "Dengue Grave"},
        {"id_notificacao": "NOT-011", "cod_mun_6": "150140", "data_notificacao": "22/08/2026", "casos_notificados": 290, "casos_confirmados": 210, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-012", "cod_mun_6": "431490", "data_notificacao": "2026-08-23", "casos_notificados": 120, "casos_confirmados": 95, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-013", "cod_mun_6": "350950", "data_notificacao": "24/08/2026", "casos_notificados": 850, "casos_confirmados": 720, "classificacao": "Dengue com Sinais de Alarme"},
        {"id_notificacao": "NOT-014", "cod_mun_6": "354980", "data_notificacao": "2026-08-25", "casos_notificados": 430, "casos_confirmados": 380, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-015", "cod_mun_6": "354340", "data_notificacao": "26/08/2026", "casos_notificados": 790, "casos_confirmados": 680, "classificacao": "Dengue com Sinais de Alarme"},
        {"id_notificacao": "NOT-016", "cod_mun_6": "317020", "data_notificacao": "2026-08-27", "casos_notificados": 560, "casos_confirmados": 490, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-017", "cod_mun_6": "420540", "data_notificacao": "28/08/2026", "casos_notificados": 95, "casos_confirmados": 75, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-018", "cod_mun_6": "320530", "data_notificacao": "2026-08-29", "casos_notificados": 210, "casos_confirmados": 170, "classificacao": "Dengue Classica"},
        {"id_notificacao": "NOT-019", "cod_mun_6": "500270", "data_notificacao": "30/08/2026", "casos_notificados": 980, "casos_confirmados": 860, "classificacao": "Dengue com Sinais de Alarme"},
        {"id_notificacao": "NOT-020", "cod_mun_6": "510340", "data_notificacao": "31/08/2026", "casos_notificados": 1150, "casos_confirmados": 1020, "classificacao": "Dengue Grave"},
        # Anomalias propositais para Quarentena de Notificações:
        {"id_notificacao": "NOT-021", "cod_mun_6": "355030", "data_notificacao": "2026-08-15", "casos_notificados": -25, "casos_confirmados": -20, "classificacao": "Erro Quantidade Negativa"},
        {"id_notificacao": "NOT-022", "cod_mun_6": "330455", "data_notificacao": "DATA_CORROMPIDA_99", "casos_notificados": 50, "casos_confirmados": 40, "classificacao": "Data Invalida"},
        {"id_notificacao": "NOT-023", "cod_mun_6": "310620", "data_notificacao": "2026-08-20", "casos_notificados": 0, "casos_confirmados": 0, "classificacao": "Sem Notificacao"},
        {"id_notificacao": "NOT-001", "cod_mun_6": "355030", "data_notificacao": "12/08/2026", "casos_notificados": 1420, "casos_confirmados": 1150, "classificacao": "Dengue Classica"} # Duplicata
    ]
    df_dengue = pd.DataFrame(notificacoes_dengue)
    p_dengue_out = os.path.join(DIR_BRONZE, "datasus_dengue_2026-08.csv")
    df_dengue.to_csv(p_dengue_out, sep=";", index=False)
    print(f"✅ Fonte 2 gerada (DataSUS Dengue): {len(df_dengue)} registros em {p_dengue_out}")

    # 3. Fonte 3: INMET Clima e Chuva Acumulada
    chuva_dados = [
        {"cod_mun_6": "355030", "chuva_acumulada_mm": "145,8", "dias_com_chuva": 14, "estacao_monitorada": "São Paulo - Mirante de Santana"},
        {"cod_mun_6": "330455", "chuva_acumulada_mm": "180,2", "dias_com_chuva": 16, "estacao_monitorada": "Rio de Janeiro - Marambaia"},
        {"cod_mun_6": "310620", "chuva_acumulada_mm": "210,5", "dias_com_chuva": 18, "estacao_monitorada": "Belo Horizonte - Pampulha"},
        {"cod_mun_6": "530010", "chuva_acumulada_mm": "190,0", "dias_com_chuva": 15, "estacao_monitorada": "Brasília - Plano Piloto"},
        {"cod_mun_6": "292740", "chuva_acumulada_mm": "95,4", "dias_com_chuva": 10, "estacao_monitorada": "Salvador - Ondina"},
        {"cod_mun_6": "230440", "chuva_acumulada_mm": "65,0", "dias_com_chuva": 7, "estacao_monitorada": "Fortaleza - Aeroporto"},
        {"cod_mun_6": "410690", "chuva_acumulada_mm": "120,6", "dias_com_chuva": 12, "estacao_monitorada": "Curitiba - Centro"},
        {"cod_mun_6": "130260", "chuva_acumulada_mm": "280,4", "dias_com_chuva": 22, "estacao_monitorada": "Manaus - Ponta Negra"},
        {"cod_mun_6": "261160", "chuva_acumulada_mm": "110,0", "dias_com_chuva": 11, "estacao_monitorada": "Recife - Curado"},
        {"cod_mun_6": "520870", "chuva_acumulada_mm": "175,2", "dias_com_chuva": 14, "estacao_monitorada": "Goiânia - Autódromo"},
        {"cod_mun_6": "150140", "chuva_acumulada_mm": "310,8", "dias_com_chuva": 24, "estacao_monitorada": "Belém - Marco"},
        {"cod_mun_6": "431490", "chuva_acumulada_mm": "135,0", "dias_com_chuva": 13, "estacao_monitorada": "Porto Alegre - Belém Novo"},
        {"cod_mun_6": "350950", "chuva_acumulada_mm": "130,5", "dias_com_chuva": 12, "estacao_monitorada": "Campinas - IAC"},
        {"cod_mun_6": "354980", "chuva_acumulada_mm": "142,0", "dias_com_chuva": 13, "estacao_monitorada": "São José dos Campos - CTA"},
        {"cod_mun_6": "354340", "chuva_acumulada_mm": "98,4", "dias_com_chuva": 9, "estacao_monitorada": "Ribeirão Preto - Aeroporto"},
        {"cod_mun_6": "317020", "chuva_acumulada_mm": "165,0", "dias_com_chuva": 15, "estacao_monitorada": "Uberlândia - UFU"},
        {"cod_mun_6": "420540", "chuva_acumulada_mm": "155,2", "dias_com_chuva": 14, "estacao_monitorada": "Florianópolis - São José"},
        {"cod_mun_6": "320530", "chuva_acumulada_mm": "105,6", "dias_com_chuva": 11, "estacao_monitorada": "Vitória - Goiabeiras"},
        {"cod_mun_6": "500270", "chuva_acumulada_mm": "188,4", "dias_com_chuva": 16, "estacao_monitorada": "Campo Grande - Embrapa"},
        {"cod_mun_6": "510340", "chuva_acumulada_mm": "220,0", "dias_com_chuva": 19, "estacao_monitorada": "Cuiabá - CPA"},
        # Anomalias de clima:
        {"cod_mun_6": "355030", "chuva_acumulada_mm": "-50,0", "dias_com_chuva": 5, "estacao_monitorada": "Estacao Chuva Negativa"},
        {"cod_mun_6": "330455", "chuva_acumulada_mm": "VALOR_TEXTO_INVALIDO", "dias_com_chuva": 0, "estacao_monitorada": "Sensor Quebrado"}
    ]
    df_chuva = pd.DataFrame(chuva_dados)
    p_chuva_out = os.path.join(DIR_BRONZE, "inmet_chuva.csv")
    df_chuva.to_csv(p_chuva_out, sep=";", index=False)
    print(f"✅ Fonte 3 gerada (INMET Clima): {len(df_chuva)} registros em {p_chuva_out}")

    # 4. Fonte 4: CNES Capacidade Hospitalar & Leitos SUS (PostgreSQL)
    leitos_dados = [
        {"cod_mun_6": "355030", "municipio": "São Paulo", "leitos_clinicos": 18500, "leitos_uti": 3200, "postos_saude": 480},
        {"cod_mun_6": "330455", "municipio": "Rio de Janeiro", "leitos_clinicos": 11200, "leitos_uti": 1850, "postos_saude": 260},
        {"cod_mun_6": "310620", "municipio": "Belo Horizonte", "leitos_clinicos": 5400, "leitos_uti": 980, "postos_saude": 152},
        {"cod_mun_6": "530010", "municipio": "Brasília", "leitos_clinicos": 4800, "leitos_uti": 820, "postos_saude": 130},
        {"cod_mun_6": "292740", "municipio": "Salvador", "leitos_clinicos": 4100, "leitos_uti": 650, "postos_saude": 140},
        {"cod_mun_6": "230440", "municipio": "Fortaleza", "leitos_clinicos": 4300, "leitos_uti": 690, "postos_saude": 125},
        {"cod_mun_6": "410690", "municipio": "Curitiba", "leitos_clinicos": 3800, "leitos_uti": 610, "postos_saude": 110},
        {"cod_mun_6": "130260", "municipio": "Manaus", "leitos_clinicos": 2900, "leitos_uti": 480, "postos_saude": 95},
        {"cod_mun_6": "261160", "municipio": "Recife", "leitos_clinicos": 3500, "leitos_uti": 570, "postos_saude": 105},
        {"cod_mun_6": "520870", "municipio": "Goiânia", "leitos_clinicos": 3100, "leitos_uti": 510, "postos_saude": 90},
        {"cod_mun_6": "150140", "municipio": "Belém", "leitos_clinicos": 2700, "leitos_uti": 430, "postos_saude": 85},
        {"cod_mun_6": "431490", "municipio": "Porto Alegre", "leitos_clinicos": 3200, "leitos_uti": 540, "postos_saude": 98},
        {"cod_mun_6": "350950", "municipio": "Campinas", "leitos_clinicos": 2400, "leitos_uti": 390, "postos_saude": 68},
        {"cod_mun_6": "354980", "municipio": "São José dos Campos", "leitos_clinicos": 1450, "leitos_uti": 240, "postos_saude": 45},
        {"cod_mun_6": "354340", "municipio": "Ribeirão Preto", "leitos_clinicos": 1600, "leitos_uti": 280, "postos_saude": 50},
        {"cod_mun_6": "317020", "municipio": "Uberlândia", "leitos_clinicos": 1500, "leitos_uti": 260, "postos_saude": 48},
        {"cod_mun_6": "420540", "municipio": "Florianópolis", "leitos_clinicos": 1250, "leitos_uti": 210, "postos_saude": 42},
        {"cod_mun_6": "320530", "municipio": "Vitória", "leitos_clinicos": 980, "leitos_uti": 170, "postos_saude": 35},
        {"cod_mun_6": "500270", "municipio": "Campo Grande", "leitos_clinicos": 1850, "leitos_uti": 290, "postos_saude": 62},
        {"cod_mun_6": "510340", "municipio": "Cuiabá", "leitos_clinicos": 1400, "leitos_uti": 230, "postos_saude": 52}
    ]
    df_leitos = pd.DataFrame(leitos_dados)
    p_leitos_out = os.path.join(DIR_BRONZE, "cnes_leitos_hospitalares.csv")
    df_leitos.to_csv(p_leitos_out, sep=";", index=False)
    print(f"✅ Fonte 4 gerada (CNES Leitos SUS): {len(df_leitos)} registros em {p_leitos_out}")

    # 5. Fonte 5: Vigilância Sanitária & Alertas Epidemiológicos (MongoDB NoSQL)
    alertas_dados = [
        {"id_alerta": "ALT-001", "cod_mun_6": "530010", "cidade": "Brasília", "nivel_risco": "Epidemia", "acao": "Ativação de tenda de hidratação e nebulização espacial", "data": "2026-08-16"},
        {"id_alerta": "ALT-002", "cod_mun_6": "310620", "cidade": "Belo Horizonte", "nivel_risco": "Epidemia", "acao": "Abertura de centros de atendimento 24h", "data": "2026-08-17"},
        {"id_alerta": "ALT-003", "cod_mun_6": "520870", "cidade": "Goiânia", "nivel_risco": "Alto Risco", "acao": "Mutirão de limpeza e bloqueio de focos", "data": "2026-08-18"},
        {"id_alerta": "ALT-004", "cod_mun_6": "510340", "cidade": "Cuiabá", "nivel_risco": "Alto Risco", "acao": "Visitas domiciliares intensificadas", "data": "2026-08-19"},
        {"id_alerta": "ALT-005", "cod_mun_6": "500270", "cidade": "Campo Grande", "nivel_risco": "Alto Risco", "acao": "Monitoramento de larvas em reservatórios", "data": "2026-08-20"},
        {"id_alerta": "ALT-006", "cod_mun_6": "355030", "cidade": "São Paulo", "nivel_risco": "Médio Risco", "acao": "Campanha de conscientização em mídias", "data": "2026-08-21"},
        {"id_alerta": "ALT-007", "cod_mun_6": "330455", "cidade": "Rio de Janeiro", "nivel_risco": "Médio Risco", "acao": "Fiscalização de ferros-velhos e terrenos", "data": "2026-08-22"},
        {"id_alerta": "ALT-008", "cod_mun_6": "431490", "cidade": "Porto Alegre", "nivel_risco": "Baixo Risco", "acao": "Monitoramento de rotina quinzenal", "data": "2026-08-23"},
        {"id_alerta": "ALT-009", "cod_mun_6": "420540", "cidade": "Florianópolis", "nivel_risco": "Baixo Risco", "acao": "Inspeções preventivas regulares", "data": "2026-08-24"},
        # Anomalias de alertas para quarentena:
        {"id_alerta": "ALT-010", "cod_mun_6": "999999", "cidade": "Cidade Inexistente", "nivel_risco": "RISCO_DESCONHECIDO_99", "acao": "Sem acao", "data": "2026-08-25"}
    ]
    p_alertas_out = os.path.join(DIR_BRONZE, "alertas_vigilancia.json")
    with open(p_alertas_out, "w", encoding="utf-8") as f:
        json.dump(alertas_dados, f, indent=2, ensure_ascii=False)
    print(f"✅ Fonte 5 gerada (Alertas NoSQL MongoDB): {len(alertas_dados)} alertas em {p_alertas_out}")

if __name__ == "__main__":
    gerar_fontes()
