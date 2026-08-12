"""
Extrator de Dados com Regex
Pipeline: TXT → Extração (CPF/Telefone/Email) → CSV + JSON

Trilha Python para IA - Aula 06
Autor: Pedro Clarindo da Silva Neto
Data: 2026-08-11
"""

import re
import csv
import json
from pathlib import Path

# ============================================================
# CONFIGURAÇÃO DE CAMINHOS
# ============================================================
RAIZ = Path(__file__).parent
ENTRADA = RAIZ / "contatos.txt"
SAIDA = RAIZ / "saida"

# ============================================================
# PADRÕES REGEX
# ============================================================

# CPF: 123.456.789-09 ou 12345678909
PADRAO_CPF = re.compile(
    r'\b(\d{3})[.\s]?(\d{3})[.\s]?(\d{3})[-\s]?(\d{2})\b'
)

# Telefone: (11) 9 8765-4321, (21)98765-1234, 11912345678
PADRAO_TEL = re.compile(
    r'\(?\d{2}\)?[\s.-]?9?[\s.-]?\d{4}[\s.-]?\d{4}'
)

# Email: ana@email.com, ana.paula@empresa.com.br
PADRAO_EMAIL = re.compile(
    r'[\w.+_-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}',
    re.IGNORECASE
)

# ============================================================
# FUNÇÕES DE ARQUIVO
# ============================================================

def ler_arquivo(caminho: Path) -> str:
    """Lê o conteúdo de um arquivo de texto."""
    print(f"\n📖 Lendo arquivo: {caminho.name}")
    
    try:
        conteudo = caminho.read_text(encoding='utf-8')
        print(f"✅ {len(conteudo)} caracteres lidos")
        return conteudo
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho}")
        raise
    except UnicodeDecodeError:
        print(f"❌ Erro de encoding. Tentando com 'latin-1'...")
        return caminho.read_text(encoding='latin-1')

