# ====================================================================
# MÓDULO 2: PyPDF2 vs pdfplumber — Quando Usar Cada Um
# ====================================================================
#
# pypdf (sucessor do PyPDF2):
# - Instalação: pip install pypdf
# - Velocidade: Muito rápido
# - Qualidade do texto: Boa para PDFs simples
# - Extração de tabelas: Não
# - Bounding boxes: Não
# - Manipulação: Sim — ponto forte (merge, split)
# - Melhor para: ETL rápido, PDFs simples, manipulação de arquivos (juntar/separar páginas).
#
# pdfplumber:
# - Instalação: pip install pdfplumber
# - Velocidade: Mais lento (faz análise detalhada de layout)
# - Qualidade do texto: Excelente, especialmente em PDFs complexos
# - Extração de tabelas: Sim — usando extract_table()
# - Bounding boxes: Sim — obtém coordenadas x,y de cada palavra
# - Manipulação: Somente leitura
# - Melhor para: PDFs com layout complexo, tabelas, e quando for necessária análise visual precisa.
#
# REGRA PRÁTICA DE ESCOLHA:
# Use `pypdf` quando precisar de velocidade e processar grandes volumes de PDFs 
# nativos simples, ou quando precisar apenas mesclar/dividir/rotacionar páginas. 
#
# Use `pdfplumber` quando a qualidade do texto extraído for crítica, 
# se o PDF tiver múltiplas colunas, tabelas ou quando precisar das coordenadas 
# exatas dos elementos na página. Em caso de dúvida, teste ambos.
#
# (Este módulo é apenas conceitual e comparativo)
