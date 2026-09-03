# ====================================================================
# MÓDULO 1: PDF - Estrutura Interna e o Problema da Extração
# ====================================================================
# O formato PDF (Portable Document Format) foi projetado para apresentação visual,
# não para extração de texto. Internamente, armazena posições absolutas de glifos.
# Não há, em geral, um conceito de 'parágrafo' ou 'coluna' explícito no arquivo.
#
# Tipos de PDF e Comportamento na extração:
# - PDF nativo (texto): Texto extraível diretamente — qualidade boa a excelente.
# - PDF nativo com colunas: Ordem das palavras pode sair errada sem heurística de layout.
# - PDF escaneado (imagem): Sem texto extraível — requer OCR (Reconhecimento Óptico).
# - PDF com tabelas: Estrutura da tabela se perde sem ferramenta específica.
# - PDF com fórmulas: Fórmulas matemáticas raramente extraem corretamente.
# - PDF com proteção: Extração pode ser bloqueada por senha ou permissões.
#
# DICA: Antes de qualquer extração, inspecione o PDF visualmente. Se conseguir 
# selecionar o texto, é um PDF nativo. Se não, é escaneado e precisará de OCR.
#
# (Este módulo é puramente conceitual e introdutório)
