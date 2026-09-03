# ==============================================================================
# Aula 14: OCR + NLP Clássico (Pipeline de Texto)
# Módulo 1: OCR - Reconhecimento Óptico de Caracteres
# ==============================================================================
"""
O OCR (Optical Character Recognition) é a tecnologia que converte imagens de texto 
em texto digital editável e pesquisável.

A qualidade do OCR depende da qualidade da imagem e do modelo de reconhecimento.
O pré-processamento da imagem é a etapa com maior impacto prático na precisão.

Estágios de funcionamento interno:
1. Pré-processamento: Conversão para escala de cinza, binarização, remoção de ruído, etc.
2. Detecção de layout: Identificação de regiões de texto, colunas, tabelas, etc.
3. Segmentação de linhas: Divisão do bloco de texto em linhas individuais.
4. Reconhecimento: Classificação de caracteres (ex: usando HMM ou LSTM).
5. Pós-processamento: Correção ortográfica e uso de dicionários.

Principais Ferramentas:
- Tesseract (via pytesseract): Excelente para texto impresso limpo e de alta resolução.
- EasyOCR: Superior para texto manuscrito, fontes variadas e imagens complexas.
"""

# Este módulo foca apenas na fundamentação teórica conforme material.
# As implementações e práticas estarão nos módulos subsequentes.
pass
