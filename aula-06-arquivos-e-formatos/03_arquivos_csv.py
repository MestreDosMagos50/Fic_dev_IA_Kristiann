# 3. Arquivos CSV com o Módulo csv
import csv
from pathlib import Path

Path("saida_03").mkdir(exist_ok=True)

# Arquivo de exemplo — clientes.csv:
clientes_csv_path = Path("saida_03/clientes.csv")
clientes_csv_path.write_text("""nome,email,telefone,cidade
Ana Silva,ana@email.com,(11) 9 8765-4321,São Paulo
Bruno Costa,bruno@email.com,(21) 9 1234-5678,Rio de Janeiro""", encoding="utf-8")

# 3.1 Lendo CSV

# ── csv.reader: acessa campos por índice numérico ─────────
with open(clientes_csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f) # cada linha vira uma lista
    cabecalho = next(reader) # lê e avança além do cabeçalho
    print("Colunas:", cabecalho) # ['nome', 'email', 'telefone', 'cidade']
    
    for linha in reader:
        nome, email, tel, cidade = linha
        print(f"{nome} — {cidade}")

# ── csv.DictReader: acessa campos pelo nome da coluna ─────
# Preferível ao reader quando o CSV tem cabeçalho definido
with open(clientes_csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f) # cada linha vira um dict
    for linha in reader:
        print(linha["nome"], "—", linha["cidade"])
        # {'nome': 'Ana Silva', 'email': '...', ...}

# ── CSV com ponto-e-vírgula (exportação brasileira do Excel) ─
# Criando arquivo de vendas.csv de teste
Path("saida_03/vendas.csv").write_text("produto;preco\nMouse;50\nTeclado;100", encoding="utf-8")

with open("saida_03/vendas.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    for linha in reader:
        print(linha)

# 3.2 Escrevendo CSV

clientes = [
    {"nome": "Ana Silva", "email": "ana@email.com", "cidade": "São Paulo"},
    {"nome": "Bruno Costa", "email": "bruno@email.com", "cidade": "Recife"},
    {"nome": "Carla Mendes", "email": "carla@email.com", "cidade": "Curitiba"},
]

# ── csv.DictWriter: escrita por nome de campo (preferível) ─
campos = ["nome", "email", "cidade"]
saida = Path("saida_03/clientes_saida.csv")

with open(saida, "w", encoding="utf-8", newline="") as f:
    # newline="" é obrigatório: sem ele o Windows insere uma linha em
    # branco entre cada registro (o csv.writer já adiciona \r\n internamente)
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader() # linha de cabeçalho
    writer.writerows(clientes) # todos os registros de uma vez

print(f"Salvo em: {saida.resolve()}")

# ── csv.writer: escrita por listas ────────────────────────
with open("saida_03/notas.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["aluno", "nota", "status"]) # cabeçalho
    writer.writerows([
        ["Alice", 9.5, "Aprovada"],
        ["Bruno", 5.0, "Recuperação"],
    ])

# ── extrasaction='ignore': ignora chaves extras do dict ────
# Útil quando o dict tem mais campos do que as colunas definidas
with open("saida_03/simplificado.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["nome", "cidade"],
                            extrasaction="ignore")
    writer.writeheader()
    writer.writerows(clientes) # 'email' é ignorado silenciosamente
