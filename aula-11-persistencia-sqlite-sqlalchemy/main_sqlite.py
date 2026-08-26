import sqlite3

# ====================================================================
# MÓDULO 1: Persistência e o Ciclo CRUD
# ====================================================================
# Persistência é a capacidade de armazenar dados além do tempo de vida
# de um processo. Bancos de dados relacionais resolvem esse problema.
# Ciclo CRUD: Create (INSERT), Read (SELECT), Update (UPDATE), Delete (DELETE).
# (Este módulo é conceitual)


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


# ====================================================================
# MÓDULO 3: SQLAlchemy — ORM Declarativo
# ====================================================================
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime

# ─── 3.1 Configuração: Engine, Base e Session ──────────────────
engine = create_engine('sqlite:///pipeline.db', echo=False)

class Base(DeclarativeBase):
    pass

# ─── 3.2 Definindo Modelos ─────────────────────────────────────
class DocumentoORM(Base):
    __tablename__ = 'documentos_orm'  # Alterado para não conflitar com a tabela do módulo 2
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    origem = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default='pendente')
    num_tokens = Column(Integer, nullable=True)
    score_ia = Column(Float, nullable=True)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Documento id={self.id} nome={self.nome!r} status={self.status!r}>'

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, nullable=False)
    nome = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<Tag doc_id={self.doc_id} nome={self.nome!r}>'

# Criar todas as tabelas no banco
Base.metadata.create_all(engine)
print('\n[Módulo 3] Tabelas ORM criadas!')

# ─── 3.3 Create — Inserindo Registros ──────────────────────────
with Session(engine) as session:
    doc1 = DocumentoORM(
        nome='relatorio_q1.pdf',
        origem='upload',
        num_tokens=1842,
        score_ia=0.87,
    )
    session.add(doc1)
    session.commit()
    print(f'ID atribuído: {doc1.id}')

    docs = [
        DocumentoORM(nome='contrato_2024.pdf', origem='email', num_tokens=950),
        DocumentoORM(nome='ata_reuniao.docx', origem='drive', num_tokens=420),
        DocumentoORM(nome='proposta.pdf', origem='upload', num_tokens=2100, score_ia=0.91),
    ]
    session.add_all(docs)
    session.commit()
    print(f'{len(docs)} documentos inseridos.')

# ─── 3.4 Read — Consultando com Query ──────────────────────────
with Session(engine) as session:
    print('\nBuscar todos:')
    todos = session.query(DocumentoORM).all()
    for d in todos:
        print(d)

    print('\nBuscar por ID:')
    doc = session.get(DocumentoORM, 1)
    print(doc.nome if doc else 'Não encontrado')

    print('\nFiltrar com filter():')
    pendentes = (session.query(DocumentoORM)
                 .filter(DocumentoORM.status == 'pendente')
                 .all())
    print(f'{len(pendentes)} pendentes')

    total = session.query(DocumentoORM).count()
    print(f'Total: {total}')

# ─── 3.5 Update — Atualizando Registros ────────────────────────
with Session(engine) as session:
    doc = session.get(DocumentoORM, 1)
    if doc:
        doc.status = 'processado'
        doc.score_ia = 0.93
        session.commit()
        print(f'\nDocumento {doc.id} atualizado')

    atualizados = (session.query(DocumentoORM)
                   .filter(DocumentoORM.num_tokens > 1500)
                   .update({'status': 'fila_longa'})
    )
    session.commit()
    print(f'{atualizados} documento(s) movidos para fila_longa')

# ─── 3.6 Delete — Removendo Registros ──────────────────────────
with Session(engine) as session:
    doc = session.get(DocumentoORM, 3)
    if doc:
        session.delete(doc)
        session.commit()
        print('\nDocumento removido')

    removidos = (session.query(DocumentoORM)
                 .filter(DocumentoORM.status == 'pendente', DocumentoORM.num_tokens < 100)
                 .delete()
    )
    session.commit()
    print(f'{removidos} registro(s) removido(s)')


# ====================================================================
# MÓDULO 4: sqlite3 vs SQLAlchemy — Quando Usar Cada Um
# ====================================================================
# - sqlite3 (stdlib): SQL puro, maior controle, scripts simples, ETL, prototipagem.
# - SQLAlchemy ORM: Objetos Python, SQL gerado, mais legível, portátil (PostgreSQL, MySQL).
# (Este módulo é apenas conceitual)


print('\nFim da execucao. Banco salvo em pipeline.db')

