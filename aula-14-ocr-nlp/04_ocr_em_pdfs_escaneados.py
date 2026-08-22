# ==============================================================================
# Aula 14: OCR + NLP Clássico (Pipeline de Texto)
# Módulo 4: OCR em PDFs Escaneados e EasyOCR
# ==============================================================================
"""
A biblioteca pdf2image converte cada página de um PDF em uma imagem PIL, que pode 
então ser passada diretamente ao Tesseract ou ao EasyOCR. A resolução de 300 DPI 
é o padrão da indústria para digitalização de documentos.
"""

from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
import easyocr
import numpy as np

# ------------------------------------------------------------------------------
# 4.1 Extração Básica de PDFs Escaneados com Tesseract
# ------------------------------------------------------------------------------
def ocr_pdf(caminho_pdf: str,
            dpi: int = 300,
            idioma: str = 'por',
            psm: int = 6) -> list[dict]:
    """Executa OCR em todas as páginas de um PDF escaneado."""
    print(f'Convertendo PDF em imagens a {dpi} DPI...')
    
    paginas = convert_from_path(
        caminho_pdf,
        dpi=dpi,
        fmt='png',       # PNG preserva qualidade (sem compressão JPEG)
        thread_count=4,  # paralelismo na conversão
    )
    
    print(f'Total de paginas: {len(paginas)}')
    config_tess = f'--oem 3 --psm {psm} -l {idioma}'
    resultados = []
    
    for i, img_pagina in enumerate(paginas, start=1):
        print(f' Processando pagina {i}/{len(paginas)}...', end=' ')
        texto = pytesseract.image_to_string(img_pagina, config=config_tess)
        texto = texto.strip()
        
        resultados.append({
            'pagina': i,
            'texto': texto,
            'caracteres': len(texto),
        })
        print(f'{len(texto)} caracteres')
        
    return resultados

def salvar_texto_pdf(resultados: list[dict], destino: str) -> None:
    """Salva o texto extraído de todas as páginas em um único arquivo .txt."""
    with open(destino, 'w', encoding='utf-8') as arq:
        for r in resultados:
            arq.write(f'=== Página {r["pagina"]} ===\n')
            arq.write(r['texto'])
            arq.write('\n\n')
            
    total = sum(r['caracteres'] for r in resultados)
    print(f'Texto salvo em: {destino} ({total} caracteres no total)')


# Exemplo de uso de extração de PDF (Descomente para usar)
# 
# resultados = ocr_pdf('documento_escaneado.pdf', dpi=300)
# salvar_texto_pdf(resultados, 'documento_extraido.txt')
# texto_completo = '\n\n'.join(r['texto'] for r in resultados)


# ------------------------------------------------------------------------------
# 4.2 EasyOCR como Alternativa para Imagens Difíceis
# ------------------------------------------------------------------------------
"""
Quando o Tesseract produz resultados insatisfatórios — imagens de baixa qualidade, 
ângulos oblíquos, fontes não padronizadas — o EasyOCR é a alternativa natural. 
Sua API é mais simples e retorna, junto com o texto, as coordenadas de cada bloco 
e um score de confiança.
"""

def exemplo_easyocr(caminho_img: str):
    """Exemplo demonstrando a leitura de uma imagem com EasyOCR."""
    print("Carregando modelo EasyOCR (pode demorar no primeiro uso)...")
    
    # gpu=False para usar apenas CPU
    leitor = easyocr.Reader(['pt', 'en'], gpu=False)
    
    # OCR em uma imagem
    resultados = leitor.readtext(caminho_img)
    
    # Cada resultado é uma tupla: (bbox, texto, confianca)
    # bbox = [[x1,y1], [x2,y1], [x2,y2], [x1,y2]] (coordenadas do bloco)
    for bbox, texto, confianca in resultados:
        print(f'Conf: {confianca:.2f} | Texto: {texto}')
        
    # Extraindo apenas o texto com confiança >= 0.5
    texto_filtrado = ' '.join(
        texto 
        for _, texto, conf in resultados 
        if conf >= 0.5
    )
    
    print('\nTexto completo:')
    print(texto_filtrado)

# Exemplo de processamento integrado OpenCV -> EasyOCR
# img_array = np.array(Image.open('documento.png').convert('RGB'))
# resultados = leitor.readtext(img_array)


# ------------------------------------------------------------------------------
# Executando um pequeno teste do OCR em PDFs
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Verificando se há algum PDF para testar
    pdf_teste = '035599_COMPLETO.pdf'
    
    if os.path.exists(pdf_teste):
        print("=== Testando Extração de PDF com Tesseract ===")
        try:
            resultados_pdf = ocr_pdf(pdf_teste, dpi=300)
            destino_txt = 'documento_extraido.txt'
            salvar_texto_pdf(resultados_pdf, destino_txt)
            
            # Printa uma prévia do resultado
            print("\nPrévia do texto extraído:")
            print('-' * 40)
            texto_preview = '\n\n'.join(r['texto'] for r in resultados_pdf)
            print(texto_preview[:500] + "\n[...]")
            print('-' * 40)
            
        except Exception as e:
            print(f"Erro no OCR de PDF: {e}")
            
    else:
        print(f"Para testar, coloque um arquivo PDF chamado '{pdf_teste}' nesta pasta.")
        print("Dica: você pode copiar um dos PDFs da pasta da aula 13 para cá e renomeá-lo!")
        
    # Exemplo extra do EasyOCR com imagem
    img_teste = 'documento.png'
    if os.path.exists(img_teste):
        print("\n=== Testando EasyOCR ===")
        try:
            exemplo_easyocr(img_teste)
        except Exception as e:
            print(f"Erro no EasyOCR: {e}")

