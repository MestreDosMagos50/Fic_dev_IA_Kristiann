# 5. Expressões Regulares com o Módulo re
import re

# 5.2 Funções do Módulo re

texto = "Contato: maria@email.com | CPF: 123.456.789-09 | Tel: (11) 9 8765-4321"

# ── re.search() — primeira ocorrência em qualquer posição ─
# Retorna um Match object ou None
m = re.search(r"\d{3}\.\d{3}\.\d{3}-\d{2}", texto)
if m:
    print("CPF:", m.group()) # 123.456.789-09
    print("Início:", m.start()) # posição no texto

# ── re.match() — verifica APENAS o início da string ───────
m = re.match(r"Contato", texto)
print(bool(m)) # True — texto começa com 'Contato'

# ── re.findall() — retorna lista com TODAS as ocorrências ─
numeros = re.findall(r"\d+", texto)
print(numeros) # ['123', '456', '789', '09', '11', '9', '8765', '4321']

# ── re.finditer() — iterador de Match objects ─────────────
# Mais eficiente que findall() quando há muitas ocorrências
for m in re.finditer(r"\d+", texto):
    print(f"'{m.group()}' na posição {m.start()}")

# ── re.sub() — substitui TODAS as ocorrências ─────────────
anonimizado = re.sub(r"\d{3}\.\d{3}\.\d{3}-\d{2}", 
                     "***.***.***-**", texto)
print(anonimizado)

# ── re.compile() — compila o padrão para reutilização ─────
# Muito mais eficiente quando o mesmo padrão é usado em loop
PADRAO_CPF = re.compile(r"\d{3}\.\d{3}\.\d{3}-\d{2}")
print(PADRAO_CPF.findall(texto)) # mesmo resultado, mais rápido

# 5.3 Raw Strings e Flags

# REGRA: sempre use raw strings r'...' em padrões regex.
# Python interpreta \ antes de passá-lo ao motor de regex:
# sem raw string: '\d' pode ser mal interpretado pelo Python
# com raw string: r'\d' preserva os dois caracteres: barra + d

# CORRETO — sempre:
re.search(r"\d+", "abc123")

# ── Flags modificam o comportamento do motor ───────────────

# re.IGNORECASE (re.I): ignora maiúsculas/minúsculas
m = re.search(r"python", "Aprenda PYTHON!", re.IGNORECASE)
print(m.group()) # PYTHON

# re.MULTILINE (re.M): ^ e $ funcionam por linha, não por string
multi = "linha1\nlinha2\nlinha3"
print(re.findall(r"^linha\d", multi, re.MULTILINE))
# ['linha1', 'linha2', 'linha3']

# re.DOTALL (re.S): o ponto . captura também \n
m = re.search(r"início.*fim", "início\nmeio\nfim", re.DOTALL)
print(m.group())

# Combinar múltiplas flags com |
# re.findall(r"padrão", texto, re.IGNORECASE | re.MULTILINE)

# 5.4 Grupos de Captura

# ── Grupos posicionais — acessados por número ─────────────
texto_data = "Cadastro em: 21/03/2026"
m = re.search(r"(\d{2})/(\d{2})/(\d{4})", texto_data)
if m:
    print(m.group(0)) # 21/03/2026 (match completo — grupo 0)
    print(m.group(1)) # 21 (grupo 1 — dia)
    print(m.group(2)) # 03 (grupo 2 — mês)
    print(m.group(3)) # 2026 (grupo 3 — ano)
    dia, mes, ano = m.groups() # desempacotar todos os grupos
    print(f"{ano}-{mes}-{dia}") # converter para formato ISO

# ── Grupos nomeados — (?P<nome>padrão) ────────────────────
# Mais legível em padrões com muitos grupos
m = re.search(
    r"(?P<dia>\d{2})/(?P<mes>\d{2})/(?P<ano>\d{4})", 
    texto_data
)
if m:
    print(m.group("dia")) # 21
    print(m.groupdict()) # {'dia': '21', 'mes': '03', 'ano': '2026'}

# ── findall() com grupos retorna lista de tuplas ───────────
texto2 = "Ana: 15/03/1990 | Bruno: 22/07/1985"
datas = re.findall(r"(\d{2})/(\d{2})/(\d{4})", texto2)
print(datas) # [('15', '03', '1990'), ('22', '07', '1985')]
for dia, mes, ano in datas:
    print(f"Ano: {ano}, Mês: {mes}, Dia: {dia}")


# 5.5 Padrões para CPF, Telefone e E-mail

# ── CPF ──────────────────────────────────────────────────
PADRAO_CPF_COMPLETO = re.compile(
    r"\b(\d{3})[.\s]?(\d{3})[.\s]?(\d{3})[-\s]?(\d{2})\b"
)

# ── TELEFONE ─────────────────────────────────────────────
PADRAO_TEL = re.compile(
    r"\(?\d{2}\)?[\s.-]?9?[\s.-]?\d{4}[\s.-]?\d{4}"
)

# ── E-MAIL ───────────────────────────────────────────────
PADRAO_EMAIL = re.compile(
    r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}",
    re.IGNORECASE
)

# ── Testando os três padrões ─────────────────────────────
texto_teste = """
CPF: 123.456.789-09 | Cel: (11) 9 8765-4321
Outro CPF: 98765432100 | Email: ana@empresa.com.br
"""

for m in PADRAO_CPF_COMPLETO.finditer(texto_teste):
    d1, d2, d3, d4 = m.groups()
    print("CPF:", f"{d1}.{d2}.{d3}-{d4}") # normalizado

print("Tels:", PADRAO_TEL.findall(texto_teste))
print("Emails:", PADRAO_EMAIL.findall(texto_teste))


# 5.6 Limpeza de Texto com re.sub()

# Remover tags HTML
html = "<b>Produto</b>: <span class='preco'>R$ 29,90</span>"
limpo = re.sub(r"<[^>]+>", "", html)
print(limpo) # Produto: R$ 29,90

# Normalizar espaços múltiplos em um único espaço
texto_espaco = "texto    com     espaços   extras"
normal = re.sub(r"\s+", " ", texto_espaco).strip()
print(normal) # texto com espaços extras

# Remover pontuação — manter letras, dígitos e espaços
suja = "Nome: Ana-Paula (contato#1) --- 2026!"
limpa = re.sub(r"[^\w\s]", "", suja)
print(limpa) # Nome AnaPaula contato1 2026

# Extrair apenas os dígitos de um CPF formatado
cpf_fmt = "123.456.789-09"
cpf_digits = re.sub(r"[^\d]", "", cpf_fmt)
print(cpf_digits) # 12345678909

# Anonimizar dados sensíveis antes de logar
def anonimizar(texto: str) -> str:
    """Substitui CPFs, telefones e e-mails por marcadores genéricos."""
    texto = PADRAO_CPF_COMPLETO.sub("[CPF]", texto)
    texto = PADRAO_TEL.sub("[TEL]", texto)
    texto = PADRAO_EMAIL.sub("[EMAIL]", texto)
    return texto

log_bruto = "Usuário Ana (ana@email.com, CPF 123.456.789-09) logou."
print(anonimizar(log_bruto))
# Usuário Ana ([EMAIL], [CPF]) logou.
