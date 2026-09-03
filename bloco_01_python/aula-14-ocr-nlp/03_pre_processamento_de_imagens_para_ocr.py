# ==============================================================================
# Aula 14: OCR + NLP Clássico (Pipeline de Texto)
# Módulo 3: Pré-processamento de Imagens para OCR
# ==============================================================================
"""
O pré-processamento é a etapa de maior impacto na qualidade do OCR.
Técnicas abordadas:
- Pré-processamento básico com Pillow (contraste, nitidez, resize)
- Pré-processamento avançado com OpenCV (binarização adaptativa, denoising, deskew)
"""

from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import cv2
import numpy as np
import pandas as pd


# ------------------------------------------------------------------------------
# 3.1 Pré-processamento com Pillow
# ------------------------------------------------------------------------------
def preprocessar_pillow(caminho_img: str) -> Image.Image:
    """Aplica pré-processamento básico com Pillow para melhorar o OCR.
    
    Etapas: conversão para cinza, aumento de contraste,
    nitidez e redimensionamento para 300 DPI equivalente.
    """
    img = Image.open(caminho_img)
    
    # Passo 1: converter para escala de cinza
    # Elimina a cor — OCR funciona melhor em escala de cinza ou P&B
    img = img.convert('L')
    
    # Passo 2: aumentar contraste
    # Fator 2.0 = dobro do contraste original
    img = ImageEnhance.Contrast(img).enhance(2.0)
    
    # Passo 3: aumentar nitidez
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    
    # Passo 4: filtro de nitidez adicional
    img = img.filter(ImageFilter.SHARPEN)
    
    # Passo 5: redimensionar para 300 DPI (se imagem for menor que 2000px)
    largura, altura = img.size
    if largura < 2000:
        fator = 2000 / largura
        nova_largura = int(largura * fator)
        nova_altura = int(altura * fator)
        img = img.resize((nova_largura, nova_altura), Image.LANCZOS)
        
    return img

# Uso do OCR com pré-processamento Pillow (Descomentar para usar)
# img_processada = preprocessar_pillow('documento.png')
# config = '--oem 3 --psm 6 -l por'
# texto = pytesseract.image_to_string(img_processada, config=config)
# print(texto[:500])


# ------------------------------------------------------------------------------
# 3.2 Pré-processamento Avançado com OpenCV
# ------------------------------------------------------------------------------
def binarizar_adaptativo(img_cinza: np.ndarray) -> np.ndarray:
    """Binarização adaptativa: ideal para iluminação desigual.
    
    Diferente da binarização global (um único limiar para toda a imagem),
    a adaptativa calcula o limiar local em cada região,
    compensando sombras e gradientes de iluminação.
    """
    return cv2.adaptiveThreshold(
        img_cinza,
        255,                                  # valor máximo (branco)
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # peso gaussiano por vizinhança
        cv2.THRESH_BINARY,                    # texto preto, fundo branco
        blockSize=31,                         # tamanho da vizinhança (ímpar, ex: 11, 21, 31)
        C=10                                  # constante subtraída da média (ajusta sensibilidade)
    )