def salvar_csv(registros: list, caminho: Path) -> None:
    """Salva registros em arquivo CSV."""
    if not registros:
        print("⚠ Nenhum registro para salvar em CSV")
        return
        
    caminho.parent.mkdir(parents=True, exist_ok=True)
    campos = ['cpf', 'telefone', 'email']
    
    with open(caminho, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(registros)
        
    print(f"✅ CSV salvo: {caminho} ({len(registros)} registros)")

def salvar_json(dados: dict, caminho: Path) -> None:
    """Salva dados em arquivo JSON."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        
    print(f"✅ JSON salvo: {caminho}")

def salvar_metadados(dados: dict, caminho: Path) -> None:
    """Salva um resumo dos dados em formato texto."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("RELATÓRIO DE EXTRAÇÃO\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Data da extração:\n{__import__('datetime').datetime.now()}\n\n")
        
        f.write(f"Total de CPFs: {dados['total_cpfs']}\n")
        f.write(f"Total de Telefones: {dados['total_telefones']}\n")
        f.write(f"Total de E-mails: {dados['total_emails']}\n\n")
        
        f.write("CPFs encontrados:\n")
        for cpf in dados['cpfs']:
            f.write(f" • {cpf}\n")
            
        f.write("\nTelefones encontrados:\n")
        for tel in dados['telefones']:
            f.write(f" • {tel}\n")
            
        f.write("\nE-mails encontrados:\n")
        for email in dados['emails']:
            f.write(f" • {email}\n")
            
    print(f"✅ Metadados salvos: {caminho}")

# ============================================================
# FUNÇÕES DE EXTRAÇÃO
# ============================================================

def extrair_cpfs(texto: str) -> list:
    """Extrai CPFs e normaliza para o formato NNN.NNN.NNN-NN."""
    cpfs = []
    
    for match in PADRAO_CPF.finditer(texto):
        d1, d2, d3, d4 = match.groups()
        cpf = f"{d1}.{d2}.{d3}-{d4}"
        
        if cpf not in cpfs:
            cpfs.append(cpf)
            
    return cpfs

def extrair_telefones(texto: str) -> list:
    """Extrai telefones únicos do texto."""
    telefones = []
    
    for match in PADRAO_TEL.finditer(texto):
        tel = match.group().strip()
        
        if tel not in telefones:
            telefones.append(tel)
            
    return telefones

def extrair_emails(texto: str) -> list:
    """Extrai e-mails únicos em letras minúsculas."""
    emails = []
    
    for match in PADRAO_EMAIL.finditer(texto):
        email = match.group().lower()
        
        if email not in emails:
            emails.append(email)
            
    return emails

def processar_texto(texto: str) -> dict:
    """Processa o texto extraindo todos os dados estruturados."""
    print("\n⚙ Processando texto...")
    
    # Extrair dados
    cpfs = extrair_cpfs(texto)
    telefones = extrair_telefones(texto)
    emails = extrair_emails(texto)
    
    # Criar registros agrupados por bloco
    registros = []
    blocos = re.split(r'\n\d+\.\s+', texto)
    
    for bloco in blocos[1:]:
        registro = {'cpf': None, 'telefone': None, 'email': None}
        
        cpfs_bloco = extrair_cpfs(bloco)
        if cpfs_bloco:
            registro['cpf'] = cpfs_bloco[0]
            
        tels_bloco = extrair_telefones(bloco)
        if tels_bloco:
            registro['telefone'] = tels_bloco[0]
            
        emails_bloco = extrair_emails(bloco)
        if emails_bloco:
            registro['email'] = emails_bloco[0]
            
        if any([registro['cpf'], registro['telefone'], registro['email']]):
            registros.append(registro)
            
    return {
        'total_cpfs': len(cpfs),
        'total_telefones': len(telefones),
        'total_emails': len(emails),
        'cpfs': cpfs,
        'telefones': telefones,
        'emails': emails,
        'registros': registros
    }

def exibir_resumo(dados: dict) -> None:
    """Exibe um resumo formatado dos dados extraídos."""
    print("\n" + "=" * 60)
    print(" RELATÓRIO DE EXTRAÇÃO - REGEX PIPELINE")
    print("=" * 60)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f" • CPFs encontrados: {dados['total_cpfs']}")
    print(f" • Telefones encontrados: {dados['total_telefones']}")
    print(f" • E-mails encontrados: {dados['total_emails']}")
    
    print(f"\n📁 CPFs ({dados['total_cpfs']}):")
    for cpf in dados['cpfs']:
        print(f" • {cpf}")
        
    print(f"\n📞 Telefones ({dados['total_telefones']}):")
    for tel in dados['telefones']:
        print(f" • {tel}")
        
    print(f"\n✉ E-mails ({dados['total_emails']}):")
    for email in dados['emails']:
        print(f" • {email}")
        
    print(f"\n👥 Registros agrupados ({len(dados['registros'])}):")
    for i, reg in enumerate(dados['registros'], 1):
        print(f"\n {i}. CPF: {reg['cpf'] or 'N/A'}")
        print(f"    Telefone: {reg['telefone'] or 'N/A'}")
        print(f"    Email: {reg['email'] or 'N/A'}")
        
    print("\n" + "=" * 60)

# ============================================================
# DESAFIOS EXTRAS (OPCIONAIS)
# ============================================================

def validar_cpf(cpf: str) -> bool:
    """Valida matematicamente um CPF."""
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
        
    # Calcular primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    if digito1 >= 10:
        digito1 = 0
        
    # Calcular segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    if digito2 >= 10:
        digito2 = 0
        
    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])

def normalizar_telefone(telefone: str) -> str:
    """Normaliza um telefone para o formato padrão."""
    digitos = re.sub(r'[^0-9]', '', telefone)
    
    if len(digitos) == 10:
        return f"({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}"
    elif len(digitos) == 11:
        return f"({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}"
    else:
        return telefone

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():
    """Função principal do pipeline."""
    print("\n🚀 INICIANDO PIPELINE DE EXTRAÇÃO DE DADOS")
    print("=" * 60)
    
    # 1. Ler arquivo
    try:
        texto = ler_arquivo(ENTRADA)
    except FileNotFoundError:
        print("❌ Pipeline interrompido: arquivo não encontrado")
        return
        
    # 2. Processar e extrair dados
    dados = processar_texto(texto)
    
    # 3. Exibir resumo
    exibir_resumo(dados)
    
    # 4. Salvar resultados
    print("\n💾 SALVANDO RESULTADOS...")
    salvar_csv(dados['registros'], SAIDA / "contatos.csv")
    salvar_json(dados, SAIDA / "contatos_completo.json")
    salvar_metadados(dados, SAIDA / "relatorio.txt")
    
    print("\n✅ Pipeline concluído com sucesso!")

if __name__ == "__main__":
    main()
