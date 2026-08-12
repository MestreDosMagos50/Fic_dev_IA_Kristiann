# 1. Leitura e Escrita de Arquivos de Texto
import os
os.makedirs("saida_01", exist_ok=True)

# 1.2 Lendo Arquivos
# Criando um arquivo de teste para leitura
with open("saida_01/relatorio.txt", "w", encoding="utf-8") as f:
    f.write("linha1\nlinha2\nlinha3\n")

# Método 1: read() — carrega o arquivo inteiro como uma string
# Adequado para arquivos pequenos (até alguns MB)
with open("saida_01/relatorio.txt", "r", encoding="utf-8") as arq:
    conteudo = arq.read() # string com todo o conteúdo
    print("--- Método 1 ---")
    print(conteudo)

# Método 2: readlines() — retorna lista de linhas, cada uma com \n
with open("saida_01/relatorio.txt", "r", encoding="utf-8") as arq:
    linhas = arq.readlines() # ['linha1\n', 'linha2\n', ...]
    print("--- Método 2 ---")
    for linha in linhas:
        print(linha.strip()) # .strip() remove o \n e espaços laterais

# Método 3: iteração direta — processa uma linha por vez
# Nunca carrega o arquivo inteiro na memória; ideal para arquivos grandes
with open("saida_01/relatorio.txt", "r", encoding="utf-8") as arq:
    print("--- Método 3 ---")
    for linha in arq:
        linha = linha.strip()
        if linha: # ignora linhas vazias
            print(linha)

# Método 4: readline() — lê uma única linha a cada chamada
with open("saida_01/relatorio.txt", "r", encoding="utf-8") as arq:
    print("--- Método 4 ---")
    cabecalho = arq.readline().strip() # apenas a primeira linha
    print("Cabeçalho:", cabecalho)

# 1.3 Escrevendo Arquivos

# Escrita simples — mode='w' apaga o conteúdo existente
registros = ["Ana Silva, 30, São Paulo",
             "Bruno Costa, 25, Recife",
             "Carla Mendes, 28, Curitiba"]

with open("saida_01/saida.txt", "w", encoding="utf-8") as arq:
    for linha in registros:
        arq.write(linha + "\n") # write() NÃO adiciona \n automaticamente

# writelines() — alternativa que aceita qualquer iterável de strings
with open("saida_01/saida.txt", "w", encoding="utf-8") as arq:
    arq.writelines(r + "\n" for r in registros)

# Append — acrescenta sem apagar o que já existe; útil para logs
with open("saida_01/eventos.log", "a", encoding="utf-8") as arq:
    arq.write("[2026-03-21 10:42] Arquivo processado: dados.csv\n")

# print() pode escrever diretamente em arquivo aberto
with open("saida_01/relatorio.txt", "w", encoding="utf-8") as arq:
    print("=" * 40, file=arq)
    print("Relatório de Processamento", file=arq)
    print(f"Total de registros: {len(registros)}", file=arq)

# Criação exclusiva — falha se o arquivo já existir
# Evita sobrescrever acidentalmente um arquivo importante
try:
    with open("saida_01/resultado_final.txt", "x", encoding="utf-8") as arq:
        arq.write("Gerado em 21/03/2026.")
except FileExistsError: # exceção da Aula 05
    print("Arquivo já existe — não foi sobrescrito.")