def remover_ruido(img_bin: np.ndarray) -> np.ndarray:
    """Remove pequenos pontos de ruído com operações morfológicas.
    
    Opening = erosão seguida de dilatação: elimina manchas pequenas
    sem afetar as letras, que têm estrutura maior e mais regular.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    return cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)

def corrigir_inclinacao(img: np.ndarray) -> np.ndarray:
    """Detecta e corrige a inclinação (deskew) de um documento escaneado.
    
    Usa a Transformada de Hough para detectar linhas horizontais e
    calcula o ângulo médio de inclinação para rotacionar a imagem.
    """
    coords = np.column_stack(np.where(img < 128)) # pixels escuros
    if len(coords) == 0:
        return img
        
    angulo = cv2.minAreaRect(coords)[-1] # ângulo da caixa mínima
    
    # Ajuste do ângulo: cv2 retorna ângulos entre -90 e 0
    if angulo < -45:
        angulo = 90 + angulo
        
    # Só corrigir se a inclinação for significativa (> 0.5 grau)
    if abs(angulo) < 0.5:
        return img
        
    (h, w) = img.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    rotacionada = cv2.warpAffine(
        img, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return rotacionada

def preprocessar_opencv(caminho_img: str) -> Image.Image:
    """Pipeline completo de pré-processamento com OpenCV."""
    # Carregar como array NumPy (escala de cinza)
    img = cv2.imread(caminho_img, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f'Imagem nao encontrada: {caminho_img}')
        
    # Denoising com filtro não-local (muito eficaz para ruído gaussiano)
    img = cv2.fastNlMeansDenoising(img, h=10)
    
    # Binarização adaptativa
    img_bin = binarizar_adaptativo(img)
    
    # Remoção de ruído morfológico
    img_limpa = remover_ruido(img_bin)
    
    # Correção de inclinação
    img_final = corrigir_inclinacao(img_limpa)
    
    # Converter de volta para PIL (pytesseract aceita ambos)
    return Image.fromarray(img_final)

# Uso: OCR com pré-processamento OpenCV (Descomentar para usar)
# img_tratada = preprocessar_opencv('documento.png')
# config = '--oem 3 --psm 6 -l por'
# texto = pytesseract.image_to_string(img_tratada, config=config)
# print("--- Texto Extraído ---")
# print(texto)


# ------------------------------------------------------------------------------
# 3.3 Modos de Segmentação do Tesseract (PSM)
# ------------------------------------------------------------------------------
"""
O Tesseract oferece 14 modos de segmentação de página (PSM — Page Segmentation Mode)
que controlam como ele interpreta o layout da imagem antes de reconhecer os caracteres.
Escolher o PSM correto é tão importante quanto o pré-processamento.
"""

def exemplos_psm(caminho_img: str):
    """Exemplos de chamadas do Tesseract com diferentes configurações de PSM."""
    img = Image.open(caminho_img)
    
    # PSM 6: documento padrão com texto corrido (contrato, relatório, certidão)
    texto_doc = pytesseract.image_to_string(img, config='--oem 3 --psm 6 -l por')
    
    # PSM 7: linha única (campo de formulário, data, CPF)
    texto_linha = pytesseract.image_to_string(img, config='--oem 3 --psm 7 -l por')
    
    # PSM 11: texto esparso (recibo, nota fiscal fotografada)
    texto_espar = pytesseract.image_to_string(img, config='--oem 3 --psm 11 -l por')
    
    # Dados de confiança por palavra (útil para filtrar resultados ruins)
    dados = pytesseract.image_to_data(
        img, 
        config='--oem 3 --psm 6 -l por',
        output_type=pytesseract.Output.DATAFRAME
    )
    
    # Filtrar apenas palavras com confiança >= 60%
    palavras_confiaveis = dados[dados['conf'] >= 60]['text'].dropna()
    print("Palavras Confiáveis:", palavras_confiaveis.tolist())


# ------------------------------------------------------------------------------
# Executando um pequeno teste do pipeline de OCR
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    
    # 1. Verifica se a imagem de teste existe
    img_teste = 'teste1.jpg'
    
    if os.path.exists(img_teste):
        print("=== Testando Pré-processamento com Pillow ===")
        try:
            img_processada = preprocessar_pillow(img_teste)
            config = '--oem 3 --psm 6 -l por'
            texto = pytesseract.image_to_string(img_processada, config=config)
            print(texto.strip())
        except Exception as e:
            print(f"Erro no OCR Pillow: {e}")
            
        print("\n=== Testando Pré-processamento com OpenCV ===")
        try:
            img_tratada = preprocessar_opencv(img_teste)
            config = '--oem 3 --psm 6 -l por'
            texto2 = pytesseract.image_to_string(img_tratada, config=config)
            print(texto2.strip())
        except Exception as e:
            print(f"Erro no OCR OpenCV: {e}")
            
        print("\n=== Testando Modos de Segmentação (PSM) ===")
        try:
            exemplos_psm(img_teste)
        except Exception as e:
            print(f"Erro nos exemplos de PSM: {e}")
    else:
        print(f"Crie ou adicione uma imagem chamada '{img_teste}' nesta pasta para testar.")
