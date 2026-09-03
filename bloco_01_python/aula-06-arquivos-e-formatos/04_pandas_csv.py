# 4. Pandas como Ponte para CSV
import pandas as pd
import os

os.makedirs("saida_04", exist_ok=True)

# Instalação (se necessário): pip install pandas

# Criando um arquivo mockado para testar
with open("saida_04/clientes.csv", "w", encoding="utf-8") as f:
    f.write("nome,email,telefone,cidade\n")
    f.write("Ana Silva,ana@email.com,11987654321,São Paulo\n")
    f.write("Bruno Costa,bruno@email.com,21912345678,Recife\n")

# 4.1 Lendo e Filtrando CSV com pandas

# read_csv() lê o arquivo e retorna um DataFrame — uma tabela em memória
df = pd.read_csv("saida_04/clientes.csv", encoding="utf-8")

# Inspeção rápida
print(df.shape)       # (100, 4) — 100 linhas, 4 colunas (exemplo)
print(df.head(3))     # primeiras 3 linhas
print(df.dtypes)      # tipo inferido de cada coluna
print(df.info())      # resumo: nulos, tipos, uso de memória

# Acessar uma coluna — retorna uma Series (lista com rótulo)
print(df["nome"])

# Filtrar linhas com condição booleana
sp = df[df["cidade"] == "São Paulo"]
print(f"{len(sp)} clientes em São Paulo")

# Múltiplas condições: & = and, | = or — parênteses obrigatórios
filtro = df[(df["cidade"] == "São Paulo") & 
            (df["nome"].str.startswith("A"))]

# CSV com ponto-e-vírgula e vírgula como decimal (padrão Brasil)
# Criando arquivo para exemplo
with open("saida_04/vendas_br.csv", "w", encoding="utf-8") as f:
    f.write("produto;preco\nTeclado;120,50\n")

df_br = pd.read_csv("saida_04/vendas_br.csv", sep=";", decimal=",", encoding="utf-8")
print(df_br)

# 4.2 Salvando CSV e JSON com pandas

df = pd.read_csv("saida_04/clientes.csv", encoding="utf-8")

# Adicionar coluna derivada
df["dominio"] = df["email"].str.split("@").str[1]

# Remover linhas com valores ausentes em colunas específicas
df = df.dropna(subset=["email"])

# Salvar CSV — index=False evita gravar a coluna de índice interno
df.to_csv("saida_04/clientes_limpos.csv", index=False, encoding="utf-8")

# Salvar JSON — orient='records' produz lista de dicts,
# o mesmo formato que você já usa com json.dump() desde a Aula 03
df.to_json("saida_04/clientes.json", orient="records",
           force_ascii=False, indent=2)

# Contar ocorrências de cada valor em uma coluna
print(df["cidade"].value_counts())
