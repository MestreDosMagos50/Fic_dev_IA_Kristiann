import re
import spacy
from collections import Counter
from typing import Any

# Carregar modelo uma única vez (operação custosa)
_nlp = None

def _carregar_modelo() -> spacy.Language:
    """Carrega o modelo spaCy na primeira chamada e reutiliza depois."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load('pt_core_news_sm')
        except OSError:
            raise OSError(
                'Modelo spaCy nao encontrado. Execute:\n'
                'python -m spacy download pt_core_news_sm'
            )
    return _nlp

# ── Limpeza pós-OCR ─────────────────────────────────────────
def limpar_ocr(texto: str) -> str:
    """Remove artefatos típicos de OCR e normaliza o texto."""
    # Reunir palavras hifenizadas no final de linha
    texto = re.sub(r'-(\n)(\w)', r'\2', texto)
    # Quebras de linha simples -> espaço; duplas preservadas
    texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)
    # Múltiplos espaços -> um
    texto = re.sub(r'[ \t]+', ' ', texto)
    # Caracteres de controle
    texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', texto)
    # Pontuação duplicada
    texto = re.sub(r'\.{3,}', '...', texto)
    texto = re.sub(r',{2,}', ',', texto)
    # Remover linhas com menos de 3 letras (lixo de OCR)
    linhas = texto.split('\n')
    linhas = [
        l for l in linhas
        if len(re.findall(r'[a-záéíóúàâêôãõüç]', l, re.I)) >= 3
        or l.strip() == ''
    ]
    return '\n'.join(linhas).strip()

# ── Análise NLP ──────────────────────────────────────────────
def tokenizar(texto: str, tamanho_min: int = 3) -> list[str]:
    """Tokeniza, remove stopwords e lematiza o texto."""
    nlp = _carregar_modelo()
    doc = nlp(texto.lower())
    return [
        token.lemma_
        for token in doc
        if token.is_alpha
        and not token.is_stop
        and not token.is_punct
        and len(token.text) >= tamanho_min
    ]

def extrair_entidades(texto: str) -> dict[str, list[str]]:
    """Reconhece entidades nomeadas e agrupa por tipo."""
    nlp = _carregar_modelo()
    doc = nlp(texto)
    entidades: dict[str, list[str]] = {}
    for ent in doc.ents:
        entidades.setdefault(ent.label_, [])
        if ent.text not in entidades[ent.label_]:
            entidades[ent.label_].append(ent.text)
    return entidades

def analisar(texto_bruto: str, top_n: int = 20) -> dict[str, Any]:
    """Pipeline NLP completo: limpeza -> tokenizacao -> NER -> frequência."""
    texto_limpo = limpar_ocr(texto_bruto)
    tokens = tokenizar(texto_limpo)
    frequencia = Counter(tokens)
    entidades = extrair_entidades(texto_limpo)
    
    return {
        'texto_limpo': texto_limpo,
        'total_tokens': len(tokens),
        'vocabulario_unico': len(set(tokens)),
        'top_termos': frequencia.most_common(top_n),
        'entidades': entidades,
        'total_caracteres': len(texto_limpo),
        'total_palavras': len(texto_limpo.split()),
    }
