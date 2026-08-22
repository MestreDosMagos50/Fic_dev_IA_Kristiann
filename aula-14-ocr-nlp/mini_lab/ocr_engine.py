# ============================================================
# ocr_engine.py — Motor de OCR com pré-processamento
# ============================================================
"""
Extrai texto de imagens e PDFs escaneados.
Escolhe automaticamente entre Pillow (rápido) e OpenCV (robusto)
conforme a qualidade da imagem de entrada.
"""

import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
import cv2
import numpy as np
import os

# Tenta importar pdf2image; se falhar, PDF não será suportado
try:
    from pdf2image import convert_from_path
    PDF_SUPORTADO = True
except ImportError:
    PDF_SUPORTADO = False

# ── Constantes ──────────────────────────────────────────────
CONFIG_TESS = '--oem 3 --psm 6 -l por'
DPI_PADRAO = 300

# ── Pré-processamento ────────────────────────────────────────
def _prep_pillow(img: Image.Image) -> Image.Image:
    """Pré-processamento leve com Pillow — rápido para imagens limpas."""
    img = img.convert('L')
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)
    
    w, h = img.size
    if w < 2000:
        fator = 2000 / w
        img = img.resize((int(w * fator), int(h * fator)), Image.LANCZOS)
    return img

def _prep_opencv(img: Image.Image) -> Image.Image:
    """Pré-processamento robusto com OpenCV — melhor para imagens difíceis."""
    arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    arr = cv2.fastNlMeansDenoising(arr, h=10)
    
    arr = cv2.adaptiveThreshold(
        arr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 10
    )
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    arr = cv2.morphologyEx(arr, cv2.MORPH_OPEN, kernel)
    return Image.fromarray(arr)

# ── Funções de OCR ───────────────────────────────────────────
def ocr_imagem(caminho: str, modo: str = 'auto') -> dict:
    """Extrai texto de uma imagem JPEG, PNG ou similar.
    
    Args:
        caminho: Caminho para o arquivo de imagem.
        modo: 'pillow' | 'opencv' | 'auto'.
              'auto' usa Pillow e, se < 200 chars, tenta OpenCV.
              
    Returns:
        Dict com 'texto', 'modo_usado', 'arquivo'.
    """
    img_original = Image.open(caminho).convert('RGB')
    
    if modo in ('pillow', 'auto'):
        img_proc = _prep_pillow(img_original)
        texto = pytesseract.image_to_string(img_proc, config=CONFIG_TESS)
        modo_used = 'pillow'
        
    if modo == 'auto' and len(texto.strip()) < 200:
        # Resultado pobre com Pillow: tentar OpenCV
        img_proc = _prep_opencv(img_original)
        texto = pytesseract.image_to_string(img_proc, config=CONFIG_TESS)
        modo_used = 'opencv (fallback)'
        
    if modo == 'opencv':
        img_proc = _prep_opencv(img_original)
        texto = pytesseract.image_to_string(img_proc, config=CONFIG_TESS)
        modo_used = 'opencv'
        
    return {
        'arquivo': os.path.basename(caminho),
        'modo_usado': modo_used,
        'texto': texto.strip(),
        'caracteres': len(texto.strip()),
    }

def ocr_pdf(caminho: str, dpi: int = DPI_PADRAO) -> dict:
    """Extrai texto de todas as páginas de um PDF escaneado.
    
    Args:
        caminho: Caminho para o arquivo PDF.
        dpi: Resolução de conversão (padrão: 300).
        
    Returns:
        Dict com 'arquivo', 'paginas' (lista), 'texto_completo'.
    """
    if not PDF_SUPORTADO:
        raise ImportError('pdf2image nao instalado. Execute: pip install pdf2image')
        
    print(f'Convertendo PDF ({dpi} DPI)...')
    imgs = convert_from_path(caminho, dpi=dpi, fmt='png', thread_count=4)
    paginas = []
    
    for i, img in enumerate(imgs, 1):
        print(f' OCR pagina {i}/{len(imgs)}...', end=' ', flush=True)
        img_proc = _prep_pillow(img)
        texto = pytesseract.image_to_string(img_proc, config=CONFIG_TESS).strip()
        paginas.append({'pagina': i, 'texto': texto, 'caracteres': len(texto)})
        print(f'{len(texto)} chars')
        
    texto_completo = '\\n\\n'.join(p['texto'] for p in paginas)
    
    return {
        'arquivo': os.path.basename(caminho),
        'total_paginas': len(paginas),
        'paginas': paginas,
        'texto_completo': texto_completo,
        'caracteres': len(texto_completo),
    }

def extrair_texto(caminho: str, **kwargs) -> dict:
    """Função unificada: detecta tipo (imagem vs PDF) e chama o extrator correto.
    
    Args:
        caminho: Caminho para imagem ou PDF.
        **kwargs: Repassados para ocr_imagem() ou ocr_pdf().
        
    Returns:
        Dict com pelo menos 'texto' e 'arquivo'.
    """
    ext = os.path.splitext(caminho)[1].lower()
    
    if ext == '.pdf':
        resultado = ocr_pdf(caminho, **kwargs)
        resultado['texto'] = resultado['texto_completo']
    else:
        resultado = ocr_imagem(caminho, **kwargs)
        
    return resultado
