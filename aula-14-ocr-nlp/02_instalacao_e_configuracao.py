# ==============================================================================
# Aula 14: OCR + NLP Clássico (Pipeline de Texto)
# Módulo 2: Instalação e Configuração
# ==============================================================================
"""
O Tesseract é um binário externo — um programa independente instalado no sistema
operacional — e o pytesseract é a biblioteca Python que serve de ponte para chamá-lo.
Ambos precisam estar instalados e o Python precisa saber onde encontrar o executável
do Tesseract. Essa é a fonte de erro mais comum para iniciantes nesta área.
"""

# ------------------------------------------------------------------------------
# 2.1 Instalando o Tesseract no Sistema Operacional (comandos de terminal)
# ------------------------------------------------------------------------------
# ── Linux (Ubuntu / Debian) ────────────────────────────────
# sudo apt-get update
# sudo apt-get install -y tesseract-ocr
# sudo apt-get install -y tesseract-ocr-por # pacote de idioma português
# sudo apt-get install -y libtesseract-dev # headers para compilação

# Verificar instalação e versão
# tesseract --version
# tesseract 5.x.x

# Listar idiomas instalados
# tesseract --list-langs
# eng por osd

# ── macOS (via Homebrew) ───────────────────────────────────
# brew install tesseract
# brew install tesseract-lang # instala todos os idiomas

# ── Windows ────────────────────────────────────────────────
# Baixar instalador em: https://github.com/UB-Mannheim/tesseract/wiki
# Marcar 'Additional language data' > Portuguese durante instalação
# Adicionar ao PATH: C:\Program Files\Tesseract-OCR


# ------------------------------------------------------------------------------
# 2.2 Instalando as Bibliotecas Python
# ------------------------------------------------------------------------------
# Instalar todas as dependências desta aula de uma vez:
# pip install pytesseract # bridge Python -> Tesseract
# pip install easyocr # OCR alternativo (baixa modelos no 1o uso)
# pip install Pillow # manipulação de imagens (PIL)
# pip install opencv-python # pré-processamento avançado de imagens
# pip install pdf2image # converte páginas de PDF em imagens
# pip install spacy # NLP clássico
# pip install nltk # NLP alternativo / stopwords adicionais

# Baixar o modelo de português do spaCy
# python -m spacy download pt_core_news_sm

# Baixar stopwords do NLTK (executar uma única vez, dentro do Python):
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')


# ------------------------------------------------------------------------------
# Configuração no Python
# ------------------------------------------------------------------------------
import pytesseract

# No Windows: pode ser necessário informar ao pytesseract onde está o executável
# (no Linux/Mac o Python geralmente detecta automaticamente pelo PATH)
#
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

"""
AVISO: O EasyOCR baixa modelos de deep learning automaticamente no primeiro uso — o
modelo para português tem cerca de 50 MB. Certifique-se de ter conexão de internet
na primeira execução. Os modelos ficam em cache em ~/.EasyOCR/ e não precisam
ser baixados novamente nas execuções seguintes.
"""
