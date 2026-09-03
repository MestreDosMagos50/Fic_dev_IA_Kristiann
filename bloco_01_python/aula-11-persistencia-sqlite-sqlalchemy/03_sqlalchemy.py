from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import DeclarativeBase, Session
from datetime import datetime

# ─── 3.1 Engine, Base e Session ────────────────────────────────
# Engine: aponta para o banco (SQLite local em arquivo)
engine = create_engine('sqlite:///pipeline_orm.db', echo=False)
# echo=True imprime o SQL gerado — util para depuracao
#
# Outros bancos (mesmo codigo ORM):
#   PostgreSQL: 'postgresql://user:senha@localhost/dbname'
#   MySQL:      'mysql+pymysql://user:senha@localhost/dbname'
#   Memoria:    'sqlite:///:memory:'  <- ideal para testes


# Base: classe mae de todos os modelos
class Base(DeclarativeBase):
    pass


# ─── 3.2 Definindo Modelos ─────────────────────────────────────
class Documento(Base):
    __tablename__ = 'documentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    origem = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default='pendente')
    num_tokens = Column(Integer, nullable=True)
    score_ia = Column(Float, nullable=True)
    criado_em = Column(DateTime, default=datetime.now)
    atualizado_em = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self) -> str:
        return f'<Documento id={self.id} nome={self.nome!r} status={self.status!r}>'


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_id = Column(Integer, nullable=False)  # chave estrangeira simples
    nome = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f'<Tag doc_id={self.doc_id} nome={self.nome!r}>'


# Criar todas as tabelas no banco (idempotente)
Base.metadata.create_all(engine)
print('Tabelas criadas!')

# ─── 3.3 Create — Inserindo Registros ──────────────────────────
with Session(engine) as session:
    # Inserir um objeto
    doc1 = Documento(
        nome='relatorio_q1.pdf',
        origem='upload',
        num_tokens=1842,
        score_ia=0.87,
    )
    session.add(doc1)
    session.commit()
    print(f'ID atribuido: {doc1.id}')  # SQLAlchemy preenche apos commit

    # Inserir varios objetos de uma vez
    docs = [
        Documento(nome='contrato_2024.pdf', origem='email', num_tokens=950),
        Documento(nome='ata_reuniao.docx', origem='drive', num_tokens=420),
        Documento(nome='proposta.pdf', origem='upload', num_tokens=2100, score_ia=0.91),
    ]
    session.add_all(docs)
    session.commit()
    print(f'{len(docs)} documentos inseridos')

# ─── 3.4 Read — Consultando com Query ──────────────────────────
with Session(engine) as session:
    # Buscar todos
    todos = session.query(Documento).all()
    print('\nTodos os documentos:')
    for d in todos:
        print(d)

    # Buscar por ID (retorna None se nao existir)
    doc = session.get(Documento, 1)
    print('\nBusca por id=1:', doc.nome if doc else 'Nao encontrado')

    # Filtrar com filter()
    pendentes = (session.query(Documento)
                 .filter(Documento.status == 'pendente')
                 .all())
    print(f'{len(pendentes)} pendentes')

    # Filtros compostos
    grandes = (session.query(Documento)
               .filter(Documento.num_tokens > 1000,
                       Documento.status == 'pendente')
               .order_by(Documento.criado_em.desc())
               .limit(5)
               .all())
    print(f'{len(grandes)} documentos grandes e pendentes')

    # filter_by() — sintaxe alternativa com kwargs (mais concisa)
    uploads = session.query(Documento).filter_by(origem='upload').all()
    print(f'{len(uploads)} documentos com origem=upload')

    # Contar sem carregar objetos
    total = session.query(Documento).count()
    print(f'Total: {total}')

    # Primeira ocorrencia (retorna None se vazio)
    primeiro = session.query(Documento).first()
    print('Primeiro registro:', primeiro)

# ─── 3.5 Update — Atualizando Registros ────────────────────────
with Session(engine) as session:
    # Buscar, modificar, commit — SQLAlchemy detecta a mudanca
    doc = session.get(Documento, 1)
    if doc:
        doc.status = 'processado'
        doc.score_ia = 0.93
        session.commit()
        print(f'\nDocumento {doc.id} atualizado')

    # Update em lote com query().update()
    atualizados = (session.query(Documento)
                   .filter(Documento.num_tokens > 1500)
                   .update({'status': 'fila_longa'}))
    session.commit()
    print(f'{atualizados} documento(s) movidos para fila_longa')

# ─── 3.6 Delete — Removendo Registros ──────────────────────────
with Session(engine) as session:
    # Buscar e deletar objeto especifico
    doc = session.get(Documento, 3)
    if doc:
        session.delete(doc)
        session.commit()
        print('\nDocumento removido')

    # Delete em lote
    removidos = (session.query(Documento)
                 .filter(Documento.status == 'pendente',
                         Documento.num_tokens < 100)
                 .delete())
    session.commit()
    print(f'{removidos} registro(s) removido(s)')

print('\nFim da execucao. Banco salvo em pipeline_orm.db')