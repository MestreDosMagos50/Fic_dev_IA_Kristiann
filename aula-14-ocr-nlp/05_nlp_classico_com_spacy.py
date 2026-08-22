# ==============================================================================
# Aula 14: OCR + NLP Clássico (Pipeline de Texto)
# Módulo 5: NLP Clássico com spaCy
# ==============================================================================
"""
Pipeline de NLP clássico: tokenização, remoção de stopwords, lematização 
e Reconhecimento de Entidades Nomeadas (NER) utilizando spaCy, além de 
limpeza de pós-processamento de OCR via Regex.
"""

import spacy
from collections import Counter
import re
from collections import defaultdict


# ------------------------------------------------------------------------------
# 5.1 Limpeza de Texto Pós-OCR com Expressões Regulares
# ------------------------------------------------------------------------------
def limpar_texto_ocr(texto: str) -> str:
    """Remove artefatos comuns introduzidos pelo OCR.
    
    Aplica as seguintes correções em sequência:
    1. Remove hifens de quebra de linha
    2. Une parágrafos quebrados erroneamente
    3. Normaliza espaços e tabulações
    4. Remove caracteres de controle
    5. Normaliza pontuação duplicada
    6. Remove linhas com apenas lixo
    """
    # 1. Juntar palavras hifenizadas no final de linha ('infor-\nmação' -> 'informação')
    texto = re.sub(r'-\n(\w)', r'\1', texto)
    
    # 2. Substituir quebras de linha simples por espaço
    texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)
    
    # 3. Normalizar espaços múltiplos
    texto = re.sub(r'[ \t]+', ' ', texto)
    
    # 4. Remover caracteres de controle não-imprimíveis
    texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', texto)
    
    # 5. Normalizar pontuação duplicada
    texto = re.sub(r'\.{3,}', '...', texto) # múltiplos pontos -> reticências
    texto = re.sub(r',{2,}', ',', texto)    # vírgulas duplicadas
    
    # 6. Remover linhas-lixo (menos de 3 caracteres alfanuméricos)
    linhas = texto.split('\n')
    linhas_validas = [
        l for l in linhas
        if len(re.findall(r'[a-záéíóúàâêôãõüç]', l, re.IGNORECASE)) >= 3
        or l.strip() == '' # preservar linhas em branco (separadores)
    ]
    texto = '\n'.join(linhas_validas)
    
    # 7. Remover espaços no início e fim
    return texto.strip()


# ------------------------------------------------------------------------------
# 5.2 Stopwords e Lematização (com spaCy)
# ------------------------------------------------------------------------------
def limpar_texto_nlp(texto: str,
                     remover_stopwords: bool = True,
                     lematizar: bool = True,
                     tamanho_minimo: int = 3) -> list[str]:
    """Tokeniza, filtra e lematiza um texto em português."""
    
    print("Carregando o modelo do spaCy...")
    nlp = spacy.load('pt_core_news_sm')
    
    doc = nlp(texto.lower()) # processa em minúsculas
    
    tokens_limpos = []
    for token in doc:
        # Filtros de qualidade
        if token.is_punct: continue     # pontuação
        if token.is_space: continue     # espaços/newlines
        if not token.is_alpha: continue # números, símbolos
        if len(token.text) < tamanho_minimo: continue # tokens curtos demais
        
        if remover_stopwords and token.is_stop: continue
        
        # Lematização ou texto puro
        forma = token.lemma_ if lematizar else token.text
        tokens_limpos.append(forma)
        
    return tokens_limpos


# ------------------------------------------------------------------------------
# 5.3 Reconhecimento de Entidades Nomeadas (NER)
# ------------------------------------------------------------------------------
def extrair_entidades(texto: str) -> None:
    """Extrai entidades estruturadas (pessoas, organizações, locais, datas)."""
    nlp = spacy.load('pt_core_news_sm')
    doc = nlp(texto.strip())
    
    print('=== Entidades Reconhecidas ===')
    for ent in doc.ents:
        print(f'{ent.text:<35} | tipo: {ent.label_:<12} | {spacy.explain(ent.label_)}')
        
    # Agrupar entidades por tipo
    entidades_por_tipo = defaultdict(list)
    for ent in doc.ents:
        entidades_por_tipo[ent.label_].append(ent.text)
        
    print('\n=== Entidades por Tipo ===')
    for tipo, lista in sorted(entidades_por_tipo.items()):
        print(f'{tipo}: {lista}')


# ------------------------------------------------------------------------------
# Executando um pequeno teste do pipeline de NLP (descomente para testar)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    texto_bruto = """
    CONTRATO DE LOCA ÇÃO DE IMÓVEL
    Pelo presente instru mento particular de locação, as partes abaixo qualificadas:
    
    LOCADOR: João Silva, brasileiro, casado, residente em São Paulo.
    O valor mensal acordado é de R$ 2.500,00, pagos em 12 parcelas.
    """
    
    # print("1. Limpeza de OCR")
    # texto_limpo = limpar_texto_ocr(texto_bruto)
    # print(texto_limpo)
    
    # print("\n2. Tokenização e Frequência de Termos")
    # tokens = limpar_texto_nlp(texto_limpo)
    # freq = Counter(tokens)
    # for termo, contagem in freq.most_common(5):
    #     print(f'{termo:<20}: {contagem}x')
        
    # print("\n3. Extração de Entidades")
    # extrair_entidades(texto_limpo)
