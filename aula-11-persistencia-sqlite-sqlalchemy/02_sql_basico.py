import sqlite3

# ====================================================================
# MÓDULO 2: SQL Básico com o Módulo sqlite3
# ====================================================================
# ─── 2.1 Conexao, Cursor e Commit ──────────────────────────────
# 'with' faz commit automatico em sucesso e rollback em excecao
with sqlite3.connect('pipeline.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT sqlite_version()')
    print('Versao do SQLite:', cursor.fetchone())

# ─── 2.2 CREATE TABLE — Definindo a Estrutura ──────────────────
with sqlite3.connect('pipeline.db') as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            origem TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pendente',
            num_tokens INTEGER,
            criado_em TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')
    print('Tabela criada (ou ja existia).')

# ─── 2.3 INSERT — Criando Registros ────────────────────────────
with sqlite3.connect('pipeline.db') as conn:
    # INSERT com parametro unico (sempre use ? — nunca f-string)
    conn.execute(
        'INSERT INTO documentos (nome, origem, num_tokens) VALUES (?, ?, ?)',
        ('relatorio_q1.pdf', 'upload', 1842)
    )

    # INSERT em lote — executemany() e mais eficiente que um loop
    documentos = [
        ('contrato_2024.pdf', 'email', 950),
        ('ata_reuniao.docx', 'drive', 420),
        ('proposta.pdf', 'upload', 2100),
    ]
    conn.executemany(
        'INSERT INTO documentos (nome, origem, num_tokens) VALUES (?, ?, ?)',
        documentos
    )
    print('Registros inseridos.')

# ─── 2.4 SELECT — Consultando Registros ────────────────────────
with sqlite3.connect('pipeline.db') as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Todos os registros
    cursor.execute('SELECT * FROM documentos ORDER BY criado_em DESC')
    print('\nTodos os registros:')
    for row in cursor.fetchall():
        print(dict(row))

    # Filtrar por status
    cursor.execute(
        'SELECT id, nome, status FROM documentos WHERE status = ?',
        ('pendente',)
    )
    pendentes = cursor.fetchall()
    print(f'\n{len(pendentes)} documentos pendentes')

    # Agregar: contar por status
    cursor.execute(
        'SELECT status, COUNT(*) as total FROM documentos GROUP BY status'
    )
    print('\nContagem por status:')
    for row in cursor.fetchall():
        print(f'{row["status"]}: {row["total"]}')

    # fetchone() para busca por ID
    cursor.execute('SELECT * FROM documentos WHERE id = ?', (1,))
    doc = cursor.fetchone()
    print('\nBusca por id=1:', doc['nome'] if doc else 'Nao encontrado')

# ─── 2.5 UPDATE e DELETE ────────────────────────────────────────
with sqlite3.connect('pipeline.db') as conn:
    # UPDATE: marcar documento como processado
    conn.execute(
        'UPDATE documentos SET status = ? WHERE id = ?',
        ('processado', 1)
    )

    # UPDATE condicional
    conn.execute(
        'UPDATE documentos SET status = ? WHERE num_tokens > ?',
        ('fila_longa', 1500)
    )

    # Verificar quantas linhas foram afetadas
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE documentos SET status = ? WHERE origem = ?',
        ('revisao', 'email')
    )
    print(f'\n{cursor.rowcount} linha(s) atualizada(s) para origem=email')

    # DELETE por ID
    conn.execute('DELETE FROM documentos WHERE id = ?', (3,))

    # DELETE condicional
    conn.execute(
        'DELETE FROM documentos WHERE status = ? AND num_tokens < ?',
        ('pendente', 100)
    )
    print('Delecoes executadas.')
