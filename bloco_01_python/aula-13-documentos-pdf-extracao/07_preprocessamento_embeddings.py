# ====================================================================
# MÓDULO 7: Pré-processamento para Embeddings e JSON de Saída
# ====================================================================
import re
import importlib

# Importando a função de limpeza base
limpeza_module = importlib.import_module("05_limpeza_texto")
limpar_texto = limpeza_module.limpar_texto

# ─── 7.1 Pipeline de Pré-processamento Leve ─────────────────────────
def preprocessar_para_embedding(texto: str) -> str:
    """
    Pré-processamento leve para texto destinado a embeddings.
    NÃO remove stopwords nem faz stemming — isso prejudica embeddings.
    """
    if not texto or not texto.strip():
        return ''
        
    # 1. Limpeza base (herda todo o pipeline do Módulo 5)
    texto = limpar_texto(texto)
    
    # 2. Lowercase — opcional; depende do modelo de embedding
    # Modelos case-sensitive (BERT, E5) performam melhor sem lowercase
    # Modelos antigos (word2vec) beneficiam do lowercase
    # texto = texto.lower()  # descomente apenas se necessário
    
    # 3. Remover URLs (substitui pelo token especial [URL])
    texto = re.sub(r'https?://\S+|www\.\S+', '[URL]', texto)
    
    # 4. Remover e-mails (substitui pelo token especial [EMAIL])
    texto = re.sub(r'\b[\w.+-]+@[\w-]+\.[\w.]+\b', '[EMAIL]', texto)
    
    # 5. Normalizar números longos (evita tokens raros no modelo)
    # Preservar anos (4 dígitos) e valores monetários com contexto
    texto = re.sub(r'\b\d{6,}\b', '[NUM]', texto)
    
    # 6. Garantir espaço único
    texto = re.sub(r'[ \t]+', ' ', texto)
    
    return texto.strip()

# Estimativa de tokens (regra dos 4 chars por token para português)
def estimar_tokens(texto: str, chars_por_token: float = 4.0) -> int:
    return max(1, int(len(texto) / chars_por_token))

if __name__ == '__main__':
    # Teste
    texto = 'Acesse https://empresa.com ou envie para joao@empresa.com.br para concorrer a 1500000 reais.'
    print("Texto original:")
    print(texto)
    
    print("\nTexto pré-processado para Embeddings:")
    print(preprocessar_para_embedding(texto))
