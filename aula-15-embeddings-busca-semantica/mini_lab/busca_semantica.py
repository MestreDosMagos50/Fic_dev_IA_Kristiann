# busca_semantica.py
# Mini-lab Aula 15 — Motor de busca semântica com sentence-transformers

from __future__ import annotations
import json
import time
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

# ─── Configuração ─────────────────────────────────────────────
MODELO_NOME = 'paraphrase-multilingual-MiniLM-L12-v2'
PASTA_INDICE = Path('indice')
CHUNK_SIZE = 1000 # chars, para corpus inline
TOP_K_PADRAO = 5

# ─── Corpus inline (usado quando não há chunks.json) ──────────
CORPUS = [
    {
        'chunk_id': 'contrato_c001',
        'fonte': 'contrato_servicos.pdf',
        'pagina': 1,
        'texto': ('O presente contrato de prestação de serviços tem vigência de\n'
                  '24 meses, contados a partir da data de assinatura. Qualquer\n'
                  'rescisão antecipada por parte do contratante implicará multa\n'
                  'equivalente a 20% do valor total remanescente do contrato.'),
    },
    {
        'chunk_id': 'contrato_c002',
        'fonte': 'contrato_servicos.pdf',
        'pagina': 1,
        'texto': ('O pagamento deverá ser efetuado mensalmente, até o dia 10 \n'
                  'de cada mês, mediante emissão de nota fiscal. O atraso no \n'
                  'pagamento acarretará juros de 1% ao mês e multa moratória \n'
                  'de 2% sobre o valor em atraso.'),
    },
    {
        'chunk_id': 'contrato_c003',
        'fonte': 'contrato_servicos.pdf',
        'pagina': 2,
        'texto': ('As partes elegem o foro da comarca de São Paulo para dirimir\n'
                  'quaisquer litígios decorrentes deste instrumento, com renúncia \n'
                  'expressa a qualquer outro, por mais privilegiado que seja.'),
    },
    {
        'chunk_id': 'manual_c001',
        'fonte': 'manual_produto.pdf',
        'pagina': 3,
        'texto': ('Para instalar o software, execute o instalador como \n'
                  'administrador e siga as instruções na tela. O sistema \n'
                  'requer Windows 10 ou superior, com mínimo de 8 GB de RAM \n'
                  'e 20 GB de espaço em disco.'),
    },
    {
        'chunk_id': 'manual_c002',
        'fonte': 'manual_produto.pdf',
        'pagina': 5,
        'texto': ('Em caso de falha durante a instalação, verifique se o \n'
                  'antivírus está desativado temporariamente. Erros comuns \n'
                  'incluem: permissão negada, porta em uso e dependência \n'
                  'ausente. Consulte o log em C:\\Temp\\install.log.'),
    },
    {
        'chunk_id': 'relatorio_c001',
        'fonte': 'relatorio_q1.pdf',
        'pagina': 1,
        'texto': ('A receita líquida do primeiro trimestre de 2025 atingiu \n'
                  'R$ 42,3 milhões, representando crescimento de 18% em \n'
                  'relação ao mesmo período do ano anterior. O resultado \n'
                  'operacional foi de R$ 8,7 milhões, com margem de 20,6%.'),
    },
    {
        'chunk_id': 'relatorio_c002',
        'fonte': 'relatorio_q1.pdf',
        'pagina': 2,
        'texto': ('Os custos operacionais cresceram 12% no trimestre, \n'
                  'principalmente devido ao aumento nos preços de matéria-prima\n'
                  'e ao reajuste salarial aplicado em janeiro. A empresa \n'
                  'implementou medidas de eficiência que devem gerar economia \n'
                  'de R$ 2 milhões anuais a partir do segundo semestre.'),
    },
    {
        'chunk_id': 'relatorio_c003',
        'fonte': 'relatorio_q1.pdf',
        'pagina': 3,
        'texto': ('As vendas no canal digital cresceram 45% no trimestre, \n'
                  'respondendo agora por 32% da receita total. O aplicativo \n'
                  'mobile registrou 1,2 milhão de downloads e avaliação \n'
                  'média de 4,7 estrelas nas lojas de aplicativos.'),
    },
]

