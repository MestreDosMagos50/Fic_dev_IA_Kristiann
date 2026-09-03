import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

print("3. Visualização com Matplotlib\n")

# Criar diretório para salvar os gráficos
os.makedirs('graficos', exist_ok=True)

print("--- 3.1 Configuração e Estrutura Básica ---\n")

# Configurações globais (executar uma vez por notebook/script)
plt.rcParams['figure.dpi'] = 120           # resolução da figura
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.spines.top'] = False    # remove borda superior
plt.rcParams['axes.spines.right'] = False  # remove borda direita

# --- Criando uma figura com um único gráfico ---
fig, ax = plt.subplots(figsize=(8, 5))  # largura x altura em polegadas

# ax é o objeto Axes — use-o para plotar e personalizar
ax.plot([1, 2, 3, 4], [10, 20, 15, 30])
ax.set_title('Meu primeiro gráfico', fontsize=14, fontweight='bold')
ax.set_xlabel('Período')
ax.set_ylabel('Valor')

plt.tight_layout()  # ajusta espaçamentos automaticamente
plt.savefig('graficos/grafico_3_1.png', dpi=150, bbox_inches='tight')
plt.show()

print("Gráfico 3.1 salvo como 'grafico_3_1.png' e exibido.\n")


print("--- 3.2 Gráfico de Linha ---\n")

# Dados: evolução das médias da turma por bimestre
bimestres = ['1º Bim', '2º Bim', '3º Bim', '4º Bim']
media_turma_a = [7.2, 7.5, 6.8, 8.1]
media_turma_b = [6.5, 7.0, 7.3, 7.8]

fig, ax = plt.subplots(figsize=(9, 5))

# Plotando duas séries na mesma figura
ax.plot(bimestres, media_turma_a,
        marker='o',         # marcador nos pontos
        linewidth=2,
        color='#2E86C1',
        label='Turma A')

ax.plot(bimestres, media_turma_b,
        marker='s',         # quadrado
        linewidth=2,
        linestyle='--',     # linha tracejada
        color='#E74C3C',
        label='Turma B')

# Linha de referência: nota mínima para aprovação
ax.axhline(y=7.0, color='gray', linestyle=':', linewidth=1.5,
           label='Mínimo aprovação (7.0)')

ax.set_title('Evolução da Média por Bimestre', fontsize=14, fontweight='bold')
ax.set_xlabel('Bimestre')
ax.set_ylabel('Média da Turma')
ax.set_ylim(5.0, 10.0)       # definir limites do eixo Y
ax.legend()                  # exibir legenda
ax.grid(axis='y', alpha=0.4) # grade horizontal suave

plt.tight_layout()
plt.savefig('graficos/evolucao_medias_3_2.png', dpi=150, bbox_inches='tight')
plt.show()

print("Gráfico 3.2 salvo como 'evolucao_medias_3_2.png' e exibido.\n")


print("--- 3.3 Gráfico de Barras ---\n")

# --- Barras verticais: média por disciplina ---
disciplinas = ['Matemática', 'Português', 'História', 'Ciências', 'Inglês']
medias = [7.3, 8.1, 7.8, 6.9, 8.4]
cores = ['#2E86C1' if m >= 7.0 else '#E74C3C' for m in medias]

fig, ax = plt.subplots(figsize=(9, 5))
barras = ax.bar(disciplinas, medias, color=cores,
                width=0.6, edgecolor='white', linewidth=0.8)

# Rótulo de valor em cima de cada barra
for barra in barras:
    altura = barra.get_height()
    ax.text(
        barra.get_x() + barra.get_width() / 2, # posição x: centro da barra
        altura + 0.05,                         # posição y: levemente acima
        f'{altura:.1f}',                       # texto: valor formatado
        ha='center', va='bottom', fontsize=10, fontweight='bold'
    )

