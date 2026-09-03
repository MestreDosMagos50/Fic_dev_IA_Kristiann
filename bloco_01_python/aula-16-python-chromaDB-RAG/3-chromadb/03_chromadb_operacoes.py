"""
Aula 16 — Peça 2: ChromaDB — Cliente, Coleções e CRUD
======================================================
Execute: python 3-chromadb/03_chromadb_operacoes.py

O que você verá:
  - Diferença entre cliente efêmero e persistente
  - Como criar e gerenciar coleções
  - add(), query() com filtros where e where_document
  - get(), update(), upsert(), delete()

Dependências: pip install chromadb sentence-transformers
"""

import chromadb
from sentence_transformers import SentenceTransformer

# ── 1. Modos de cliente ───────────────────────────────────────────────────
print('=== Modos de Cliente ===')

# Efêmero: apenas para testes — dados perdidos ao encerrar
client_mem = chromadb.EphemeralClient()
print('Efêmero criado (apenas memória)')

# Persistente: dados salvos em disco
client = chromadb.PersistentClient(path='./banco_demo')
print('Persistente criado em ./banco_demo')

# ── 2. Coleções ───────────────────────────────────────────────────────────
print('\n=== Criando Coleção ===')
colecao = client.get_or_create_collection(
    name='exemplos',
    metadata={
        'hnsw:space': 'cosine',          # métrica de distância
        'description': 'Chunks de teste',
    }
)
print(f'Coleção: {colecao.name} | Documentos: {colecao.count()}')

# ── 3. Gerar embeddings ───────────────────────────────────────────────────
print('\n=== Gerando Embeddings ===')
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

documentos = [
    'O contrato de locação foi assinado entre as partes em março de 2024.',
    'O valor do aluguel mensal é de R$ 2.500,00 com reajuste anual pelo IGPM.',
    'Em caso de rescisão antecipada, aplica-se multa de três aluguéis.',
    'A procuração foi outorgada com poderes amplos ao advogado.',
]
ids = ['doc1_c0', 'doc1_c1', 'doc1_c2', 'doc2_c0']
metadatas = [
    {'arquivo': 'contrato.pdf', 'pagina': 1, 'tipo': 'contrato'},
    {'arquivo': 'contrato.pdf', 'pagina': 1, 'tipo': 'contrato'},
    {'arquivo': 'contrato.pdf', 'pagina': 2, 'tipo': 'contrato'},
    {'arquivo': 'procuracao.pdf', 'pagina': 1, 'tipo': 'procuracao'},
]
embeddings = modelo.encode(documentos, normalize_embeddings=True).tolist()

# ── 4. add() ─────────────────────────────────────────────────────────────
print('\n=== add() — Inserir Documentos ===')
colecao.add(ids=ids, documents=documentos,
            embeddings=embeddings, metadatas=metadatas)
print(f'Total após add: {colecao.count()}')

# ── 5. query() — busca semântica ─────────────────────────────────────────
print('\n=== query() — Busca Semântica Pura ===')
emb_query = modelo.encode(
    'Qual o valor do aluguel e o reajuste?',
    normalize_embeddings=True
).tolist()

resultado = colecao.query(
    query_embeddings=[emb_query],
    n_results=3,
    include=['documents', 'metadatas', 'distances']
)
for doc, meta, dist in zip(
    resultado['documents'][0],
    resultado['metadatas'][0],
    resultado['distances'][0]
):
    print(f'  dist={dist:.4f} | {meta["arquivo"]} p.{meta["pagina"]} | {doc[:60]}...')

# ── 6. query() com where (filtro de metadados) ───────────────────────────
print('\n=== query() com where — Filtro por Metadados ===')
resultado_filtrado = colecao.query(
    query_embeddings=[emb_query],
    n_results=3,
    where={'tipo': 'contrato'},           # só chunks de contratos
    include=['documents', 'distances']
)
for doc, dist in zip(resultado_filtrado['documents'][0], resultado_filtrado['distances'][0]):
    print(f'  dist={dist:.4f} | {doc[:70]}...')

# ── 7. query() com where_document (filtro de conteúdo) ───────────────────
print('\n=== query() com where_document — Filtro por Conteúdo ===')
resultado_conteudo = colecao.query(
    query_embeddings=[emb_query],
    n_results=3,
    where_document={'$contains': 'aluguel'},  # chunk deve conter a palavra
    include=['documents', 'distances']
)
for doc, dist in zip(resultado_conteudo['documents'][0], resultado_conteudo['distances'][0]):
    print(f'  dist={dist:.4f} | {doc[:70]}...')

# ── 8. get() — buscar por ID ─────────────────────────────────────────────
print('\n=== get() — Buscar por ID ===')
resultado_get = colecao.get(ids=['doc1_c0', 'doc1_c1'], include=['documents', 'metadatas'])
for doc_id, doc, meta in zip(resultado_get['ids'], resultado_get['documents'], resultado_get['metadatas']):
    print(f'  {doc_id} | {meta} | {doc[:50]}...')

# ── 9. update() ──────────────────────────────────────────────────────────
print('\n=== update() — Atualizar Documento Existente ===')
colecao.update(
    ids=['doc1_c0'],
    documents=['Texto corrigido do primeiro chunk do contrato.'],
    metadatas=[{'arquivo': 'contrato.pdf', 'pagina': 1, 'tipo': 'contrato', 'revisado': True}]
)
print('doc1_c0 atualizado.')

# ── 10. upsert() ─────────────────────────────────────────────────────────
print('\n=== upsert() — Inserir ou Substituir ===')
emb_novo = modelo.encode(['Aditivo contratual registrado em cartório.'], normalize_embeddings=True).tolist()
colecao.upsert(
    ids=['doc3_c0'],
    documents=['Aditivo contratual registrado em cartório.'],
    embeddings=emb_novo,
    metadatas=[{'arquivo': 'aditivo.pdf', 'pagina': 1, 'tipo': 'aditivo'}]
)
print(f'Total após upsert: {colecao.count()}')

# ── 11. delete() ─────────────────────────────────────────────────────────
print('\n=== delete() — Remover por ID ===')
colecao.delete(ids=['doc2_c0'])
print(f'Total após delete por ID: {colecao.count()}')

print('\n=== delete() — Remover por Filtro de Metadados ===')
colecao.delete(where={'arquivo': 'procuracao.pdf'})
print(f'Total após delete por filtro: {colecao.count()}')

print('\nFinalizado. Banco salvo em ./banco_demo/')
