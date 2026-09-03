# ====================================================================
# MÓDULO 3: Extração com pypdf
# ====================================================================
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject

caminho_pdf = '9-ebook.pdf'

# ─── 3.1 Metadados e Inspeção ───────────────────────────────────
print("--- 3.1 Metadados e Inspeção ---")
try:
    reader = PdfReader(caminho_pdf)

    # Lendo metadados
    meta = reader.metadata
    if meta:
        print(f"Título: {meta.title}")
        print(f"Autor: {meta.author}")
        print(f"Criado em: {meta.creation_date}")
        print(f"Produtor: {meta.producer}")

    # Lendo a estrutura do documento
    print(f"Total de páginas: {len(reader.pages)}")

    # Verificar se o PDF tem senha
    if reader.is_encrypted:
        print("PDF protegido por senha")
        # reader.decrypt('senha_aqui') # decriptografar se necessário

    # Tamanho (dimensões) da primeira página
    if len(reader.pages) > 0:
        pagina = reader.pages[0]
        print(f"Largura da pág 1: {pagina.mediabox.width:.1f} pt")
        print(f"Altura da pág 1: {pagina.mediabox.height:.1f} pt")

except FileNotFoundError:
    print(f"Arquivo '{caminho_pdf}' não encontrado. Certifique-se de ter um PDF para testar.")


# ─── 3.2 Extração de Texto por Página ───────────────────────────
print("\n--- 3.2 Extração de Texto por Página ---")
try:
    reader = PdfReader(caminho_pdf)
    
    # Extrair texto de uma página (ex: página 1)
    if len(reader.pages) > 0:
        texto_p1 = reader.pages[0].extract_text()
        print("Prévia da página 1:")
        print(texto_p1[:200], "...\n")
    
    # Extrair de todas as páginas
    paginas = []
    for i, pagina in enumerate(reader.pages):
        texto = pagina.extract_text() or '' # retorna None se for string vazia
        paginas.append({'pagina': i + 1, 'texto': texto})
        
    print(f"{len(paginas)} páginas extraídas")
    print(f"Total de caracteres: {sum(len(p['texto']) for p in paginas)}")
    
    # Orientação da extração — útil para PDFs com colunas
    # Modos: 'plain', 'layout'
    if len(reader.pages) > 0:
        texto_layout = reader.pages[0].extract_text(extraction_mode='layout')
        
except FileNotFoundError:
    print(f"Arquivo '{caminho_pdf}' não encontrado.")


# ─── 3.3 Manipulação de Páginas ─────────────────────────────────
print("\n--- 3.3 Manipulação de Páginas ---")
try:
    # 1. Mesclar dois PDFs
    writer = PdfWriter()
    # Usando o mesmo arquivo duas vezes apenas como exemplo de mesclagem (parte 1 e parte 2)
    for caminho in [caminho_pdf, caminho_pdf]: 
        reader = PdfReader(caminho)
        for pagina in reader.pages:
            writer.add_page(pagina)
            
    with open('merged.pdf', 'wb') as f:
        writer.write(f)
    print(f"PDFs mesclados e salvos em 'merged.pdf' (total de páginas geradas: {len(writer.pages)})")
    
    # 2. Extrair páginas específicas (ex: páginas 1 a 5)
    writer_split = PdfWriter()
    reader = PdfReader(caminho_pdf)
    # índice 0 = página 1 (então 0:5 representa as páginas 1 a 5)
    for pagina in reader.pages[0:5]: 
        writer_split.add_page(pagina)
        
    with open('paginas_1_a_5.pdf', 'wb') as f:
        writer_split.write(f)
    print(f"Extraídas {len(writer_split.pages)} páginas parciais em 'paginas_1_a_5.pdf'")
    
except FileNotFoundError:
    print(f"Arquivo '{caminho_pdf}' não encontrado para teste de manipulação.")
