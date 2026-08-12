# 2. Caminhos Portáveis com pathlib
from pathlib import Path

Path("saida_02").mkdir(exist_ok=True)

# 2.1 Criando e Navegando com Path

# Criando Paths — sem se preocupar com / ou \
pasta = Path("dados")
arquivo = Path("dados/clientes.csv")

# O operador / constrói caminhos de forma portável
# Funciona identicamente no Windows, Linux e Mac
base = Path("projeto")
entrada = base / "dados" / "contatos.txt" # projeto/dados/contatos.txt
saida = base / "saida" / "resultado.csv"  # projeto/saida/resultado.csv

# Propriedades do caminho — sem string manipulation manual
arq = Path("/home/usuario/projeto/dados/clientes.csv")
print(arq.name)   # clientes.csv      (nome com extensão)
print(arq.stem)   # clientes          (nome sem extensão)
print(arq.suffix) # .csv              (extensão)
print(arq.parent) # /home/usuario/projeto/dados
# print(arq.resolve()) # caminho absoluto normalizado

# Verificações de existência
print(arq.exists())   # True se existir no disco
print(arq.is_file())  # True se for um arquivo
print(arq.is_dir())   # True se for um diretório

# Caminho relativo ao script atual — fundamental para portabilidade
# __file__ é uma variável especial com o caminho do script em execução
RAIZ = Path(__file__).parent # pasta do script
ENTRADA = RAIZ / "dados" / "contatos.txt" # sempre relativo ao script

# 2.2 Criando Pastas e Listando Arquivos

# Criar toda uma hierarquia de diretórios de uma vez
Path("projeto/saida/relatorios").mkdir(parents=True, exist_ok=True)
# parents=True — cria todos os diretórios intermediários necessários
# exist_ok=True — não levanta erro se o diretório já existir

# Listar arquivos de uma pasta com glob() — padrão tipo shell
pasta = Path("projeto")
for csv_file in pasta.glob("*.csv"): # apenas arquivos .csv
    print(csv_file.name)

for txt in pasta.rglob("*.txt"): # .txt em subpastas também
    print(txt.relative_to(pasta)) # caminho relativo à pasta base

# Atalhos para arquivos pequenos: read_text / write_text
# Abrem, operam e fecham em uma única chamada
arq_nota = Path("saida_02/nota.txt")
arq_nota.write_text("Processamento concluído.", encoding="utf-8")
conteudo = arq_nota.read_text(encoding="utf-8")

# Verificar tamanho do arquivo antes de carregá-lo
tamanho = arq_nota.stat().st_size # tamanho em bytes
print(f"{arq_nota.name}: {tamanho / 1024:.1f} KB")
