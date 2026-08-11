# FIC DEV IA - Módulo Python

Repositório para armazenar os exemplos de código e exercícios práticos do curso FIC DEV IA.

## Estrutura do Repositório

```text
.
├── README.md
├── aula-02-sintaxe-basica/
│   ├── 01_variaveis_e_constantes.py
│   ├── 02_tipos_de_dados.py
│   ├── 03_operadores.py
│   ├── 04_strings_e_fstrings.py
│   ├── 05_controle_de_fluxo.py
│   └── mini_lab_calculadora_imc.py
├── aula-03-estrutura-dados-json/
│   ├── 01_listas.py
│   ├── 02_tuplas.py
│   ├── 03_sets.py
│   ├── 04_dicionarios.py
│   ├── 05_iteracao.py
│   ├── 06_json.py
│   ├── turma_exemplo.json
│   └── mini-lab-analise-turma/
│       ├── analise_turma.py
│       ├── turma.json
│       └── relatorio.json
├── aula-04-funcoes-organizacao/
│   ├── 01_definicao_e_anatomia.py
│   ├── 02_parametros_e_argumentos.py
│   ├── 03_retorno_de_valores.py
│   ├── 04_escopo_de_variaveis.py
│   ├── 05_docstrings_e_type_hints.py
│   ├── 06_boas_praticas_srp.py
│   ├── 07_biblioteca_interna/
│   │   ├── calculos.py
│   │   └── main.py
│   └── mini-lab-imc-funcoes/
│       └── imc_funcoes.py
└── aula-05-excecoes-depuracao-qualidade/
    ├── 01_excecoes_em_python.py
    ├── 02_depuracao_no_vscode.py
    ├── 03_modulo_logging.py
    ├── 04_estilo_pep8_e_ferramentas.py
    ├── pyproject.toml
    └── mini-lab-leitor-robusto/
        ├── pyproject.toml
        ├── alunos.csv
        ├── leitor_robusto.py
        └── logs/
            └── app.log
```

---

## Aulas

### Aula 02 - Sintaxe Essencial e Tipos Básicos
- Variáveis, constantes e convenções da PEP 8
- Tipos primitivos (`int`, `float`, `str`, `bool`) e conversão de tipos
- Operadores aritméticos, relacionais e lógicos
- Manipulação e formatação de texto com f-strings
- Estruturas de controle de fluxo (`if`, `elif`, `else`)
- **Mini-lab:** Calculadora de IMC com validação básica

### Aula 03 - Estruturas de Dados e JSON
- Listas (`list`), tuplas (`tuple`), conjuntos (`set`) e dicionários (`dict`)
- Métodos essenciais de manipulação e iteração (`for`, `enumerate`, `zip`, `dict.items()`)
- Serialização e desserialização de JSON (`json.dump`, `json.dumps`, `json.load`, `json.loads`)
- **Mini-lab:** Análise estatística de turma de alunos com geração de relatório JSON

### Aula 04 - Funções e Organização do Código
- Anatomia e definição de funções com `def`
- Parâmetros posicionais, nomeados, com valor padrão, `*args` e `**kwargs`
- Retorno único, múltiplos retornos e retorno antecipado
- Escopo de variáveis (LEGB - Local, Enclosing, Global, Built-in)
- Documentação com Docstrings (Google Style) e Type Hints (PEP 484)
- Princípio da Responsabilidade Única (SRP) e modularização
- **Mini-lab:** Calculadora de IMC refatorada e modular

### Aula 05 - Exceções, Depuração e Qualidade
- Tratamento de exceções com blocos `try / except / else / finally` e princípio EAFP
- Lançamento e re-lançamento de erros com `raise` e encadeamento com `raise ... from`
- Exceções customizadas com hierarquia de domínio herdando de `Exception`
- Configuração de logging profissional com níveis de severidade e `RotatingFileHandler`
- Depuração no VSCode (breakpoints, watches, step over/into)
- Padrões de código limpo com PEP 8, Type Hints modernos e linter/formatter Ruff
- **Mini-lab:** Leitor Robusto de Dados CSV com Exceções Customizadas, Logs e Relatório de Qualidade

---

## Como Executar

Acesse a pasta da aula desejada e execute os scripts via terminal:

```bash
# Executando exemplos da Aula 05
cd aula-05-excecoes-depuracao-qualidade
python3 01_tratamento_de_excecoes.py
python3 04_modulo_logging.py

# Executando o mini-lab da Aula 05
cd mini-lab-leitor-robusto
python3 leitor_robusto.py
```


