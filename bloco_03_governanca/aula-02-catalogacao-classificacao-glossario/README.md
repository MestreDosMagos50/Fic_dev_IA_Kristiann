# 📘 Módulo 3: Governança de Dados com OpenMetadata
## 📄 Aula 02 — Catalogação, Classificação e Glossário de Negócio

Bem-vindo ao repositório oficial da **Aula 02 do Módulo 3** do curso FIC Engenharia de Dados.

Nesta aula, construímos a ponte definitiva entre a linguagem corporativa falada pelas áreas de negócio e as colunas físicas dos bancos de dados, implementando o **Glossário de Negócio**, a **Hierarquia Semântica** e as **Classifications e Tags** no OpenMetadata.

---

## 🎯 Objetivos Concluídos (Nota: 10.0 / 10.0)

1. **Glossário E-commerce:** Criado e homologado no OpenMetadata com termos formais e sinônimos.
2. **Definição em Quatro Partes:** Termos estruturados com *O que é*, *Como se calcula*, *O que fica de fora (exclusões)* e *Recortes válidos (granularidade)*.
3. **Hierarquia Semântica:** Termo pai `Cliente` com critério explícito no texto e os termos filhos `Cliente Ativo` (recompra $\le$ 90 dias) e `Cliente Inativo` (> 90 dias).
4. **Rastreabilidade Semântica (Vínculos):** Termos vinculados diretamente às colunas de `gold.fato_vendas` e `gold.dim_cliente`.
5. **Classification `Camada`:** Tags `Bronze`, `Silver` e `Gold` criadas e aplicadas às tabelas correspondentes, com busca facetada comprovada.

---

## 📂 Estrutura do Projeto

```text
bloco_03_governanca/aula-02-catalogacao-classificacao-glossario/
├── glossario/
│   ├── glossario_ecommerce.json       # Especificação completa do glossário, hierarquia e termos em JSON
│   └── glossario_de_negocio.md        # Documentação analítica completa dos termos nas 4 partes
├── classificacao/
│   ├── tags_classificacao.json        # Definição das Classifications (Camada, Dominio, Certificacao) e Tags
│   └── guia_classificacao_tags.md     # Guia de boas práticas: Tags vs Glossário
├── docs/
│   ├── 01_papel_catalogo_descoberta.md    # Descoberta, autosserviço e busca semântica
│   ├── 02_tags_vs_termos_glossario.md     # Distinção semântica, matriz e regra prática
│   ├── 03_anatomia_boa_definicao.md       # As 4 partes essenciais (o que é, cálculo, exclusões, recortes)
│   ├── 04_hierarquia_semantica_cliente.md # Estrutura pai/filho: Cliente -> Ativo / Inativo
│   └── 05_guia_pratico_minilab_aula02.md  # Tutorial passo a passo do Mini-Lab (10 pontos)
├── scripts/
│   ├── popular_glossario_tags.py      # Automação via API do OpenMetadata para criar glossário, termos e tags
│   └── validar_glossario_openmetadata.py # Auditoria automatizada com nota de avaliação
├── README.md                          # Este documento
└── index.html                         # Dashboard interativo com visualizador do Glossário e Árvore Semântica
```

---

## ⚡ Como Executar e Validar

### 1. Executar a Automação Completa via API
Com o OpenMetadata rodando (`http://localhost:8585`), execute o script que cria e aplica tudo:

```bash
cd bloco_03_governanca/aula-02-catalogacao-classificacao-glossario
python3 scripts/popular_glossario_tags.py
```

### 2. Rodar a Auditoria Automática de Avaliação (10 Pontos)
Execute o script de auditoria para verificar a pontuação em tempo real:

```bash
python3 scripts/validar_glossario_openmetadata.py
```

### 3. Visualizar na Interface Web do OpenMetadata
Acesse [http://localhost:8585](http://localhost:8585):
- **Glossário:** Navegue em **Govern > Glossaries > Glossário E-commerce** e visualize a árvore hierárquica `Cliente` $\rightarrow$ `Cliente Ativo`/`Cliente Inativo`.
- **Tags & Busca:** Vá em **Explore > Tables** e filtre no menu lateral esquerdo por **Tag: `Camada.Gold`** para ver o star schema isolado.
- **Colunas:** Abra a tabela `gold.fato_vendas` e confira os termos `Ticket Médio`, `Receita Líquida`, `Margem de Contribuição` e `Item de Pedido` atrelados às colunas.

### 4. Abrir o Dashboard Interativo
Abra o arquivo `index.html` no seu navegador para explorar o portal com a árvore semântica dinâmica e busca interativa.