ax.axhline(y=7.0, color='gray', linestyle='--', linewidth=1.2,
           label='Mínimo aprovação')
ax.set_title('Média por Disciplina — Todas as Turmas', fontsize=14, fontweight='bold')
ax.set_ylabel('Média')
ax.set_ylim(0, 10)
ax.legend()

plt.tight_layout()
plt.savefig('graficos/medias_disciplinas_3_3.png', dpi=150, bbox_inches='tight')
plt.show()

print("Gráfico 3.3 (Barras Verticais) salvo como 'medias_disciplinas_3_3.png' e exibido.\n")

# --- Barras horizontais: aprovados vs reprovados por turma ---
turmas = ['Turma A', 'Turma B', 'Turma C']
aprovados = [28, 22, 30]
reprovados = [2, 8, 0]

x = range(len(turmas))
largura = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar([i - largura/2 for i in x], aprovados, largura,
       label='Aprovados', color='#27AE60')
ax.bar([i + largura/2 for i in x], reprovados, largura,
       label='Reprovados', color='#E74C3C')

ax.set_xticks(x)
ax.set_xticklabels(turmas)
ax.set_title('Resultado por Turma', fontsize=14, fontweight='bold')
ax.set_ylabel('Número de Alunos')
ax.legend()

plt.tight_layout()
plt.savefig('graficos/resultado_turmas_3_3.png', dpi=150, bbox_inches='tight')
plt.show()

print("Gráfico 3.3 (Barras Horizontais) salvo como 'resultado_turmas_3_3.png' e exibido.\n")


print("--- 3.4 Histograma ---\n")

# Simulando notas de 90 alunos (distribuição realista)
np.random.seed(42)
notas_turma = np.concatenate([
    np.random.normal(loc=7.5, scale=1.2, size=70),  # maioria no meio
    np.random.uniform(low=3.0, high=5.0, size=20),  # alunos com dificuldade
])
notas_turma = np.clip(notas_turma, 0, 10) # limitar entre 0 e 10

fig, ax = plt.subplots(figsize=(9, 5))
n, bins, patches = ax.hist(
    notas_turma,
    bins=15,                 # número de intervalos
    color='#2E86C1',
    edgecolor='white',
    linewidth=0.8,
    alpha=0.85               # leve transparência
)

# Colorir barras abaixo de 7.0 em vermelho
for patch, left_edge in zip(patches, bins[:-1]):
    if left_edge < 7.0:
        patch.set_facecolor('#E74C3C')

# Linha de média
media = notas_turma.mean()
ax.axvline(x=media, color='#1F3864', linestyle='-', linewidth=2,
           label=f'Média: {media:.2f}')

# Linha de mínimo para aprovação
ax.axvline(x=7.0, color='gray', linestyle='--', linewidth=1.5,
           label='Mínimo aprovação (7.0)')

ax.set_title('Distribuição das Notas — Todas as Turmas', fontsize=14, fontweight='bold')
ax.set_xlabel('Nota Final')
ax.set_ylabel('Número de Alunos')
ax.legend()

plt.tight_layout()
plt.savefig('graficos/distribuicao_notas_3_4.png', dpi=150, bbox_inches='tight')
plt.show()

print("Gráfico 3.4 (Histograma) salvo como 'distribuicao_notas_3_4.png' e exibido.\n")


print("--- 3.5 Salvando Gráficos com Qualidade ---\n")

# Reutilizando a última figura para salvar em múltiplos formatos
fig.savefig('graficos/distribuicao_notas_3_5.png', dpi=150, bbox_inches='tight', facecolor='white')
fig.savefig('graficos/distribuicao_notas_3_5.pdf', bbox_inches='tight') # vetorial, ideal para impressão
fig.savefig('graficos/distribuicao_notas_3_5.svg', bbox_inches='tight') # vetorial, ideal para web

print("Gráfico 3.5 salvo em múltiplos formatos (.png, .pdf, .svg).\n")
