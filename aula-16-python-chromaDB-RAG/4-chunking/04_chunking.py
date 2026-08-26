"""
Aula 16 — Peça 3: Chunking — Dividindo Documentos
==================================================
Execute: python 04_chunking.py

O que você verá:
  - Chunking por tamanho fixo com sobreposição
  - Chunking semântico por parágrafos
  - Como a sobreposição protege frases na fronteira

Dependências: nenhuma além da stdlib
"""

import re

# ── 1. Chunking por tamanho fixo com sobreposição ────────────────────────
def chunkar_texto(texto: str, tamanho: int = 400,
                  sobreposicao: int = 80) -> list[dict]:
    """Divide texto em chunks de tamanho fixo com sobreposição.

    Args:
        texto:        Texto completo a dividir.
        tamanho:      Número de palavras por chunk.
        sobreposicao: Número de palavras compartilhadas entre chunks adjacentes.

    Returns:
        Lista de dicionários com 'texto', 'indice', 'inicio', 'fim'.
    """
    palavras = texto.split()
    chunks, inicio, indice = [], 0, 0
    while inicio < len(palavras):
        fim   = min(inicio + tamanho, len(palavras))
        chunk = ' '.join(palavras[inicio:fim])
        if len(chunk.split()) >= 20:
            chunks.append({
                'texto':  chunk,
                'indice': indice,
                'inicio': inicio,
                'fim':    fim,
            })
            indice += 1
        inicio += tamanho - sobreposicao
    return chunks


# ── 2. Chunking semântico por parágrafos ─────────────────────────────────
def chunkar_por_paragrafos(texto: str, max_palavras: int = 400,
                            min_palavras: int = 20) -> list[dict]:
    """Divide texto respeitando parágrafos e marcadores estruturais.

    Args:
        texto:        Texto com estrutura de parágrafos ou cláusulas.
        max_palavras: Limite de palavras por chunk.
        min_palavras: Tamanho mínimo para não descartar o chunk.

    Returns:
        Lista de dicionários com 'texto' e 'indice'.
    """
    # Divide em dupla quebra de linha ou antes de marcadores estruturais
    paragrafos = re.split(r'\n{2,}|(?=CLÁUSULA|CAPÍTULO|ARTIGO|SEÇÃO|§)', texto)
    paragrafos = [p.strip() for p in paragrafos if p.strip()]

    chunks, buffer, indice = [], [], 0
    for para in paragrafos:
        palavras_buffer = sum(len(b.split()) for b in buffer)
        palavras_para   = len(para.split())
        if buffer and palavras_buffer + palavras_para > max_palavras:
            chunks.append({'texto': ' '.join(buffer), 'indice': indice})
            indice += 1
            buffer = []
        buffer.append(para)

    if buffer:
        texto_final = ' '.join(buffer)
        if len(texto_final.split()) >= min_palavras:
            chunks.append({'texto': texto_final, 'indice': indice})

    return chunks


# ── Demonstração ──────────────────────────────────────────────────────────
TEXTO_EXEMPLO = """
CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE CONSULTORIA

Pelo presente instrumento, as partes abaixo qualificadas celebram contrato
de prestação de serviços nas condições aqui descritas.

CLÁUSULA PRIMEIRA — DO OBJETO
A CONTRATADA se compromete a prestar serviços de consultoria em tecnologia
da informação, incluindo análise de sistemas, desenvolvimento de software
e treinamento de equipes. O escopo detalhado consta no Anexo I.

CLÁUSULA SEGUNDA — DO PRAZO
O presente contrato tem vigência de doze meses a partir da data de
assinatura, podendo ser prorrogado mediante acordo escrito entre as partes
com antecedência mínima de 30 dias.

CLÁUSULA TERCEIRA — DO VALOR
O valor mensal dos serviços é de R$ 10.000,00, pagos até o quinto dia útil
de cada mês mediante nota fiscal emitida pela CONTRATADA.

CLÁUSULA QUARTA — DA RESCISÃO
Em caso de rescisão antecipada sem justa causa pela CONTRATANTE, será devida
multa equivalente a 20% do valor total remanescente do contrato.
""".strip()


print('=== Chunking por Tamanho Fixo (tamanho=30, sobreposicao=8) ===')
chunks_fixo = chunkar_texto(TEXTO_EXEMPLO, tamanho=30, sobreposicao=8)
print(f'Total de chunks: {len(chunks_fixo)}\n')
for c in chunks_fixo:
    print(f"Chunk {c['indice']:02d} | palavras {c['inicio']}-{c['fim']}")
    print(f"  {c['texto'][:90]}...")
    print()

print('=' * 60)
print('=== Chunking por Parágrafos (max_palavras=25) ===')
chunks_para = chunkar_por_paragrafos(TEXTO_EXEMPLO, max_palavras=25, min_palavras=5)
print(f'Total de chunks: {len(chunks_para)}\n')
for c in chunks_para:
    print(f"--- Chunk {c['indice']} ---")
    print(c['texto'])
    print()

print('=' * 60)
print('Nota: em produção use tamanho=400 e sobreposicao=80.')
print('Esses valores produzem 3 a 5 chunks por página A4.')