# ─── Carregamento do corpus ───────────────────────────────────
def carregar_corpus(caminho_json: str | Path | None = None) -> list[dict]:
    """Carrega chunks de um JSON (formato Aula 13) ou usa o corpus inline."""
    if caminho_json and Path(caminho_json).exists():
        with open(caminho_json, encoding='utf-8') as f:
            dados = json.load(f)
        # Suporta formato {'chunks': [...]} ou lista direta
        chunks = dados.get('chunks', dados) if isinstance(dados, dict) else dados
        print(f'Corpus carregado de {caminho_json}: {len(chunks)} chunks')
        return chunks
    
    print(f'Usando corpus interno: {len(CORPUS)} chunks')
    return CORPUS

# ─── Indexação ────────────────────────────────────────────────
def indexar(
    corpus: list[dict],
    modelo: SentenceTransformer,
    forcar_reindexar: bool = False,
) -> tuple[np.ndarray, list[dict]]:
    """
    Gera embeddings para todos os chunks e salva em disco.
    Se o índice já existir, carrega sem reprocessar.
    """
    arq_emb = PASTA_INDICE / 'embeddings.npy'
    arq_meta = PASTA_INDICE / 'metadados.json'
    
    if not forcar_reindexar and arq_emb.exists() and arq_meta.exists():
        print('Índice encontrado — carregando do disco...')
        embs = np.load(arq_emb)
        with open(arq_meta, encoding='utf-8') as f:
            meta = json.load(f)
        print(f' {embs.shape[0]} vetores ({embs.shape[1]}d) carregados')
        return embs, meta
        
    print(f'Indexando {len(corpus)} chunks com {MODELO_NOME}...')
    t0 = time.time()
    
    textos = [c.get('texto_embed', c['texto']) for c in corpus]
    embs = modelo.encode(
        textos,
        batch_size=32,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    
    dt = time.time() - t0
    print(f' Concluído em {dt:.1f}s — {len(corpus)/dt:.0f} chunks/s')
    
    # Salvar
    PASTA_INDICE.mkdir(exist_ok=True)
    np.save(arq_emb, embs)
    with open(arq_meta, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=2)
        
    print(f' Índice salvo em {PASTA_INDICE}/')
    return embs, corpus

# ─── Busca ────────────────────────────────────────────────────
def buscar(
    query: str,
    modelo: SentenceTransformer,
    embeddings: np.ndarray,
    metadados: list[dict],
    k: int = TOP_K_PADRAO,
) -> list[dict]:
    """
    Busca os k chunks mais relevantes para a query.
    Retorna lista de dicts com chunk + score de similaridade.
    """
    vec_query = modelo.encode(query, normalize_embeddings=True)
    scores = embeddings @ vec_query
    top_idx = np.argsort(scores)[::-1][:k]
    
    return [
        {**metadados[i], 'score': float(scores[i])}
        for i in top_idx
    ]

# ─── Exibição ─────────────────────────────────────────────────
def exibir_resultados(query: str, resultados: list[dict]) -> None:
    print(f'\nQuery: "{query}"')
    print('-' * 55)
    for i, r in enumerate(resultados, 1):
        fonte = r.get('fonte', r.get('chunk_id', '?'))
        pagina = r.get('pagina', '?')
        score = r['score']
        texto = r['texto'][:200].replace('\n', ' ')
        print(f'{i}. [{score:.4f}] {fonte} (p.{pagina})')
        print(f'   {texto}...')
    print()

# ─── Avaliação qualitativa ────────────────────────────────────
CASOS_TESTE = [
    {'categoria': 'Direto',     'query': 'rescisão antecipada do contrato',             'esperado': 'multa'},
    {'categoria': 'Sinônimo',   'query': 'encerramento do acordo antes do prazo',       'esperado': 'rescisão'},
    {'categoria': 'Pergunta',   'query': 'Qual é a penalidade por cancelar o contrato?','esperado': 'multa'},
    {'categoria': 'Pagamento',  'query': 'data de vencimento e juros por atraso',       'esperado': 'pagamento'},
    {'categoria': 'Técnico',    'query': 'requisitos mínimos para instalar o software', 'esperado': 'windows'},
    {'categoria': 'Financeiro', 'query': 'crescimento da receita no trimestre',         'esperado': 'receita'},
    {'categoria': 'Digital',    'query': 'desempenho do canal online e aplicativo',     'esperado': 'digital'},
    {'categoria': 'Negativo',   'query': 'previsão do tempo para amanhã',               'esperado': ''}, # nenhum resultado deve ser relevante
]

def avaliar(modelo, embeddings, metadados, k=3):
    print('\n' + '=' * 55)
    print(' AVALIAÇÃO QUALITATIVA')
    print('=' * 55)
    acertos = 0
    checkados = 0
    for caso in CASOS_TESTE:
        resultados = buscar(caso['query'], modelo, embeddings, metadados, k=k)
        textos = ' '.join(r['texto'].lower() for r in resultados)
        esperado = caso['esperado'].lower()
        
        if esperado:
            checkados += 1
            acertou = esperado in textos
            if acertou: acertos += 1
            status = '✓' if acertou else '✗'
        else:
            # Caso negativo: nenhum resultado deve ter score alto
            max_score = max(r['score'] for r in resultados)
            status = '✓' if max_score < 0.5 else '~'
            
        top1 = resultados[0]
        fonte = top1.get('fonte', top1.get('chunk_id', '?'))
        print(f'{status} [{caso["categoria"]:12}] {caso["query"][:45]}')
        print(f'   → top-1: [{top1["score"]:.3f}] {fonte}')
        
    print(f'\nAcertos verificáveis: {acertos}/{checkados} (top-{k})')
    print('=' * 55)

# ─── Loop interativo ──────────────────────────────────────────
def loop_interativo(modelo, embeddings, metadados):
    print('\nModo interativo — digite uma query (ou "sair" para encerrar)')
    print('Use k=N para definir número de resultados. Ex: contrato k=3')
    while True:
        entrada = input('\n> ').strip()
        if not entrada or entrada.lower() == 'sair':
            break
            
        # Extrair k opcional da entrada
        k = TOP_K_PADRAO
        if ' k=' in entrada:
            partes = entrada.rsplit(' k=', 1)
            entrada = partes[0].strip()
            try: k = int(partes[1])
            except ValueError: pass
            
        resultados = buscar(entrada, modelo, embeddings, metadados, k=k)
        exibir_resultados(entrada, resultados)

# ─── Main ─────────────────────────────────────────────────────
def main():
    import sys
    json_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    print('Carregando modelo...')
    t0 = time.time()
    modelo = SentenceTransformer(MODELO_NOME)
    print(f'Modelo pronto em {time.time()-t0:.1f}s')
    
    corpus = carregar_corpus(json_path)
    embeddings, metadados = indexar(corpus, modelo)
    
    # Demonstração: 3 queries representativas
    print('\n' + '=' * 55)
    print(' DEMONSTRAÇÃO DE BUSCA')
    print('=' * 55)
    
    queries_demo = [
        'Qual é a multa por rescisão antecipada?',
        'requisitos para instalar o sistema',
        'resultado financeiro do trimestre',
    ]
    
    for q in queries_demo:
        resultados = buscar(q, modelo, embeddings, metadados, k=2)
        exibir_resultados(q, resultados)
        
    # Avaliação qualitativa
    avaliar(modelo, embeddings, metadados, k=3)
    
    # Loop interativo
    loop_interativo(modelo, embeddings, metadados)

if __name__ == '__main__':
    main()
