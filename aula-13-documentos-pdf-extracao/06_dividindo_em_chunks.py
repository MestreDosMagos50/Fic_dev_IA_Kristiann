# ====================================================================
# MÓDULO 6: Dividindo em Chunks
# ====================================================================
# Modelos de linguagem têm uma janela de contexto limitada.
# Chunks menores permitem recuperação mais precisa em sistemas de RAG.

import importlib

# Importando a função de limpeza do módulo 5 
# (usando importlib devido ao arquivo começar com número)
limpeza_module = importlib.import_module("05_limpeza_texto")
limpar_texto = limpeza_module.limpar_texto

# ─── 6.1 Chunk por Página ───────────────────────────────────────────
def chunks_por_pagina(paginas: list[dict]) -> list[dict]:
    """
    Recebe lista de {'pagina': N, 'texto': '...'}
    Retorna a mesma lista, pulando páginas vazias.
    """
    return [
        {
            'chunk_id': f'p{p["pagina"]:03d}',
            'pagina': p['pagina'],
            'texto': limpar_texto(p['texto']),
            'n_chars': len(limpar_texto(p['texto'])),
        }
        for p in paginas
        if p['texto'].strip()
    ]

# ─── 6.2 Chunk por Tamanho Fixo com Overlap ─────────────────────────
def chunks_por_tamanho(
    texto: str,
    tamanho_max: int = 1000,
    overlap: int = 200,
    origem: str = '',
) -> list[dict]:
    """
    Divide texto em chunks de até tamanho_max caracteres.
    Chunks consecutivos se sobrepõem em 'overlap' caracteres.
    """
    texto = limpar_texto(texto)
    if not texto:
        return []
        
    chunks = []
    inicio = 0
    idx = 0
    
    while inicio < len(texto):
        fim = inicio + tamanho_max
        trecho = texto[inicio:fim]
        
        # Tentar quebrar no espaço mais próximo antes do limite para não cortar palavras
        if fim < len(texto):
            ultimo_espaco = trecho.rfind(' ')
            if ultimo_espaco > tamanho_max * 0.6:  # ao menos 60% preenchido
                trecho = trecho[:ultimo_espaco]
                fim = inicio + ultimo_espaco
                
        chunks.append({
            'chunk_id': f'{origem}_c{idx:03d}' if origem else f'c{idx:03d}',
            'texto': trecho.strip(),
            'n_chars': len(trecho.strip()),
            'inicio': inicio,
            'fim': inicio + len(trecho),
        })
        
        inicio = fim - overlap  # retroceder 'overlap' chars para próximo chunk
        idx += 1
        
    return chunks

# ─── 6.3 Chunk por Parágrafo ────────────────────────────────────────
def chunks_por_paragrafo(
    texto: str,
    max_chars: int = 2000,
    origem: str = '',
) -> list[dict]:
    """
    Divide por parágrafo (\n\n). Agrega parágrafos curtos até
    atingir max_chars para evitar chunks muito pequenos.
    """
    texto = limpar_texto(texto)
    paragrafos = [p.strip() for p in texto.split('\n\n') if p.strip()]
    chunks, atual, idx = [], '', 0
    
    for par in paragrafos:
        candidato = (atual + '\n\n' + par).strip() if atual else par
        if len(candidato) <= max_chars:
            atual = candidato
        else:
            if atual:
                chunks.append({
                    'chunk_id': f'{origem}_c{idx:03d}' if origem else f'c{idx:03d}',
                    'texto': atual,
                    'n_chars': len(atual),
                })
                idx += 1
            atual = par
            
    if atual:
        chunks.append({
            'chunk_id': f'{origem}_c{idx:03d}' if origem else f'c{idx:03d}',
            'texto': atual,
            'n_chars': len(atual)
        })
        
    return chunks

if __name__ == '__main__':
    # Teste rápido
    texto_teste = "Primeiro parágrafo de teste.\n\n" * 15 # texto razoavelmente grande
    
    print("--- Teste: Chunk por Tamanho ---")
    chunks_tam = chunks_por_tamanho(texto_teste, tamanho_max=100, overlap=20)
    print(f"Gerados {len(chunks_tam)} chunks.")
    for i, c in enumerate(chunks_tam[:3]):
        print(f"[{c['chunk_id']}] {c['texto'][:50]}... (chars: {c['n_chars']})")

    print("\n--- Teste: Chunk por Parágrafo ---")
    chunks_par = chunks_por_paragrafo(texto_teste, max_chars=100)
    print(f"Gerados {len(chunks_par)} chunks.")
    for i, c in enumerate(chunks_par[:3]):
        print(f"[{c['chunk_id']}] {c['texto'][:50]}... (chars: {c['n_chars']})")
