# ====================================================================
# MÓDULO 4: Extração com pdfplumber
# ====================================================================
import pdfplumber
import pandas as pd

# Usando o arquivo que você definiu para os testes!
caminho_pdf = '9-ebook.pdf'

# ─── 4.1 Extração de Texto com Contexto ───────────────────────────
print("\n--- 4.1 Extração de Texto com Contexto ---")
try:
    with pdfplumber.open(caminho_pdf) as pdf:
        # Metadados
        print("Metadados:", pdf.metadata)
        print(f'{len(pdf.pages)} páginas\n')
        
        if len(pdf.pages) > 0:
            # Extrair texto de uma página
            pagina = pdf.pages[0]
            texto = pagina.extract_text()
            print("Texto (primeiros 500 caracteres):")
            print(texto[:500] if texto else "Nenhum texto encontrado.")
            
            # extract_text() com separador de layout
            # x_tolerance: distância horizontal que define espaço entre palavras
            # y_tolerance: distância vertical que define nova linha
            texto_layout = pagina.extract_text(x_tolerance=3, y_tolerance=3)
            
            # Extraindo de Todas as páginas
            paginas = []
            for i, pag in enumerate(pdf.pages):
                texto_pag = pag.extract_text() or ''
                paginas.append({'pagina': i + 1, 'texto': texto_pag})
                
except FileNotFoundError:
    print(f"Arquivo '{caminho_pdf}' não encontrado.")


# ─── 4.2 Extração de Tabelas ──────────────────────────────────────
print("\n--- 4.2 Extração de Tabelas ---")
try:
    with pdfplumber.open(caminho_pdf) as pdf:
        if len(pdf.pages) > 0:
            pagina = pdf.pages[0]
            
            # Extrair primeira tabela da página
            tabela = pagina.extract_table()
            if tabela:
                # Primeira linha como cabeçalho
                df = pd.DataFrame(tabela[1:], columns=tabela[0])
                print("Primeira Tabela encontrada (DataFrame):")
                print(df)
            else:
                print("Nenhuma tabela encontrada na página 1.")
                
            # Extrair todas as tabelas de uma página
            tabelas = pagina.extract_tables()
            print(f'\n{len(tabelas)} tabela(s) extraída(s) na página 1.')
            
            # Iterar por todas as páginas buscando tabelas
            print("Verificando tabelas em todas as páginas...")
            for i, pag in enumerate(pdf.pages):
                for j, tab in enumerate(pag.extract_tables()):
                    if tab:
                        df_tab = pd.DataFrame(tab[1:], columns=tab[0])
                        print(f'Tabela {j+1} da página {i+1}: Formato {df_tab.shape}')
                        # df_tab.to_csv(f'tabela_p{i+1}_t{j+1}.csv', index=False)
except FileNotFoundError:
    pass # Tratado no bloco anterior


# ─── 4.3 Bounding Boxes e Palavras ────────────────────────────────
print("\n--- 4.3 Bounding Boxes e Palavras ---")
try:
    with pdfplumber.open(caminho_pdf) as pdf:
        if len(pdf.pages) > 0:
            pagina = pdf.pages[0]
            
            # Lista de palavras com metadados completos
            palavras = pagina.extract_words()
            print("Prévia das primeiras 5 palavras com suas coordenadas x/y:")
            for palavra in palavras[:5]:
                print(palavra)
                
            # Recortar região específica da página (bounding box)
            # Útil para extrair apenas o corpo, ignorando cabeçalho e rodapé
            # Coordenadas: (x0, top, x1, bottom) em pontos
            altura = float(pagina.height)
            corpo = pagina.crop((0, 80, pagina.width, altura - 80))
            texto_corpo = corpo.extract_text() or ''
            print(f'\nTexto do corpo (após o crop): {len(texto_corpo)} caracteres extraídos sem cabeçalho/rodapé.')
            
            # Remover cabeçalho e rodapé de todas as páginas iterativamente
            textos_limpos = []
            for pag in pdf.pages:
                recorte = pag.crop((0, 60, pag.width, float(pag.height) - 60))
                textos_limpos.append(recorte.extract_text() or '')
except FileNotFoundError:
    pass
