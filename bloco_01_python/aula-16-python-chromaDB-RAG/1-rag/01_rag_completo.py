"""
Aula 16 — RAG Completo (indexação + recuperação)
================================================
Execute em ordem:
  1. python 1-rag/01_rag_completo.py indexar  pdfs/arquivo.pdf
  2. python 1-rag/01_rag_completo.py perguntar

Dependências:
  pip install chromadb sentence-transformers pdfplumber
"""

import sys
import os
import hashlib
import pdfplumber
from sentence_transformers import SentenceTransformer
import chromadb

# ── Configuração ──────────────────────────────────────────────────────────
MODELO_NOME      = 'paraphrase-multilingual-MiniLM-L12-v2'
DB_PATH          = './banco_rag'
COLECAO_NOME     = 'pdf_chunks'
CHUNK_PALAVRAS   = 400
CHUNK_OVERLAP    = 80
N_RESULTADOS     = 5
LIMIAR_DISTANCIA = 0.65

# ── Inicialização (lazy) ──────────────────────────────────────────────────
_modelo  = None
_colecao = None

def obter_modelo():
    global _modelo
    if _modelo is None:
        print(f'Carregando modelo: {MODELO_NOME}')
        _modelo = SentenceTransformer(MODELO_NOME)
    return _modelo

def obter_colecao():
    global _colecao
    if _colecao is None:
        client   = chromadb.PersistentClient(path=DB_PATH)
        _colecao = client.get_or_create_collection(
            name=COLECAO_NOME,
            metadata={'hnsw:space': 'cosine', 'modelo': MODELO_NOME}
        )
    return _colecao

# ── Chunking ──────────────────────────────────────────────────────────────
def chunkar(texto: str) -> list[str]:
    palavras = texto.split()
    chunks, inicio = [], 0
    while inicio < len(palavras):
        fim   = min(inicio + CHUNK_PALAVRAS, len(palavras))
        chunk = ' '.join(palavras[inicio:fim])
        if len(chunk.split()) >= 20:
            chunks.append(chunk)
        inicio += CHUNK_PALAVRAS - CHUNK_OVERLAP
    return chunks

# ── Fase 1: Indexação ─────────────────────────────────────────────────────
def indexar(caminho_pdf: str) -> int:
    nome    = os.path.basename(caminho_pdf)
    modelo  = obter_modelo()
    colecao = obter_colecao()

    print(f'\nIndexando: {nome}')

    # 1. Extrair texto por página
    paginas = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for i, pag in enumerate(pdf.pages, 1):
            texto = (pag.extract_text() or '').strip()
            if len(texto.split()) >= 10:
                paginas.append({'pagina': i, 'texto': texto})
    print(f'  Páginas com texto: {len(paginas)}')

    # 2. Chunkar e montar listas
    ids, docs, metas = [], [], []
    for pg in paginas:
        for j, chunk in enumerate(chunkar(pg['texto'])):
            ids.append(hashlib.md5(chunk.encode()).hexdigest()[:16])
            docs.append(chunk)
            metas.append({'arquivo': nome, 'pagina': pg['pagina'], 'chunk_local': j})
    print(f'  Chunks gerados: {len(docs)}')

    # 3. Filtrar IDs já existentes (idempotência)
    ja_existem = set(colecao.get(ids=ids)['ids']) if ids else set()
    novos = [(i, d, m) for i, d, m in zip(ids, docs, metas) if i not in ja_existem]

    if not novos:
        print('  Todos os chunks já estavam indexados.')
        return 0

    ids_n, docs_n, metas_n = zip(*novos)

    # 4. Gerar embeddings
    print(f'  Gerando embeddings para {len(docs_n)} chunks...')
    embs = modelo.encode(
        list(docs_n), batch_size=32,
        normalize_embeddings=True, show_progress_bar=True
    ).tolist()

    # 5. Inserir no ChromaDB
    colecao.add(ids=list(ids_n), documents=list(docs_n),
                embeddings=embs, metadatas=list(metas_n))

    print(f'  Inseridos: {len(docs_n)} chunks')
    print(f'  Total na coleção: {colecao.count()}')
    return len(docs_n)

# ── Fase 2: Recuperação ───────────────────────────────────────────────────
def recuperar(pergunta: str) -> list[dict]:
    modelo  = obter_modelo()
    colecao = obter_colecao()

    emb = modelo.encode(pergunta, normalize_embeddings=True).tolist()

    resultado = colecao.query(
        query_embeddings=[emb],
        n_results=N_RESULTADOS,
        include=['documents', 'metadatas', 'distances']
    )

    chunks = []
    for rank, (doc, meta, dist) in enumerate(zip(
        resultado['documents'][0],
        resultado['metadatas'][0],
        resultado['distances'][0]
    ), start=1):
        if dist <= LIMIAR_DISTANCIA:
            chunks.append({
                'rank':      rank,
                'texto':     doc,
                'arquivo':   meta.get('arquivo', '?'),
                'pagina':    meta.get('pagina', '?'),
                'distancia': round(dist, 4),
                'relevancia': round(1 - dist, 4),
            })
    return chunks

def montar_contexto(chunks: list[dict], max_palavras: int = 1500) -> str:
    partes, total = [], 0
    for c in chunks:
        n = len(c['texto'].split())
        if total + n > max_palavras:
            break
        partes.append(f"[{c['arquivo']} — p. {c['pagina']}]\n{c['texto']}")
        total += n
    return '\n\n---\n\n'.join(partes)

def exibir(pergunta: str, chunks: list[dict]) -> None:
    print()
    print('=' * 62)
    print(f'PERGUNTA : {pergunta}')
    print(f'CHUNKS   : {len(chunks)} recuperados')
    print('=' * 62)
    if not chunks:
        print('Nenhum chunk dentro do limiar de relevância.')
        print('Tente reformular ou reduza o LIMIAR_DISTANCIA.')
        return
    for c in chunks:
        bar = '#' * int(c['relevancia'] * 20)
        print(f"\n  #{c['rank']} [{bar:<20}] rel={c['relevancia']:.3f}")
        print(f"      {c['arquivo']} — pág. {c['pagina']}")
        print(f"      {c['texto'][:180].strip()}...")
    print('=' * 62)

# ── Loop interativo ───────────────────────────────────────────────────────
def loop_perguntas():
    colecao = obter_colecao()
    if colecao.count() == 0:
        print('Banco vazio. Execute primeiro:')
        print('  python 01_rag_completo.py indexar <arquivo.pdf>')
        return

    print('=' * 62)
    print(f'  RAG — {colecao.count()} chunks indexados')
    print("  Digite 'sair' para encerrar.")
    print('=' * 62)

    while True:
        pergunta = input('\nPergunta: ').strip()
        if not pergunta:
            continue
        if pergunta.lower() in ('sair', 'exit', 'q'):
            print('Encerrando.')
            break
        chunks = recuperar(pergunta)
        exibir(pergunta, chunks)

# ── Ponto de entrada ──────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso:')
        print('  python 01_rag_completo.py indexar <arquivo.pdf>')
        print('  python 01_rag_completo.py perguntar')
        sys.exit(1)

    comando = sys.argv[1].lower()

    if comando == 'indexar':
        if len(sys.argv) < 3:
            print('Informe o caminho do PDF: python 1-rag/01_rag_completo.py indexar pdfs/arquivo2.pdf')
            sys.exit(1)
        indexar(sys.argv[2])

    elif comando == 'perguntar':
        loop_perguntas()

    else:
        print(f'Comando desconhecido: {comando}')
        print('Use: indexar  ou  perguntar')
