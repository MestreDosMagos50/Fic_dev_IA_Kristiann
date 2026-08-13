# analise_turma/estatisticas.py
# Responsabilidade: Estatísticas sobre a turma (Desafio 3)

def maior_media(resultados: list[dict]) -> dict | None:
    """Encontra o aluno com a maior média.
    
    Args:
        resultados: Lista de dicionários contendo os dados processados dos alunos, 
                    incluindo a chave 'media'.
                    
    Returns:
        O dicionário do aluno com a maior média, ou None se a lista for vazia.
    """
    if not resultados:
        return None
    return max(resultados, key=lambda x: x['media'])

def menor_media(resultados: list[dict]) -> dict | None:
    """Encontra o aluno com a menor média.
    
    Args:
        resultados: Lista de dicionários contendo os dados processados dos alunos, 
                    incluindo a chave 'media'.
                    
    Returns:
        O dicionário do aluno com a menor média, ou None se a lista for vazia.
    """
    if not resultados:
        return None
    return min(resultados, key=lambda x: x['media'])
