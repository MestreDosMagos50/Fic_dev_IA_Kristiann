#!/usr/bin/env python3
"""
scripts/gerar_fontes_temperatura_concorrentes.py
Gera 2 fontes concorrentes de temperatura para os 20 municípios:
- inmet_temperatura.csv (Fonte Primária: Estação Terrestre Física)
- cptec_temperatura.csv (Fonte Secundária: Sensoriamento Remoto por Satélite)
"""

import os
import csv

DIR_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_BRONZE = os.path.join(DIR_PROJETO, "dados", "bronze")
os.makedirs(DIR_BRONZE, exist_ok=True)

# 20 Cidades base
CIDADES = [
    ("130260", "Manaus", "AM", "Norte"),
    ("150140", "Belém", "PA", "Norte"),
    ("230440", "Fortaleza", "CE", "Nordeste"),
    ("261160", "Recife", "PE", "Nordeste"),
    ("292740", "Salvador", "BA", "Nordeste"),
    ("310620", "Belo Horizonte", "MG", "Sudeste"),
    ("317020", "Uberlândia", "MG", "Sudeste"),
    ("320530", "Vitória", "ES", "Sudeste"),
    ("330455", "Rio De Janeiro", "RJ", "Sudeste"),
    ("350950", "Campinas", "SP", "Sudeste"),
    ("354340", "Ribeirão Preto", "SP", "Sudeste"),
    ("354980", "São José Dos Campos", "SP", "Sudeste"),
    ("355030", "São Paulo", "SP", "Sudeste"),
    ("410690", "Curitiba", "PR", "Sul"),
    ("420540", "Florianópolis", "SC", "Sul"),
    ("431490", "Porto Alegre", "RS", "Sul"),
    ("500270", "Campo Grande", "MS", "Centro-Oeste"),
    ("510340", "Cuiabá", "MT", "Centro-Oeste"),
    ("520870", "Goiânia", "GO", "Centro-Oeste"),
    ("530010", "Brasília", "DF", "Centro-Oeste")
]

# Leituras INMET (Fonte Terrestre Física) com casos de teste propositais
INMET_DATA = {
    "130260": ("", "OFFLINE", "SENSOR_OFFLINE"),          # Manaus: Nulo (Sensor Offline) -> Fallback CPTEC
    "150140": ("31.2", "82", "OPERACIONAL"),             # Belém: Válido -> Elege INMET
    "230440": ("29.8", "74", "OPERACIONAL"),             # Fortaleza: Válido -> Elege INMET
    "261160": ("28.5", "78", "OPERACIONAL"),             # Recife: Válido -> Elege INMET
    "292740": ("99.9", "45", "ANOMALIA_CIRCUITO"),       # Salvador: 99.9°C (Anomalia extrema) -> Quarentena + Fallback CPTEC
    "310620": ("24.3", "65", "OPERACIONAL"),             # Belo Horizonte: Válido -> Elege INMET
    "317020": ("26.1", "58", "OPERACIONAL"),             # Uberlândia: Válido -> Elege INMET
    "320530": ("27.0", "72", "OPERACIONAL"),             # Vitória: Válido -> Elege INMET
    "330455": ("28.2", "70", "OPERACIONAL"),             # Rio de Janeiro: Válido -> Elege INMET
    "350950": ("-85.0", "99", "FALHA_CALIBRACAO"),       # Campinas: -85.0°C (Inverossímil) -> Quarentena + Fallback CPTEC
    "354340": ("29.4", "50", "OPERACIONAL"),             # Ribeirão Preto: Válido -> Elege INMET
    "354980": ("23.1", "68", "OPERACIONAL"),             # São José dos Campos: Válido -> Elege INMET
    "355030": ("22.8", "75", "OPERACIONAL"),             # São Paulo: Válido -> Elege INMET
    "410690": ("17.5", "80", "OPERACIONAL"),             # Curitiba: Válido -> Elege INMET
    "420540": ("21.0", "79", "OPERACIONAL"),             # Florianópolis: Válido -> Elege INMET
    "431490": ("", "OFFLINE", "ESTACAO_SEM_COMUNICACAO"), # Porto Alegre: Vazio -> Fallback CPTEC
    "500270": ("27.8", "55", "OPERACIONAL"),             # Campo Grande: Válido -> Elege INMET
    "510340": ("35.2", "42", "OPERACIONAL"),             # Cuiabá: Válido -> Elege INMET
    "520870": ("30.1", "48", "OPERACIONAL"),             # Goiânia: Válido -> Elege INMET
    "530010": ("25.6", "52", "OPERACIONAL")              # Brasília: Válido -> Elege INMET
}

# Leituras CPTEC/INPE (Satélite de Contingência - Cobertura 100% íntegra)
CPTEC_DATA = {
    "130260": ("31.5", "84", "0.96"),  # Manaus: Salva por satélite
    "150140": ("30.8", "80", "0.94"),
    "230440": ("29.2", "72", "0.95"),
    "261160": ("28.1", "76", "0.93"),
    "292740": ("28.0", "71", "0.97"),  # Salvador: Salva por satélite
    "310620": ("23.9", "67", "0.92"),
    "317020": ("25.8", "60", "0.91"),
    "320530": ("26.5", "74", "0.90"),
    "330455": ("27.8", "73", "0.95"),
    "350950": ("22.4", "66", "0.93"),  # Campinas: Salva por satélite
    "354340": ("28.9", "53", "0.92"),
    "354980": ("22.7", "70", "0.94"),
    "355030": ("22.1", "77", "0.96"),
    "410690": ("17.1", "82", "0.89"),
    "420540": ("20.8", "81", "0.91"),
    "431490": ("19.2", "78", "0.93"),  # Porto Alegre: Salva por satélite
    "500270": ("27.2", "57", "0.95"),
    "510340": ("34.8", "45", "0.98"),
    "520870": ("29.7", "50", "0.94"),
    "530010": ("25.1", "55", "0.95")
}

def main():
    path_inmet = os.path.join(DIR_BRONZE, "inmet_temperatura.csv")
    path_cptec = os.path.join(DIR_BRONZE, "cptec_temperatura.csv")

    with open(path_inmet, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["cod_mun_6", "municipio", "temperatura_c", "umidade_relativa", "status_sensor", "data_leitura"])
        for cod, mun, uf, reg in CIDADES:
            temp, umid, st = INMET_DATA[cod]
            w.writerow([cod, mun, temp, umid, st, "2026-08-31 14:00:00"])

    with open(path_cptec, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["cod_mun_6", "municipio", "temperatura_satelite_c", "umidade_satelite", "indice_cobertura", "data_leitura"])
        for cod, mun, uf, reg in CIDADES:
            temp, umid, cob = CPTEC_DATA[cod]
            w.writerow([cod, mun, temp, umid, cob, "2026-08-31 14:00:00"])

    print(f"✅ Fonte 3A (INMET Terrestre) gerada: {path_inmet} ({len(CIDADES)} registros)")
    print(f"✅ Fonte 3B (CPTEC Satélite) gerada: {path_cptec} ({len(CIDADES)} registros)")

if __name__ == "__main__":
    main()
