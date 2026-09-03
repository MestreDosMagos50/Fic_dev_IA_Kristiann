# ==============================================================================
# Aula 15: Embeddings e Busca Semântica
# Módulo 5: Avaliação Qualitativa da Busca Semântica
# ==============================================================================
"""
Para validação inicial, a avaliação qualitativa é o método mais prático: 
você define casos de teste representativos e analisa os resultados.

Categorias de teste:
- Correspondência direta
- Sinônimos
- Pergunta natural
- Paráfrase
- Negativo (irrelevante)
- Específico vs geral
"""

def avaliar_busca(casos: list[dict], motor_busca, k: int = 3) -> None:
    """
    Executa casos de teste e imprime resultado para inspeção visual.
    Cada caso tem: 'query', 'esperado' (palavra-chave no resultado ideal)
    """
    print('\n' + '=' * 60)
    print(' AVALIAÇÃO QUALITATIVA DA BUSCA SEMÂNTICA')
    print('=' * 60)
    
    acertos = 0
    for caso in casos:
        resultados = motor_busca(caso['query'], k=k)
        textos_resultado = [r['texto'].lower() for r in resultados]
        esperado = caso.get('esperado', '').lower()
        
        # Verificar se o esperado aparece em algum resultado
        acertou = any(esperado in txt for txt in textos_resultado) if esperado else None
        
        if acertou is True:
            acertos += 1
            
        status = '✓' if acertou else ('?' if acertou is None else '✗')
        print(f'\n[{caso["categoria"]}] {status}')
        print(f' Query: {caso["query"]}')
        
        for i, r in enumerate(resultados, 1):
            preview = r['texto'][:80].replace('\n', ' ')
            print(f' {i}. [{r["score"]:.3f}] {preview}...')
            
    total_check = sum(1 for c in casos if c.get('esperado'))
    print(f'\nResultado: {acertos}/{total_check} casos com resultado esperado no top-{k}')
    print('=' * 60)

if __name__ == "__main__":
    # Casos de Teste (Seção 5.1)
    CASOS_TESTE = [
        {'categoria': 'Direto', 'query': 'rescisão de contrato', 'esperado': 'rescisão'},
        {'categoria': 'Sinônimos', 'query': 'encerramento do acordo', 'esperado': 'rescisão'},
        {'categoria': 'Pergunta', 'query': 'Qual é a multa por cancelamento?', 'esperado': 'multa'},
        {'categoria': 'Negativo', 'query': 'clima e temperatura hoje', 'esperado': ''},
    ]

    # Motor de busca Fictício apenas para demonstrar a execução do teste
    def motor_busca_ficticio(query: str, k: int = 3) -> list[dict]:
        # Simulando o retorno de um motor de busca
        if "clima" in query:
            return [{'texto': 'Não há resultados', 'score': 0.1}]
        else:
            return [
                {'texto': 'O contrato prevê multa de 20%...', 'score': 0.85},
                {'texto': 'Em caso de rescisão antecipada...', 'score': 0.75}
            ][:k]

    # Rodando o avaliador
    avaliar_busca(CASOS_TESTE, motor_busca_ficticio, k=2)
