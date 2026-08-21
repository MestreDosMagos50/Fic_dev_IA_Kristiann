# ====================================================================
# MÓDULO 5: Limpeza de Texto Extraído
# ====================================================================
import re
import unicodedata

# ─── 5.2 Função de Limpeza ──────────────────────────────────────────
def limpar_texto(texto: str) -> str:
    """
    Aplica pipeline de limpeza em texto extraído de PDF.
    Retorna string limpa, pronta para chunking ou embeddings.
    """
    if not texto or not texto.strip():
        return ''
        
    # 1. Normalizar unicode (NFC): unificar formas de caracteres acentuados
    texto = unicodedata.normalize('NFC', texto)
    
    # 2. Remover caracteres de controle (\x00–\x1F exceto \n e \t)
    texto = re.sub(r'[\x00-\x08\x0b-\x1f\x7f]', '', texto)
    
    # 3. Reparar hifenização de quebra de linha
    # Ex: 'aná-\nlise' → 'análise'
    texto = re.sub(r'(\w+)-\n(\w+)', r'\1\2', texto)
    
    # 4. Juntar linhas quebradas no meio de frases
    # Uma quebra de linha isolada (sem linha em branco antes) → espaço
    texto = re.sub(r'(?<!\n)\n(?!\n)', ' ', texto)
    
    # 5. Recolher múltiplos espaços em um único
    texto = re.sub(r'[ \t]+', ' ', texto)
    
    # 6. Limitar linhas em branco consecutivas a no máximo 2
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    
    # 7. Limpar espaço antes de pontuação
    texto = re.sub(r' +([.,;:!?])', r'\1', texto)
    
    return texto.strip()

if __name__ == '__main__':
    # Teste rápido
    bruto = 'aná-\nlise de da-\ndos\n\n\n\n  Página 1 de 10 '
    print("Texto Bruto:")
    print(repr(bruto))
    
    limpo = limpar_texto(bruto)
    print("\nTexto Limpo:")
    print(repr(limpo))
